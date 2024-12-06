import enum
import functools
import os
import time
from typing import Any, Callable

from ..file_manager import FileManager


class LoggingLevel(enum.Enum):
    DEBUG = 10, 'DEBUG'
    INFO = 20, 'INFO'
    WARNING = 30, 'WARNING'
    ERROR = 40, 'ERROR'
    CRITICAL = 50, 'CRITICAL'


class TQRunLogger:
    """
    用于记录每单次运行的日志输出.
    支持 实例, Decorator 和 Context Manager 的使用方式。
    """
    __LOGGING_MESSAGE_FORMAT = '[{time}][{level}]: {message}\n'
    __LOGGING_DIR_FORMAT = '%Y-%m-%d-%H-%M-%S'
    __LOGGING_TIME_FORMAT = '%Y%m%d-%H:%M:%S'
    __LOGGING_FILE_NAME = 'logging'
    __LOGGING_FILE_EXTENSION = '.log'

    def __init__(self, logging_output_dir: str, logging_level: LoggingLevel = LoggingLevel.DEBUG, max_bytes: int = -1,
                 backup_count: int = -1):
        """
        :param logging_output_dir: 日志文件输出的根目录
        :param logging_level: 日志输出的限制级别
        :param max_bytes: 单个日志大小限制(Byte)(会有一定的超出，实现限制，仅会在大小超出时才做分割); defaults -1, 表示不进行分割
        :param backup_count: 分割日志时，保存最新日志的数量; defaults -1, 表示保存所有分割的日志
        """
        self.__run_logging_output_dir = os.path.join(logging_output_dir,
                                                     time.strftime(self.__LOGGING_DIR_FORMAT, time.localtime()))
        self.__num = 1  # 表示当前分割日志的第几份
        self.__max_bytes = max_bytes
        self.__backup_count = backup_count
        self.__logging_level_value = logging_level.value[0]
        self.__logging_file_path = self.__get_logging_file_path(self.__num)
        self.__logger_file = self.__get_logging_file_manager().open()

    def __get_logging_file_path(self, num: int):
        """
        :param num: 当前分割日志第几份
        """
        index = '.' + str(num) if self.__max_bytes > 0 else ''  # 如果进行日志分割，会对日志进行编号
        return os.path.join(self.__run_logging_output_dir,
                            self.__LOGGING_FILE_NAME + index + self.__LOGGING_FILE_EXTENSION)

    def __get_logging_file_manager(self):
        return FileManager(self.__logging_file_path, 'at')

    def __rotate_logs(self):
        self.__logger_file.close()  # 先关闭之前的日志文件
        self.__num += 1  # 当前分割日志的份数 +1
        self.__logging_file_path = self.__get_logging_file_path(self.__num)  # 获得新的日志路径
        self.__logger_file = self.__get_logging_file_manager().open()  # 打开对应的日志文件
        # num = 1, back=2,   1,       0 < 2 < 1, 不满足，不删除
        # num = 2, back=2,   1, 2     0 < 2 < 2, 不满足，不删除
        # num = 3, back=2,   1, 2, 3, 0 < 2 < 3, 满足，删除  (3-2)=(1)
        if 0 < self.__backup_count < self.__num:  # 删除备份要求之外的旧日志
            os.remove(self.__get_logging_file_path(self.__num - self.__backup_count))

    def __logging_message(self, level: LoggingLevel, message: str):
        level_value, level_str = level.value
        if level_value < self.__logging_level_value:
            return
        if 0 < self.__max_bytes < os.path.getsize(self.__logging_file_path):
            self.__rotate_logs()
        self.__logger_file.write(
            self.__get_format_message(level_str=level_str, message=message))

    def __get_format_message(self, level_str: str, message: str):
        time_str = time.strftime(self.__LOGGING_TIME_FORMAT, time.localtime())
        return self.__LOGGING_MESSAGE_FORMAT.format(level=level_str, time=time_str, message=message)

    def debug(self, message: str):
        self.__logging_message(level=LoggingLevel.DEBUG, message=message)

    def info(self, message: str):
        self.__logging_message(level=LoggingLevel.INFO, message=message)

    def warning(self, message: str):
        self.__logging_message(level=LoggingLevel.WARNING, message=message)

    def error(self, message: str):
        self.__logging_message(level=LoggingLevel.ERROR, message=message)

    def critical(self, message: str):
        self.__logging_message(level=LoggingLevel.CRITICAL, message=message)

    def logging_output_file(self, file_name: str, file_data: Any, file_save_function: Callable[[str, Any], None]):
        """
        日志输出文件
        :param file_name: 文件全称
        :param file_data: 文件数据
        :param file_save_function: 文件保存处理函数. params(file_path:str, file_data: Any)
        """
        filepath = os.path.join(self.__run_logging_output_dir, file_name)
        abs_filepath = os.path.abspath(filepath)
        file_dir = os.path.dirname(abs_filepath)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_save_function(abs_filepath, file_data)
        self.info('save file at {}'.format(abs_filepath))

    def __enter__(self):
        """Support using logger as a context manager"""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__logger_file.close()

    def __call__(self, func):
        """Support using logger as a decorator"""

        @functools.wraps(func)
        def wrapper_logger(*args, **kwargs):
            with self as logger:
                return func(logger, *args, **kwargs)

        return wrapper_logger
