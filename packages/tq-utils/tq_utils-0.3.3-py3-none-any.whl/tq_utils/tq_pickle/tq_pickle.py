import pickle

from ..file_manager import FileManager


def load(path: str, initial_data=None):
    """
    Load pickle file to Python object.
    :param path: pickle file path. file suffix is '.pkl'.
    :param initial_data: if file doesn't exist, it'll initialize it with initial data. Default is empty list.
    """
    if initial_data is None:
        initial_data = []
    with FileManager(path, mode='rb', encoding=None, initial_data=pickle.dumps(initial_data)) as fr:
        return pickle.load(fr)


def dump(path: str, data):
    """
    Dump Python object to pickle file.
    :param path: pickle file path. file suffix is '.pkl'.
    :param data: Python object to dump.
    """
    with FileManager(path, mode='wb', encoding=None) as fw:
        pickle.dump(data, fw)
