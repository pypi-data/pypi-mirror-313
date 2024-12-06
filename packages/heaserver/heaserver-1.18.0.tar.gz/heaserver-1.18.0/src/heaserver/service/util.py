import logging

from functools import wraps
from typing import Optional, Type, Any, TypeVar, Generic, AsyncContextManager
from collections.abc import Sequence, AsyncIterator, Awaitable, Coroutine, Callable, Generator, Iterable
from collections import OrderedDict
import requests
from contextlib import contextmanager
import asyncio
import time
import os
from dataclasses import dataclass
from heaobject.util import now  # Keep here so that older uses of it don't break.
import inspect
from contextlib import asynccontextmanager

RT = TypeVar('RT')  # return type

def async_retry(*exceptions: type[Exception], retries: int = 3, cooldown: int | None = 1,
                verbose = True) -> Callable[[Callable[..., Coroutine[Any, Any, RT]]], Callable[..., Coroutine[Any, Any, RT]]]:
    """
    Decorate an async function to execute it a few times before giving up.

    :param exceptions: One or more exceptions expected during function execution, as positional arguments.
    :param retries: Number of retries of function execution.
    :param cooldown: Seconds to wait before retry. If None, does not cool down.
    :param verbose: Specifies if we should log about not successful attempts.
    :raises: if all retries failed, or an exception other than those in the exceptions parameter was raised, the
    exception from the last try.
    """

    def wrap(func):
        @wraps(func)
        async def inner(*args, **kwargs) -> Any:
            _logger = logging.getLogger(__name__)
            retries_count = 0

            while True:
                try:
                    _logger.debug('About to try %s', func)
                    result = await func(*args, **kwargs)
                except exceptions as err:
                    message = "Exception {} during {} execution. " \
                              "{} of {} retries attempted".format(type(err), func, retries_count, retries)
                    if retries_count >= retries:
                        if verbose:
                            _logger.exception(message)
                        raise err
                    elif verbose:
                        _logger.warning(message)

                    if cooldown:
                        _logger.debug('Cooling down for %s seconds', cooldown)
                        await asyncio.sleep(cooldown)
                    retries_count += 1
                else:
                    return result
        return inner
    return wrap


def async_retry_context_manager(*exceptions: type[Exception], retries = 3, cooldown: Optional[int] = 1,
                                verbose = True) -> Callable[[Callable[..., AsyncContextManager[RT]]], Callable[..., AsyncContextManager[RT]]]:
    def wrap(ctxman: Callable[..., AsyncContextManager[RT]]) -> type[AsyncContextManager[RT]]:
        class AsyncContextManagerWrapper(AsyncContextManager[RT]):
            def __init__(self, *args, **kwargs) -> None:
                self.__args = args
                self.__kwargs = kwargs

            @async_retry(*exceptions, retries=retries, cooldown=cooldown, verbose=verbose)
            async def __aenter__(self) -> RT:
                self.__ctxman = ctxman(*self.__args, **self.__kwargs)
                return await self.__ctxman.__aenter__()

            async def __aexit__(self, exc_type, exc, tb) -> Any:
                return await self.__ctxman.__aexit__(exc_type, exc, tb)
        return AsyncContextManagerWrapper
    return wrap


def retry(*exceptions: Type[Exception], retries: int = 3, cooldown: Optional[int] = 1,
          verbose: bool = True) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """
    Decorate a non-async function to execute it a few times before giving up.

    :param exceptions: One or more exceptions expected during function execution, as positional arguments.
    :param retries: Number of retries of function execution.
    :param cooldown: Seconds to wait before retry. If None, does not cool down.
    :param verbose: Specifies if we should log about not successful attempts.
    :return a callable that accepts a callable, wraps it with the retry behavior, and returns a callable with the same
    signature.
    :raises: if all retries failed, or an exception other than those in the exceptions parameter was raised, the
    exception from the last try.
    """

    def wrap(func):
        @wraps(func)
        def inner(*args, **kwargs):
            _logger = logging.getLogger(__name__)
            retries_count = 0

            while True:
                try:
                    _logger.debug('About to try %s', func)
                    result = func(*args, **kwargs)
                except exceptions as err:
                    message = "Exception {} during {} execution. " \
                              "{} of {} retries attempted".format(type(err), func, retries_count, retries)

                    if retries_count >= retries:
                        verbose and _logger.exception(message)
                        raise err
                    else:
                        verbose and _logger.warning(message)

                    if cooldown:
                        _logger.debug('Cooling down for %s seconds', cooldown)
                        time.sleep(cooldown)
                    retries_count += 1
                else:
                    return result
        return inner
    return wrap


