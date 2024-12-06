import threading


class SingletonTypeThreadSafe(type):
    # _instance = None  # 只存储一个类的实例，即仅支持一个单例类
    _instances = {}  # 支持多个单例类的实例管理
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with SingletonTypeThreadSafe._instance_lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonTypeThreadSafe, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
