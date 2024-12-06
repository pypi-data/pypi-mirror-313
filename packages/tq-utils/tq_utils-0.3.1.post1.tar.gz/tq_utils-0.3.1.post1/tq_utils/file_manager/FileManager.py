import os
import platform
import re
from typing import Callable, Optional, Union


class ModeErrorException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class PermissionErrorException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class FileNotFoundException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class UnsupportedPlatformException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class InvalidFileNameException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


def is_valid_filename(filename: str) -> bool:
    """
    验证文件名的有效性，区分 Windows 和 Linux。

    :param filename: 文件名
    :return: 如果文件名有效返回 True，否则返回 False
    """
    # 检查文件名长度
    if not (1 <= len(filename) <= 255):
        return False

    # 获取操作系统
    os_name = platform.system()

    # 定义非法字符和保留文件名
    if os_name == 'Windows':
        # Windows 系统的非法字符
        illegal_chars = r'[<>:"/\\|?*]'
        reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8',
                          'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}

        # 检查非法字符
        if re.search(illegal_chars, filename):
            return False

        # 检查是否是保留文件名
        name_only = os.path.splitext(filename)[0].upper()
        if name_only in reserved_names:
            return False

    elif os_name == 'Linux':
        # Linux 系统的非法字符（几乎没有限制）
        # 这里可以根据需要添加特定的检查
        if '/' in filename:
            return False

    else:
        raise UnsupportedPlatformException("Unsupported operating system.")

    return True


class FileManager:
    """
    主要通过 Context Manager 的方式使用，也可以通过实例使用: f.open() 获取 TextIOWrapper。
    """

    def __init__(self, path: Union[int, str], mode: str, buffering: int = -1, encoding: Optional[str] = 'utf-8',
                 errors: str = None, newline: str = None, closefd: bool = True,
                 opener: Optional[Callable[[str, int], int]] = None, initial_data: Union[str, bytes] = None):
        """
        :param path: file path to open
        :param mode: file open mode.
            e.g. 'r', 'rb', 'rt', 'r+', 'rb+', 'rt+',
                 'w', 'wb', 'wt', 'w+', 'wb+', 'wt+',
                 'a', 'ab', 'at',
                 'x', 'xb', 'xt', 'x+', 'xb+', 'xt+'
        :param buffering: buffer size
        :param encoding: file encoding mode. binary mode doesn't take an encoding argument.
        :param errors: default None. Set 'ignore' to ignore the decode error and output illegal characters.
        :param newline: Line feed processing mode, None(default), ''(blank string), '\n', '\r\n', '\r'.
        :param closefd: use file descriptor to close file. turn on it when use a file descriptor to open file.
        :param opener: open file opener.
        :param initial_data: It'll automatically create the file and initialize it with initial data, if it doesn't exist.
        """
        self.path = path
        self.mode = mode
        self.buffering = buffering
        self.encoding = encoding
        self.errors = errors
        self.newline = newline
        self.closefd = closefd
        self.opener = opener
        self.initial_data = initial_data
        self.file = None
        self.modes_r = ['r', 'rb', 'rt', 'r+', 'rb+', 'rt+']
        self.modes_w = ['w', 'wb', 'wt', 'w+', 'wb+', 'wt+']
        self.modes_a = ['a', 'ab', 'at']
        self.modes_x = ['x', 'xb', 'xt', 'x+', 'xb+', 'xt+']

    def open(self):
        abspath = os.path.abspath(self.path)
        dirs = os.path.dirname(abspath)  # 获得路径的目录
        os.makedirs(dirs, exist_ok=True)  # 创建所有父文件夹
        file_name = os.path.basename(abspath)  # 获取文件名称
        if not is_valid_filename(file_name):
            raise InvalidFileNameException('Invalid filename.')

        if self.mode in self.modes_r:
            # 读文件需要判断文件是否存在，不存在则创建
            if not os.path.exists(abspath):
                if isinstance(self.initial_data, str):
                    mode = self.modes_w[0]
                    encoding = 'utf-8'
                else:
                    mode = self.modes_w[1]
                    encoding = None
                f = open(abspath, mode, encoding=encoding)
                f.write(self.initial_data)
                f.close()
        elif self.mode in self.modes_x:  # 想想还是不对创建写进行处理（删掉已存在的文件或改为覆盖写）,就让它自己抛出异常吧
            pass
        elif self.mode not in self.modes_w and self.mode not in self.modes_a:
            raise ModeErrorException('the input mode is wrong')

        try:
            self.file = open(self.path, self.mode, self.buffering, self.encoding, self.errors, self.newline,
                             self.closefd, self.opener)
        except PermissionError:
            raise PermissionErrorException('Insufficient permissions, please run as administrator.')
        return self.file

    def close(self):
        if not self.file.close:
            self.file.close()

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
