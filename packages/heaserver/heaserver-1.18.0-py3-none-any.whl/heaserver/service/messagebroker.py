"""
Implements connectivity to a RabbitMQ message broker.
"""
import sys
from functools import partial
from heaobject.root import DesktopObject, from_json, desktop_object_from_json, desktop_object_type_for_name
from heaserver.service import appproperty
from heaserver.service.config import Configuration
from pathlib import Path
from aiohttp.web import Application
from aio_pika import Message, ExchangeType, connect_robust
from aio_pika.robust_exchange import AbstractExchange
import asyncio
from typing import Optional, Any, TypeVar
from asyncio import CancelledError
from aiormq.exceptions import AMQPConnectionError
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator, AsyncGenerator, Callable, Awaitable
import logging

_logger = partial(logging.getLogger, __name__)

DEFAULT_EXCHANGE = 'hea_desktop_objects'
DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PORT = 5672
DEFAULT_USERNAME = 'guest'
DEFAULT_PASSWORD = 'guest'
DEFAULT_TOPICS = ('heaobject.root.DesktopObject',)
CONFIG_SECTION = 'MessageBroker'


async def subscribe(hostname=DEFAULT_HOSTNAME,
                    port=DEFAULT_PORT,
                    username=DEFAULT_USERNAME,
                    password=DEFAULT_PASSWORD,
                    exchange_name=DEFAULT_EXCHANGE,
                    topics=DEFAULT_TOPICS,
                    prefetch_count=1) -> AsyncGenerator[DesktopObject, None]:
    """
    Asynchronous generator that connects to a RabbitMQ message broker and allows subscribing to desktop objects that
    are published to an exchange.

    :param hostname: RabbitMQ's hostname (localhost by default).
    :param port: RabbitMQ's port (5672 by default).
    :param username: A username for connecting to RabbitMQ (guest by default).
    :param password: A password for connecting to RabbitMQ (guest by default).
    :param exchange_name: the exchange on which to wait for desktop objects (hea_desktop_objects by default)).
    :param topics: a list of one or more desktop object type names to wait for. All subtypes will also be awaited.
    Ensure that all subtypes of interest have been previously loaded into the python interpreter with an import
    statement, the importlib module, or some other method.
    :param prefetch_count: optimizes for performance (usually just leave the default value).
    :return: an async generator of DesktopObjects.
    """
    logger = _logger()

    async with await connect_robust(host=hostname, port=port, login=username, password=password) as connection:
        channel = await connection.channel()
        try:
            exchange = await channel.declare_exchange(exchange_name, ExchangeType.TOPIC)
            queue = await channel.declare_queue(exclusive=True)
            for topic in topics:
                await queue.bind(exchange, routing_key=topic)
                type_ = desktop_object_type_for_name(topic)
                await queue.bind(exchange, routing_key=type_.get_type_name())
                for subtype in type_.get_subclasses():
                    await queue.bind(exchange, routing_key=subtype.get_type_name())
            if prefetch_count:
                await channel.set_qos(prefetch_count=prefetch_count)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        message_body = message.body
                        hea_object = desktop_object_from_json(message_body)
                        assert isinstance(hea_object, tuple(desktop_object_type_for_name(tn) for tn in topics)), f'Expected type {topics} but received {type(hea_object)}'
                        yield hea_object
        finally:
            await channel.close()


