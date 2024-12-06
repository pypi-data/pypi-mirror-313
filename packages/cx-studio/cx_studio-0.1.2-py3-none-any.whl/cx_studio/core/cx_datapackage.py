class DataPackage:
    """
    DataPackage 是一个用于存储和访问嵌套数据的类。

    它允许使用点号（`.`）作为键来访问和设置数据，类似于 JavaScript 对象。
    数据存储在一个嵌套的字典结构中，可以存储基本数据类型、列表和自身。
    """

    def __init__(self, **kwargs):
        self._data = {}
        for k, v in kwargs.items():
            self._data[str(k)] = DataPackage.__check_value(v)

    def __repr__(self):
        return repr(self._data)

    @staticmethod
    def __check_value(value):
        if isinstance(value, dict):
            return DataPackage(**value)
        if isinstance(value, list):
            return [DataPackage.__check_value(x) for x in value]
        return value

    def _get_value(self, child_key, *keys):
        child = self._data.get(child_key)
        if not keys:
            return child
        if isinstance(child, DataPackage):
            return child._get_value(*keys)
        return None

    def _set_value(self, child_key, *keys, value=None):
        if not keys:
            self._data[child_key] = value
            return

        if child_key not in self._data:
            self._data[child_key] = DataPackage()

        child = self._data[child_key]
        if isinstance(child, DataPackage):
            child._set_value(*keys, value=value)
            return

        raise KeyError("Invalid key path:", child_key, keys)

    def _del_value(self, child_key, *keys):
        if not keys:
            if child_key not in self._data:
                raise KeyError("Invalid key path", child_key, keys)
            del self._data[child_key]
        elif isinstance(self._data[child_key], DataPackage):
            self._data[child_key]._del_value(*keys)
        else:
            raise KeyError('Invalid key path', child_key, keys)

    def __getitem__(self, item):
        keys = str(item).split(".")
        return self._get_value(*keys)

    def __setitem__(self, key, value):
        keys = str(key).split(".")
        return self._set_value(*keys, value=DataPackage.__check_value(value))

    def __delitem__(self, key):
        keys = str(key).split('.')
        self._del_value(*keys)

    def __getattr__(self, item):
        keys = str(item).split(".")
        return self._get_value(*keys)

    def __setattr__(self, key, value):
        s_key = str(key)
        if s_key.startswith("_"):
            self.__dict__[key] = value
        # elif '.' in s_key:
        #     self._set_value(*(s_key.split('.')), value=DataPackage.__check_value(value))
        else:
            self._data[s_key] = DataPackage.__check_value(value)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def get(self, path: str, default_value=None):
        result = default_value
        try:
            result = self._get_value(*path.split("."))
        except NotImplemented:
            pass
        return result
