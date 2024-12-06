import json
from ..file_manager import FileManager


def dump_json(path, json_data, json_encoder=None):
    """
    with-open 配合 json.dump 的普通 json 转换以及文本输出.
    :param path: 输出 json 文本的文件路径
    :param json_data: 转换成 json 文本的对象
    :param json_encoder: 自定义 JSONEncoder
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, cls=json_encoder, indent=4, ensure_ascii=False)


def dump_json_safe(path, json_data, json_encoder=None):
    """
    将对象转换成 json 文本并安全地写入 json 文件中. 安全，即若 json 文件的父目录不存在，则会进行创建。
    :param path: 输出 json 文本的文件路径
    :param json_data: 转换成 json 文本的对象
    :param json_encoder: 自定义 JSONEncoder
    """
    with FileManager(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, cls=json_encoder, indent=4, ensure_ascii=False)


def dumps_json(json_data, json_encoder=None):
    """
    将对象转换得到 json 文本
    :param json_data: 转换成 json 文本的对象
    :param json_encoder: 自定义 JSONEncoder
    :return: 转换的 json 文本
    """
    return json.dumps(json_data, cls=json_encoder, indent=4, ensure_ascii=False)


def load_json(path: str, encoding='utf-8', json_decoder=None):
    """
    with-open 配合 json.load 的普通 json 文本读取并转换得到对象.
    :param path: json 文件的路径
    :param encoding: json 文件中文本的编码
    :param json_decoder: 自定义 JSONDecoder
    :return: json 文本读取并转换得到的对象
    """
    with open(path, 'r', encoding=encoding) as f:
        return json.load(f, cls=json_decoder)


def load_json_safe(path: str, encoding='utf-8', json_decoder=None):
    """
    从 json 文件中安全地读取 json 文本并得到转换的对象. 安全，即若 json 文件不存在，则会创建一个空白的 json 文件并读取.
    :param path: json 文件的路径
    :param encoding: json 文件中文本的编码
    :param json_decoder: 自定义 JSONDecoder
    :return: json 文本读取并转换得到的对象
    """
    with FileManager(path, 'r', encoding=encoding, initial_data='') as f:
        return json.load(f, cls=json_decoder)


def loads_json(json_string, json_decoder=None):
    """
    将 json 文本转换得到对象
    :param json_string: 需要转换的 json 文本
    :param json_decoder: 自定义 JSONDecoder
    :return: json 文本转换得到的对象
    """
    return json.loads(json_string, cls=json_decoder)