def subscriber_cleanup_context_factory(message_body_cb: Optional[Callable[[Application, DesktopObject], Awaitable[None]]] = None,
                                       config: Optional[Configuration] = None,
                                       hostname=None,
                                       port=None,
                                       username=None,
                                       password=None,
                                       exchange_name=DEFAULT_EXCHANGE,
                                       topics=DEFAULT_TOPICS,
                                       prefetch_count=1) -> Callable[
    [Application], AsyncGenerator[None, None]]:
    """
    Creates a cleanup context co-routine for establishing a connection to RabbitMQ as a subscriber. It tries getting
    connection information (hostname, port, username, and password) from the HEA config file, if found. Connection
    information in the config file may be overridden by passing not-None values into this function for the hostname,
    port, username, and password parameters. Hostname, port, username, and password values that remain None are set to
    their default values ('localhost', 5672, 'guest', and 'guest', respectively). Use the topics parameter to set
    one or more desktop object type names that this subscriber will listen for. Use # as a wildcard, for example,
    heaobject.volume.# for any desktop object in the heaobject.volume module. The
    aiohttp.web.app[appproperty.HEA_MESSAGE_BROKER_SUBSCRIBER] property is set to the initialized subscriber object,
    which may be used in an async for loop as follows, where message_body has type bytes:

    async for message_body in app[appproperty.HEA_MESSAGE_BROKER_SUBSCRIBER]:
        print(f'Got {message_body}')

    :param message_body_cb: a coroutine that is invoked when a message is read from the message broker with the
    aiohttp Application object and a DesktopObject as parameters. Raise an exception to signal that the desktop object
    should not be acknowledged as received from the message broker.
    :param config: a heaserver.service.config.Configuration object. The parsed configuration data should have a
    MessageBroker section with four properties:

            Hostname = the hostname of the message broker, localhost by default.
            Port: the message broker's port, 5672 by default.
            Username: a username for connecting to the message broker, guest by default.
            Password: a password for connecting to the message broker, guest by default.

    :param hostname: the hostname of the message broker, localhost by default.
    :param port: the message broker's port, 5672 by default.
    :param exchange_name: an optional MongoDB connection string that will override any database connection
    string in a provided config file.
    :param username: an optional username that will override any username in the connection string.
    :param password: an optional password that will override any password in the connection string.
    :param exchange_name: the exchange name (required).
    :param topics: a list of one or more desktop object type names that this subscriber will listen for. Use # as a
    wildcard, for example, heaobject.volume.# for any desktop object in the heaobject.volume module.
    :param prefetch_count: optimizes for performance (usually just leave the default value).
    """
    _hostname = None
    _port = None
    _username = None
    _password = None
    _prefetch_count = None
    config_data = config.parsed_config if config else None
    if config_data and CONFIG_SECTION in config_data:
        _section = config_data[CONFIG_SECTION]
        _hostname = _section.get('Hostname')
        _port = _section.getint('Port')
        _username = _section.get('Username')
        _password = _section.get('Password')
        _prefetch_count = _section.get('PrefetchCount')
    if hostname is not None:
        _hostname = hostname
    if port is not None:
        _port = port
    if username is not None:
        _username = username
    if password is not None:
        _password = password
    if exchange_name is None:
        exchange_name = DEFAULT_EXCHANGE
    if _prefetch_count is None:
        _prefetch_count = prefetch_count

    if _hostname is None:
        _hostname = DEFAULT_HOSTNAME
    if _port is None:
        _port = DEFAULT_PORT
    if _username is None:
        _username = DEFAULT_USERNAME
    if _password is None:
        _password = DEFAULT_PASSWORD

    async def subscriber_cleanup_context(app: Application) -> AsyncGenerator[None, None]:
        logger = logging.getLogger(__name__)
        logger.debug('Subscribing to topics %s from the message broker', topics)
        queue = subscribe(_hostname, _port, _username, _password, exchange_name, topics, _prefetch_count)

        async def subscriber_loop():
            logger.debug('Awaiting desktop objects from the message broker...')
            async for desktop_object in queue:
                logger.debug('Received desktop object from the message broker: %s', desktop_object)
                try:
                    await message_body_cb(app, desktop_object)
                except CancelledError as e:
                    raise
                except Exception as e:
                    logger.exception('Error in message_body_cb')

        the_task = asyncio.create_task(subscriber_loop())

        yield

        try:
            logger.debug('Cancelling the subscriber loop...')
            the_task.cancel()
            await the_task
        except CancelledError:
            logger.debug('Subscriber loop is cancelled')
        finally:
            await queue.aclose()

    return subscriber_cleanup_context


async def publisher(hostname=DEFAULT_HOSTNAME,
                    port=DEFAULT_PORT,
                    username=DEFAULT_USERNAME,
                    password=DEFAULT_PASSWORD,
                    exchange_name=DEFAULT_EXCHANGE) -> AsyncGenerator[None, DesktopObject]:
    """
    Co-routine that connects to a RabbitMQ message broker and allows publishing desktop objects without having to
    reconnect every time. Call this function followed by anext on the returned asynchronous generator to establish
    a connection to RabbitMQ. Call the publisher's asend method with a desktop object to publish, and call its aclose
    method when done.

    :param desktop_object: the desktop object to publish.
    :param hostname: RabbitMQ's hostname (localhost by default).
    :param port: RabbitMQ's port (5672 by default).
    :param username: A username for connecting to RabbitMQ (guest by default).
    :param password: A password for connecting to RabbitMQ (guest by default).
    :param exchange_name: the exchange on which to publish the desktop object (hea_desktop_objects by default)).
    :raises AMQPConnectionError: if the connection could not be established.
    """
    logger = logging.getLogger(__name__)
    if hostname is None:
        hostname = DEFAULT_HOSTNAME
    if port is None:
        port = DEFAULT_PORT
    if username is None:
        username = DEFAULT_USERNAME
    if password is None:
        password = DEFAULT_PASSWORD
    if exchange_name is None:
        exchange_name = DEFAULT_EXCHANGE
    logger.debug('Connecting to message queue at hostname %s, port %s, username %s', hostname, port, username)

    async with await connect_robust(host=hostname, port=port, login=username, password=password) as connection:
        channel = await connection.channel()
        try:
            exchange = await channel.declare_exchange(exchange_name, ExchangeType.TOPIC)
            while True:
                await _process_desktop_object(desktop_object=(yield), exchange=exchange)
        finally:
            await channel.close()


