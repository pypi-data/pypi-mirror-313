"""
使用方法：
    class Singleton(metaclass=SingletonTypeThreadSafe):
        def __init__(self, value):
            pass
如此，即可是的定义的 Singleton 类为单例模式. SingletonTypeThreadSafe是线程安全的。
"""

from .singleton_meta_class import SingletonTypeThreadSafe

__all__ = ['SingletonTypeThreadSafe']
