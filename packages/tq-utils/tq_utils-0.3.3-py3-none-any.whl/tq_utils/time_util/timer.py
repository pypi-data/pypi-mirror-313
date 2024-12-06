"""
Timer 用于计时的类、上下文管理器 和 修饰器。详细用法见对应的测试代码。
"""
import functools
import time
from dataclasses import dataclass, field
from typing import ClassVar, Any, Dict


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


@dataclass
class Timer:
    """
    Timer class, context manager and decorator.
    :property: name: the name of the timer. If you use timer through context manager, the timer must be named.
    :property: text: the string format of time report.
    :property: logger: the logging function.
    """
    __timers: ClassVar[Dict[str, float]] = {}
    name: str = None
    text: str = "{} elapsed time: {:0.4f} seconds"
    logger: Any = print
    __start_time: Any = field(default=None, init=False, repr=False)
    __last_start_time: Any = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Initialization: add timer to dict of timers. will be called after __init__ """
        if self.name:  # 为每个 timer 实例初始化对应名称的消耗时间和开始时间（没有指定名称不支持保留消耗时间）.
            self.__timers.setdefault(self.name, 0)

    def start(self):
        """Start a new timer"""
        if self.__start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self.__start_time = time.perf_counter()
        self.__last_start_time = time.localtime()  # 记录最新地开始计时时间

    def stop(self) -> float:
        """
        Stop the timer, report and return the elapsed time(seconds).
        :return: elapsed time in seconds.
        """
        if self.__start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self.__start_time
        self.__start_time = None

        if self.logger:
            self.logger(self.text.format(self.name if self.name else 'Timer', elapsed_time))
        if self.name:  # 如果有命名，则会累计时间
            self.__timers[self.name] += elapsed_time  # 累计这次的时间，并还是存储在 timers 中。

        return elapsed_time

    @property
    def last_start_time(self) -> str:
        """ return the last start time in '%Y-%m-%d %H:%M:%S' format. """
        return time.strftime('%Y-%m-%d %H:%M:%S', self.__last_start_time)

    @classmethod
    def getTimerNames(cls):
        """
        Get Timer names.
        :return list: the str names of the timers
        """
        return cls.__timers.keys()

    @classmethod
    def popTime(cls, name, default=None) -> float:
        """
        Get Timer's time and delete timer.
        :param name: Timer name.
        :param default: default value, if timer not exists.
        :return: time elapsed (seconds), or default value if timer not exists.
        """
        return cls.__timers.pop(name, default)

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()

    def __call__(self, func):
        """Support using Timer as a decorator"""

        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_timer
