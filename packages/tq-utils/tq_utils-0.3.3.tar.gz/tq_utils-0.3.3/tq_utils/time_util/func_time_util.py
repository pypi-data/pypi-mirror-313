from typing import Optional

from .timer import Timer

# func_timeout 用起来有问题，实际用 timer 计时用了 0.03-0.04s，但是设定小于该值的 timeout 不会抛出异常，但进行调试到是正常。
import func_timeout as ft  # https://github.com/kata198/func_timeout

func_set_timeout = ft.func_set_timeout  # Decorator
FunctionTimedOut = ft.FunctionTimedOut
StoppableThread = ft.StoppableThread


def func_timeout(timeout: float, func, args: tuple = (), kwargs: Optional[dict] = None, timer: Timer = None):
    """ Copy from func_timeout.func_timeout
    Runs the given function for up to #timeout# seconds. Raises any exceptions #func# would raise, returns what #func# would return (unless timeout is exceeded), in which case it raises FunctionTimedOut
    :param timeout: Maximum number of seconds to run #func# before terminating. timeout must be positive, otherwise it will raise ValueError.
    :param func: The function to call.
    :param args: Any ordered arguments to pass to the function. Default: ().
    :param kwargs: Keyword arguments to pass to the function. Default: None.
    :param timer: if specified, timer will be used to keep track of how much time the #func# uses.
    :raises FunctionTimedOut:
        Raise FunctionTimedOut, if #timeout# is exceeded, otherwise anything #func# could raise will be raised
        Note: If the timeout is exceeded, FunctionTimedOut will be raised within the context of the called function every two seconds until it terminates,
        but will not block the calling thread (a new thread will be created to perform the join). If possible, you should try/except FunctionTimedOut
        to return cleanly, but in most cases it will 'just work'.
    :returns: The return value that #func# gives
    """
    if timeout <= 0:
        raise ValueError('timeout must be positive.')
    if timer:
        with timer:
            result = ft.func_timeout(timeout, func, args, kwargs)
    else:
        result = ft.func_timeout(timeout, func, args, kwargs)
    return result