def publisher_cleanup_context_factory(config: Optional[Configuration] = None,
                                      hostname=None, port=None, username=None, password=None,
                                      exchange_name=DEFAULT_EXCHANGE,
                                      appproperty_=appproperty.HEA_MESSAGE_BROKER_PUBLISHER) -> Callable[
    [Application], AsyncGenerator[None, None]]:
    """
    Creates a cleanup context co-routine for establishing a connection to RabbitMQ as a publisher. It tries getting
    connection information (hostname, port, username, and password) from the HEA config file, if found. Connection
    information in the config file may be overridden by passing not-None values into this function for the hostname,
    port, username, and password parameters. Hostname, port, username, and password values that remain None are set to
    their default values ('localhost', 5672, 'guest', and 'guest', respectively). The
    aiohttp.web.app[appproperty.HEA_MESSAGE_BROKER_PUBLISHER] property is set to the initialized publisher object,
    which may be used as follows, where desktop_object is a desktop object:

    await aiohttp.web.app[appproperty.HEA_MESSAGE_BROKER_PUBLISHER].asend(desktop_object)

    :param config: a heaserver.service.config.Configuration object. The parsed configuration data should have a
    MessageBroker section with four properties:

            Hostname = the hostname of the message broker, localhost by default.
            Port: the message broker's port, 5672 by default.
            Username: a username for connecting to the message broker, guest by default.
            Password: a password for connecting to the message broker, guest by default.

    :param hostname: the optional hostname of the message broker, which will override any hostname in the config file
    (localhost by default).
    :param port: the optional port of the message broker, which will override any port in the config file (5672 by
    default).
    :param username: an optional username that will override any username in the config file (guest by default).
    :param password: an optional password that will override any password in the config file (guest by default).
    :param exchange_name: the exchange name (required).
    :param appproperty_: the app property to user for accessing the publisher. For microservices that only need
    one publisher, the default (appproperty.HEA_MESSAGE_BROKER_PUBLISHER) is fine, but define custom app properties
    using this parameter for microservices that need multiple publishers. To avoid clashes with built-in app
    properties defined by heaserver, avoid app properties starting with HEA_.
    """
    _hostname = None
    _port = None
    _username = None
    _password = None
    config_data = config.parsed_config if config else None
    if config_data and 'DEFAULT' in config_data and 'MessageBrokerEnabled' in config_data['DEFAULT'] and not config_data['DEFAULT'].getboolean('MessageBrokerEnabled'):
        async def do_nothing(app: Application) -> AsyncGenerator[None, None]:
            _logger().warning('Message broker functionality is disabled')
            yield
        return do_nothing

    if config_data and CONFIG_SECTION in config_data:
        _section = config_data[CONFIG_SECTION]
        _hostname = _section.get('Hostname')
        _port = _section.getint('Port')
        _username = _section.get('Username')
        _password = _section.get('Password')
    if hostname is not None:
        _hostname = hostname
    if port is not None:
        _port = port
    if username is not None:
        _username = username
    if password is not None:
        _password = password
    if exchange_name is None:
        exchange_name = DEFAULT_EXCHANGE

    if _hostname is None:
        _hostname = DEFAULT_HOSTNAME
    if _port is None:
        _port = DEFAULT_PORT
    if _username is None:
        _username = DEFAULT_USERNAME
    if _password is None:
        _password = DEFAULT_PASSWORD
    if appproperty_ is None:
        appproperty_ = appproperty.HEA_MESSAGE_BROKER_PUBLISHER

    T = TypeVar('T')

    @asynccontextmanager
    async def new_async_queue(generator: AsyncGenerator[Any, T]) -> AsyncIterator[asyncio.Queue[T]]:
        """
        Creates a new asynchronous queue that asends items placed on the queue to the provided coroutine. It assumes
        that the generator has been "primed" already by calling the built-in anext() on it. It also assumes that the
        caller will call the generator's close() method. Upon exiting the context manager, the queue's resources are
        cleaned up automatically.

        :param generator: an async generator (required).
        :returns a newly created queue.
        """
        queue: asyncio.Queue[T] = asyncio.Queue()
        async def queue_task():
            while True:
                object_to_send = await queue.get()
                try:
                    await generator.asend(object_to_send)
                finally:
                    queue.task_done()
        queue_task_ = asyncio.create_task(queue_task())
        yield queue
        await queue.join()
        queue_task_.cancel()
        try:
            await queue_task_
        except CancelledError:
            pass

    async def publisher_cleanup_context(app: Application) -> AsyncGenerator[None, None]:
        retries = 5
        retry = 0
        cooldown = 10
        while True:
            _publisher = publisher(_hostname, _port, _username, _password, exchange_name)
            try:
                await anext(_publisher)
                async with new_async_queue(_publisher) as queue:
                    app[appproperty_] = queue
                    yield
                    return
            except AMQPConnectionError:
                retry += 1
                if retry > retries:
                    raise
                else:
                    await asyncio.sleep(cooldown)
            finally:
                await _publisher.aclose()

    return publisher_cleanup_context


