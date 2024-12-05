import json
from typing import Callable, Any, Tuple, Union, Dict

from ..file_manager import FileManager

PYTHON_SERIALIZABLE_TYPES = Union[dict, list, tuple, str, int, float, bool, None]


class TqJSONEncoder(json.JSONEncoder):
    """
    The default JSONEncoder of tq_json package.
    You can set serialize function through set_class_serialize_function, so that TqJSONEncoder can convert the correct type of class to the Python serializable object.
    Also, you don't have to self-make Encoder again.
    See set_class_serialize_function function for more details.
    """
    # 存储设置的类对应的字典化方法，只需要得到可序列化对象即可，不用得到 json 字符串。
    class_serialize_functions: Dict[Union[type, Tuple[type, ...]], Callable[[Any], PYTHON_SERIALIZABLE_TYPES]] = dict()

    @classmethod
    def set_class_serialize_function(cls, class_type: Union[type, Tuple[type, ...]],
                                     dictify_function: Callable[[Any], PYTHON_SERIALIZABLE_TYPES]):
        """
        Set class_serialize_function.
        In condition that the object is instance of class_type, the dump methods in the tq_json package will call class_serialize_function to create Python serializable object through given object.
        :param class_type: the type of the class
        :param dictify_function: the function that will create dict through object. Notice: The keys of dict should be the property names of the object.
        """
        cls.class_serialize_functions[class_type] = dictify_function

    def default(self, obj):
        for key, value in self.class_serialize_functions.items():
            if isinstance(obj, key):
                return value(obj)  # 最终方法返回的结果是，可以 json 序列化的对象
        return json.JSONEncoder.default(self, obj)


class TqJSONDecoder(json.JSONDecoder):
    """
    The default JSONDecoder of tq_json package.
    You can set objectify function through set_class_objectify_function, so that TqJSONDecoder can convert correct dict to the specified class.
    Also, you don't have to self-make Decoder again.
    See set_class_objectify_function function for more details.
    """
    # 存储设置的类对应的对象化方法。key 是类的属性名元组，value 是对象化方法。因为 json 反序列化为字典后，属性值是唯一标识了，那么就是用属性名元组进行区分。
    class_objectify_functions: Dict[Tuple[str, ...], Callable[[dict], Any]] = dict()

    def __init__(self, *args, **kwargs):
        # 使用 object_hook 实现自定义的解码逻辑
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    @classmethod
    def set_class_objectify_function(cls, class_property_names: Tuple[str, ...],
                                     objectify_function: Callable[[dict], Any]):
        """
        Set class_objectify_function.
        In condition that the keys of dict are exactly same as the property names of class, the load methods in the tq_json package will call class_objectify_function to create class object through dict.
        :param class_property_names: tuple of class's property names.
        :param objectify_function: the function that will create class object through dict
        """
        cls.class_objectify_functions[class_property_names] = objectify_function

    def object_hook(self, obj: dict):
        for key, value in self.class_objectify_functions.items():
            class_property_names = sorted(list(key))
            obj_property_names = sorted(list(obj.keys()))
            if class_property_names == obj_property_names:
                return value(obj)
        return obj


def dump_json(path, json_data, json_encoder=TqJSONEncoder):
    """
    with-open 配合 json.dump 的普通 json 转换以及文本输出.
    :param path: 输出 json 文本的文件路径
    :param json_data: 转换成 json 文本的对象
    :param json_encoder: 自定义 JSONEncoder
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, cls=json_encoder, indent=4, ensure_ascii=False)


def dump_json_safe(path, json_data, json_encoder=TqJSONEncoder):
    """
    将对象转换成 json 文本并安全地写入 json 文件中. 安全，即若 json 文件的父目录不存在，则会进行创建。
    :param path: 输出 json 文本的文件路径
    :param json_data: 转换成 json 文本的对象
    :param json_encoder: 自定义 JSONEncoder
    """
    with FileManager(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, cls=json_encoder, indent=4, ensure_ascii=False)


def dumps_json(json_data, json_encoder=TqJSONEncoder):
    """
    将对象转换得到 json 文本
    :param json_data: 转换成 json 文本的对象
    :param json_encoder: 自定义 JSONEncoder
    :return: 转换的 json 文本
    """
    return json.dumps(json_data, cls=json_encoder, indent=4, ensure_ascii=False)


def load_json(path: str, encoding='utf-8', json_decoder=TqJSONDecoder):
    """
    with-open 配合 json.load 的普通 json 文本读取并转换得到对象.
    :param path: json 文件的路径
    :param encoding: json 文件中文本的编码
    :param json_decoder: 自定义 JSONDecoder
    :return: json 文本读取并转换得到的对象
    """
    with open(path, 'r', encoding=encoding) as f:
        return json.load(f, cls=json_decoder)


def load_json_safe(path: str, encoding='utf-8', json_decoder=TqJSONDecoder):
    """
    从 json 文件中安全地读取 json 文本并得到转换的对象. 安全，即若 json 文件不存在，则会创建一个空白的 json 文件并读取.
    :param path: json 文件的路径
    :param encoding: json 文件中文本的编码
    :param json_decoder: 自定义 JSONDecoder
    :return: json 文本读取并转换得到的对象
    """
    with FileManager(path, 'r', encoding=encoding, initial_data='') as f:
        return json.load(f, cls=json_decoder)


def loads_json(json_string, json_decoder=TqJSONDecoder):
    """
    将 json 文本转换得到对象
    :param json_string: 需要转换的 json 文本
    :param json_decoder: 自定义 JSONDecoder
    :return: json 文本转换得到的对象
    """
    return json.loads(json_string, cls=json_decoder)