@contextmanager
def modified_environ(*remove, **update):
    """
    Temporarily updates the ``os.environ`` dictionary in-place.

    The ``os.environ`` dictionary is updated in-place so that the modification
    is sure to work in all situations. Code obtained from
    https://stackoverflow.com/questions/2059482/python-temporarily-modify-the-current-processs-environment.

    :param remove: Environment variables to remove.
    :param update: Dictionary of environment variables and values to add/update.
    """
    env = os.environ
    update = update or {}
    remove = remove or []

    # List of environment variables being updated or removed.
    stomped = (set(update.keys()) | set(remove)) & set(env.keys())
    # Environment variables and values to restore on exit.
    update_after = {k: env[k] for k in stomped}
    # Environment variables and values to remove on exit.
    remove_after = frozenset(k for k in update if k not in env)

    try:
        env.update(update)
        [env.pop(k, None) for k in remove]
        yield
    finally:
        env.update(update_after)
        [env.pop(k) for k in remove_after]


@contextmanager
def request_get_with_retry(url: str, retries=10, cooldown: int | None = 5, timeout: float | None = 60) -> Generator[requests.Response, None, None]:
    """
    Context manager that opens a URL, retrying if unsuccessful, and generates a HTTPResponse.

    :param url: the URL to open (required).
    :param retries: the number of retries.
    :param cooldown: the cooldown period (None for no cooldown).
    :param timeout: the connection timeout (None for no timeout).
    :raises TimeoutError: if the final retry timed out.
    :raises URLError: if the final retry errored out.
    """
    logger = logging.getLogger(__name__)
    logger.debug('Connecting to URL %s', url)

    if not retries:
        retries = 0

    @retry(requests.exceptions.RequestException, retries=retries, cooldown=cooldown)
    def do_open() -> requests.Response:
        try:
            with requests.get(url, timeout=timeout) as response:
                return response
        except Exception as e:
            logger.exception(f'Error getting URL {url}')
            raise e
    response = do_open()
    try:
        yield response
    finally:
        response.close()


class DuplicateError(ValueError):
    """
    The exception raised by the check_duplicates function.
    """
    def __init__(self, msg: str, duplicate_item: Any):
        """
        Creates the error.

        :param msg: the message to display when the exception is raised.
        :param duplicate_item: the item triggering the exception.
        """
        super().__init__(msg)
        self.__duplicate_item = duplicate_item

    @property
    def duplicate_item(self) -> Any:
        """The item triggering the exception."""
        return self.__duplicate_item


def check_duplicates(itr: Iterable[Any]):
    """
    Checks an iterable for duplicate items and raises an exception if one is found.

    @param itr: an iterable.
    @raise DuplicateError if a duplicate is found.
    """
    s = set()
    for item in itr:
        if item in s:
            raise DuplicateError(f'Duplicate {item}', item)
        else:
            s.add(item)


@dataclass(frozen=True)
class TypeEnforcingFrozenDataclass:
    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")

def issubclass_silent(cls, class_or_tuple, /):
    """
    Works like the builtin issubclass, except it returns False if cls is not a
    type instead of raising a TypeError.
    """
    return isinstance(cls, type) and cls is not None and issubclass(cls, class_or_tuple)

T = TypeVar('T')

def to_type(cls_or_instance: T | Type[T] | None) -> Type[T] | None:
    if cls_or_instance is None:
        return None
    elif isinstance(cls_or_instance, type):
        return cls_or_instance
    else:
        return type(cls_or_instance)

async def queued_processing(generator: Callable[[], AsyncIterator[T]],
                            item_processor: Callable[[T], Awaitable[None]],
                            exceptions_to_ignore: Callable[[Exception], bool] | None = None,
                            queue_max_size=100, num_workers=10):
    """
    Places items in an async generator into an asyncio queue for processing by the provided async item_processor.
    Specified exceptions may be suppressed.

    :param generator: the item async generator (required).
    :param item_processor: the async item processor.
    :param exceptions_to_ignore: a function that takes an exception parameter and returns whether the exception should
    be suppressed.
    :param queue_max_size the maximum size of the queue (default is 0, meaning infinite size).
    :param num_workers: the number of workers that take items off the queue (default is 10).
    """
    logger = logging.getLogger(__name__)
    queue: asyncio.Queue = asyncio.Queue(queue_max_size)
    async def worker(name: str, queue: asyncio.Queue):
        try:
            logger.debug('Starting worker %s', name)
            while True:
                coro = await queue.get()
                logger.debug('Worker %s processing item %s', name, coro)
                try:
                    await item_processor(coro)
                    logger.debug('Worker %s processing item %s', name, coro)
                finally:
                    queue.task_done()
        except asyncio.CancelledError:
            logger.debug('Ending worker %s', name)
        except:
            logger.exception('Error in worker %s', name)
            raise
    workers: list[asyncio.Task[None]] = []
    for i in range(num_workers):
        workers.append(asyncio.create_task(worker(f'worker-{i}', queue)))
    try:
        async for coro in generator():
            await queue.put(coro)
        await queue.join()
    finally:
        for worker_ in workers:
            worker_.cancel()
        exceptions_to_raise = []
        for r in await asyncio.gather(*workers, return_exceptions=True):
            if isinstance(r, Exception) and (not exceptions_to_ignore or not exceptions_to_ignore(r)):
                exceptions_to_raise.append(r)
        if exceptions_to_raise:
            raise exceptions_to_raise[0]