async def publish_desktop_object(app: Application, desktop_object: DesktopObject,
                                 appproperty_=appproperty.HEA_MESSAGE_BROKER_PUBLISHER):
    """
    Publishes the provided desktop object, if the service is configured with a message broker publisher. If not, then
    this coroutine does nothing.

    :param app: the Application object (required).
    :param desktop_object: a DesktopObject (required).
    :param appproperty_: the application property for the message broker, defaults to
    appproperty.HEA_MESSAGE_BROKER_PUBLISHER.
    """
    if appproperty_ is None:
        appproperty_ = appproperty.HEA_MESSAGE_BROKER_PUBLISHER
    if appproperty_ in app:
        await app[appproperty_].put(desktop_object)


async def _connect_and_publish(desktop_object: DesktopObject, hostname=DEFAULT_HOSTNAME,
                               port=DEFAULT_PORT,
                               username=DEFAULT_USERNAME,
                               password=DEFAULT_PASSWORD,
                               exchange_name=DEFAULT_EXCHANGE):
    """
    Connects to a RabbitMQ message broker and publishes a desktop object to an exchange.

    :param desktop_object: the desktop object to publish.
    :param hostname: RabbitMQ's hostname (localhost by default).
    :param port: RabbitMQ's port (5672 by default).
    :param username: A username for connecting to RabbitMQ (guest by default).
    :param password: A password for connecting to RabbitMQ (guest by default).
    :param exchange_name: the exchange on which to publish the desktop object (hea_desktop_objects by default)).
    """
    publisher_ = publisher(hostname, port, username, password, exchange_name)
    try:
        await anext(publisher_)
        await publisher_.asend(desktop_object)
    finally:
        await publisher_.aclose()


async def _process_desktop_object(desktop_object: DesktopObject, exchange: AbstractExchange):
    topic = desktop_object.get_type_name()
    message_body = desktop_object.to_json()
    message = Message(message_body.encode('utf-8'))
    await exchange.publish(message, routing_key=topic)
    _logger().debug('Sent %r', message)


def _error():
    sys.stderr.write(f'Usage: {sys.argv[0]} subscribe [binding_key] | publish hea_object_json\n')
    sys.exit(1)


async def _main_subscribe():
    topics = sys.argv[2:]
    if not topics:
        _error()

    print(f'[*] Waiting for {", ".join(topics)} objects. To exit press CTRL+C')
    async for desktop_object in subscribe(topics=topics):
        print(f'Got {desktop_object}')


async def _main_publish():
    desktop_object_json_file = sys.argv[2]
    path = Path(desktop_object_json_file)
    if not desktop_object_json_file or not path.exists():
        _error()

    desktop_object = from_json(path.read_text(encoding='utf-8'))
    if not isinstance(desktop_object, DesktopObject):
        _error()

    print(f'[*] Sending {desktop_object.get_type_name()} object...')
    await _connect_and_publish(desktop_object)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    try:
        if sys.argv[1] == 'subscribe':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_main_subscribe())
            loop.close()
        elif sys.argv[1] == 'publish':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_main_publish())
            loop.close()
        else:
            _error()
    except KeyboardInterrupt:
        sys.exit(0)
