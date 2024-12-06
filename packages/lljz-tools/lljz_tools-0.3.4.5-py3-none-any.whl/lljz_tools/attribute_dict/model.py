# coding=utf-8

"""
@fileName       :   model.py
@data           :   2024/2/3
@author         :   jiangmenggui@hosonsoft.com
"""
import re
from itertools import cycle
from types import GenericAlias, UnionType


class _AttributeDictMetaclass(type):

    def __new__(cls, name, bases, attrs, total=False, variable=True, check_type=False):
        """

        :param name:
        :param bases:
        :param attrs:
        :param total: 是否全部字段必填
        :param variable: 是否允许增加字段
        :param check_type: 是否需要检查类型
        """
        if name in ['AttributeDict', 'IgnoreCaseAttributeDict']:
            return type.__new__(cls, name, bases, attrs)
        attrs['__default__'] = {}
        __remove__ = []
        for key, value in attrs.items():
            if key.startswith('__'):  # 跳过双下划綫开头的属性
                continue
            attrs['__default__'][key] = value
            __remove__.append(key)
        for k in __remove__:
            attrs.pop(k)
        attrs['__d_args__'] = (total, variable, check_type)
        return type.__new__(cls, name, bases, attrs)


def _init_value(value, type_):
    try:
        if isinstance(type_, GenericAlias):
            if issubclass(type_.__origin__, dict):
                if not isinstance(value, dict):
                    raise TypeError
                if len(type_.__args__) == 2:
                    return type_.__origin__(
                        {_init_value(v, type_.__args__[0]): _init_value(v, type_.__args__[1]) for k, v in value.items()}
                    )
                elif len(type_.__args__) == 1:
                    return type_.__origin__({k: _init_value(v, type_.__args__[0]) for k, v in value.items()})
                else:
                    return type_.__origin__(value)
            elif issubclass(type_.__origin__, list | tuple | set):
                return type_.__origin__(_init_value(v, t) for t, v in zip(cycle(type_.__args__), value))
            return type_.__origin__(value)
        elif isinstance(type_, UnionType):
            for t in type_.__args__:
                try:
                    return _init_value(value, t)
                except TypeError:
                    continue
            else:
                raise TypeError(f"{value!r} must be {type_!r}")
        return type_(value)
    except ValueError:
        raise TypeError(f"{value!r} must be {type_!r}")
    except TypeError:
        raise TypeError(f"{value!r} must be {type_!r}")


class AttributeDict(dict, metaclass=_AttributeDictMetaclass):

    def __init__(self, __mapper=None, **kwargs):
        super().__init__((__mapper or {}), **kwargs)

        for key, value in self.__annotations__.items():
            key = self._get_key(key)
            if key in self:
                if self.__d_args__[2]:  # 检查类型
                    self[key] = _init_value(self[key], value)
                elif isinstance(value, _AttributeDictMetaclass):
                    self[key] = value(**self[key])
                elif isinstance(value, GenericAlias):
                    if not self[key]:
                        break
                    for t in value.__args__:
                        print('>>>>>', t)
                        if not isinstance(t, _AttributeDictMetaclass):
                            continue
                        try:
                            self[key] = value.__origin__(t(**v) for v in self[key])
                            break
                        except Exception:  # noqa
                            continue
                    # if self[key]:
                    #     self[key] = [value.__args__[0](**v) for v in self[key]]
                continue
            if key not in self.__default__ and self.__d_args__[0]:
                raise ValueError(f"{self.__class__.__name__!r} missing key {key!r}")
            self[key] = self.__default__.get(key, None)

    def _get_key(self, key):
        return key

    def __getattr__(self, item):
        try:
            return self[self._get_key(item)]
        except KeyError:
            if self.__d_args__[1]:
                return None
            raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {item!r}")

    def __setattr__(self, item, value):
        item = self._get_key(item)
        if item not in self and not self.__d_args__[1]:
            raise TypeError(f"{self.__class__.__name__!r} cannot add attribute {item!r}")
        self[item] = value

    def __delattr__(self, item):
        return self.__delitem__(self._get_key(item))

    __show__ = None

    def __str__(self):
        show = self.__show__
        if not show:
            show = self.__annotations__.keys()
        if isinstance(show, str):
            show = re.split(r'[,\s]+', show.strip())
        val = ', '.join(f"{key}={self.__getattr__(key)!r}" for key in show)
        return f'{self.__class__.__name__}({val})'

    __repr__ = __str__


class IgnoreCaseAttributeDict(AttributeDict):

    def _get_key(self, key):
        for k in self.keys():
            if k.lower() == key.lower():
                return k
        return super()._get_key(key)


Model = AttributeDict


def to_attr_dict(obj):
    if isinstance(obj, AttributeDict):
        return type(obj)({key: to_attr_dict(value) for key, value in obj.items()})
    elif isinstance(obj, dict):
        return AttributeDict({key: to_attr_dict(value) for key, value in obj.items()})
    elif isinstance(obj, list | tuple | set):
        return type(obj)(to_attr_dict(item) for item in obj)
    else:
        return obj


if __name__ == '__main__':
    class Book(AttributeDict, variable=False, total=True, check_type=True):
        name: str
        author: str
        price: float
        history: set[int]

        __show__ = 'name author'


    class User(IgnoreCaseAttributeDict, total=True, variable=True, check_type=True):
        name: int | str
        books: list[Book]


    user = User(name='tom', books=[{'name': 'python', 'author': 123, 'price': '3.2', 'history': ('1', 2, 3, 2)}])
    print(user)
    user.password = "abc"
    print(user.password)

    # data = to_attr_dict({"name": "tom", "books": [{'name': 'python', 'author': 123, 'price': '3.2', 'history': ('1', 2, 3, 2)}]})
    # print(data.name)
    # d = AttributeDict(**{"name": "tom"})
    # print(d['name'])