def public_methods(cls: Type) -> list[str]:
    """
    Returns a list of the provided class' public methods, defined as any callable attribute of the class that is not a
    class and whose name does not begin with an underscore.

    :param cls: the class (required).
    :return: a list of method names.
    """
    l: list[str] = []
    for method in dir(cls):
        attr = getattr(cls, method)
        if not method.startswith('_') and not inspect.isclass(attr):
            l.append(method)
    return l


async def yield_control():
    """
    Yields control from the current async task to another task.
    """
    await asyncio.sleep(0.1)


def raise_multiple(errors: Sequence[BaseException]):
    """
    Raises multiple exceptions at once, nesting them. The first exception in the sequence can be caught in a try-except
    clause around a call to this function.

    :param errors: the exceptions to raise.
    """
    if not errors:
        return
    errors_ = list(errors)
    try:
        raise errors_.pop()
    finally:
        raise_multiple(errors_)


K = TypeVar('K', bound=Any)

class AsyncioLockCache(Generic[K]):
    """
    A cache for asyncio.Lock objects with a fixed capacity, using an LRU eviction policy. K must be an immutable type.

    Attributes:
        capacity (int): The maximum number of locks the cache can hold.
        cache (OrderedDict[str, asyncio.Lock]): The internal cache storing the locks.
        ref_count (dict[str, int]): A dictionary tracking the reference count of each lock.
    """

    def __init__(self, capacity = 128) -> None:
        """
        Initialize the AsyncioLockCache with a given capacity.

        :param capacity: The maximum number of locks the cache can hold. Defaults to 128.
        """
        self.__capacity = capacity if capacity is not None else 128
        self.__cache: OrderedDict[K, asyncio.Lock] = OrderedDict()
        self.__ref_count: dict[K, int] = {}
        self.__lock = asyncio.Lock()

    @property
    def capacity(self) -> int:
        """
        The capacity of the cache (read-only).
        """
        return self.__capacity

    @property
    def cache(self) -> OrderedDict[K, asyncio.Lock]:
        """
        A copy of the internal cache (read-only).
        """
        return self.__cache.copy()

    @property
    def ref_count(self) -> dict[K, int]:
        """
        A copy of the reference count dictionary (read-only).
        """
        return self.__ref_count.copy()

    async def get(self, key: K) -> asyncio.Lock:
        """
        Get the lock associated with the given key, creating a new one if necessary.

        :param key: The key for which to get the lock.
        :return: The lock associated with the given key.
        """
        async with self.__lock:
            if key in self.__cache:
                self.__cache.move_to_end(key)
                self.__ref_count[key] += 1
            else:
                self.__cache[key] = asyncio.Lock()
                self.__ref_count[key] = 1
                if len(self.__cache) > self.__capacity:
                    await self.__evict()
            return self.__cache[key]

    async def release(self, key: K) -> None:
        """
        Release the lock associated with the given key, decrementing its reference count.

        :param key: The key for which to release the lock.
        """
        async with self.__lock:
            if key in self.__ref_count:
                self.__ref_count[key] -= 1
                if self.__ref_count[key] == 0:
                    del self.__ref_count[key]
                    del self.__cache[key]

    async def __evict(self) -> None:
        """
        Evict the least recently used lock that is not currently in use.
        """
        for key in list(self.__cache.keys()):
            if self.__ref_count[key] == 0:
                del self.__ref_count[key]
                del self.__cache[key]
                break


class LockManager(Generic[K]):
    """
    A context manager for acquiring and releasing asyncio locks for specific strings. K must be an immutable type.
    """

    def __init__(self, capacity = 128) -> None:
        """
        Initialize the LockManager.

        :param capacity:  The maximum number of locks the cache can hold. Defaults to 128.
        """
        self.__lock_cache: AsyncioLockCache[K] = AsyncioLockCache(capacity=capacity)

    @asynccontextmanager
    async def lock(self, key: K):
        """
        An async context manager for acquiring and releasing a lock for a specific key.

        :param key: The key for which to acquire the lock.
        """
        lock = await self.__lock_cache.get(key)
        try:
            async with lock:
                yield
        finally:
            await self.__lock_cache.release(key)
