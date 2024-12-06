from freezegun import freeze_time as _freeze_time
from functools import partial
from contextlib import contextmanager
from typing import Callable
from heaobject.error import HEAException
try:
    import pywintypes
    _MaybeDockerIsNotRunning: Exception | type = pywintypes.error
    _additional_docker_running_check_logic: Callable[[Exception], bool] = lambda e: e.args == (2, 'CreateFile', 'The system cannot find the file specified.')
except:
    # TODO: implement Linux logic here.
    # The code below is a sensible default that results in all raised
    # exceptions being propagated up the stack.
    _MaybeDockerIsNotRunning = Exception
    _additional_docker_running_check_logic = lambda e: False


freeze_time = partial(_freeze_time, "2022-05-17", ignore=['asyncio'])
freeze_time.__doc__ = "Context manager that freezes time to 2022-05-17T00:00:00-06:00."

class MaybeDockerIsNotRunning(HEAException):
    """Exception raised to inform the test runner that perhaps Docker is not
    running. The python Docker library raises non-specific errors when there is
    no running Docker daemon, so we cannot be 100% sure."""
    pass

@contextmanager
def maybe_docker_is_not_running():
    """
    Context manager to wrap code that interacts with the Docker daemon to
    suggest to the test runner that the Docker daemon may not be running when
    certain exceptions are raised. The exceptions raised are platform
    dependent. The word maybe in the function name is there because the python
    Docker library raises non-specific errors when there is no running Docker
    daemon, but we do the best we can. The original exception is nested in case
    you need to see it.

    :raises MaybeDockerIsNotRunningException: if the wrapped code raises an
    error suggesting that Docker may not be running. The original exception is
    nested. Otherwise, raised exceptions are propagated up the stack."""
    try:
        yield
    except _MaybeDockerIsNotRunning as e:
        if _additional_docker_running_check_logic(e):
            raise MaybeDockerIsNotRunning from e
        else:
            raise e
