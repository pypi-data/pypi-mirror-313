"""
def test_open_file():  # context manager usage
    print()
    # loading a file
    # 路径以测试环境为主，E:\Workspace\Pycharm\TQUtils\test
    with FileManager(add_base_dir(r'test.txt'), 'w') as f:
        f.write('Test')
    print(f.closed)  # Output:true


def test_use_file_manager_through_instance():  # instance usage
    fm = FileManager(add_base_dir(r'test1.txt'), 'r')
    f = fm.open()
    print(f.read())
    fm.close()
    # or
    # f.close()
"""
from .FileManager import FileManager, InvalidFileNameException, UnsupportedPlatformException, ModeErrorException, \
    PermissionErrorException, FileNotFoundException, is_valid_filename

__all__ = ['FileManager', 'UnsupportedPlatformException', 'ModeErrorException', 'PermissionErrorException',
           'InvalidFileNameException', 'FileNotFoundException', 'is_valid_filename']
