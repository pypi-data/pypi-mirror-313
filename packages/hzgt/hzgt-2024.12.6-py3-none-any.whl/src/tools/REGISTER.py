from ..strop import restrop
from ..sc import SCError


class Func_Register(dict):
    """
    函数注册器
    """
    def __init__(self, *args, **kwargs):
        super(Func_Register, self).__init__(*args, **kwargs)
        self._dict = {}

    def __call__(self, target):
        return self.register(target)

    def register(self, target):
        def add_item(key, value):
            if not callable(value):
                raise Exception(f'{restrop("Error:")} {value} must be callable!')
            if key in self._dict:
                print(f'{restrop("Warning:", f=3)} {value.__name__} already exists and will be overwritten!')
            self[key] = value
            return value

        if callable(target):    # 传入的target可调用 --> 没有给注册名 --> 传入的函数名或类名作为注册名
            return add_item(target.__name__, target)
        else:                   # 不可调用 --> 传入了注册名 --> 作为可调用对象的注册名
            return lambda x: add_item(target, x)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

class Class_Register(dict):
    """
    类-注册器
    """
    def __init__(self, registry_name, *args, **kwargs):
        super(Class_Register, self).__init__(*args, **kwargs)
        self._dict = {}
        self._name = registry_name

    def __setitem__(self, key, value):
        if not callable(value):
            raise SCError(f'Value of a Registry must be a callable! Value: {value}')
        if key is None:
            key = value.__name__
        if key in self._dict:
            print("Key %s already in registry %s." % (key, self._name))
        self._dict[key] = value

    def __call__(self, target):
        return self.register(target)

    def register(self, target):
        """Decorator to register a function or class."""
        def add(key, value):
            self[key] = value
            return value

        if callable(target):
            # @reg.register
            return add(None, target)
        # @reg.register('alias')
        return lambda x: add(target, x)

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def keys(self):
        """key"""
        return self._dict.keys()

    def items(self):
        return self._dict.items()

