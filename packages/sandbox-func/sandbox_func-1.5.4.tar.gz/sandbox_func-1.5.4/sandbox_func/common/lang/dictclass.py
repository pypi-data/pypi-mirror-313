import json
import logging
from collections import UserDict, namedtuple
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DictClass(UserDict):
    """
    字典对象
    数据存储在字典中，
    支持对象属性访问字典数据，
    支持字典的所有操作
    """

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            self._make_dictclass(self.data)
        except Exception as e:
            logger.error(f"args: {args}, kwargs: {kwargs}")
            raise e

    def __getattr__(self, item):
        if item in ["data"]:
            return object.__getattribute__(self, item)
        else:
            return self.data.get(item)

    def __setattr__(self, key, value):
        if key in ["data"]:
            object.__setattr__(self, key, value)
        elif value is not None:
            self.data[key] = value

    def _make_dictclass(self, data: dict):
        for k, v in data.items():
            if isinstance(v, dict):
                self.data[k] = DictClass(v)

    def deepcopy(self):
        new_data = dict()
        for k, v in self.items():
            if isinstance(v, DictClass):
                new_data[k] = v.deepcopy()
            elif hasattr(v, "copy"):
                new_data[k] = v.copy()
            else:
                new_data[k] = v
        return self.__class__(new_data)

    def json(self):
        return json.dumps(self, ensure_ascii=False, default=lambda dclass: dclass.data)  # 数据嵌套

    def dict(self):
        return self.data


def first_true(iterable, default=None, pred=None):
    """
    Returns the first true value in the iterable.
    """
    return next(filter(pred, iterable), default)


def dict_to_object(d):
    """
    将字典转换为对象
    """
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    """
    将json字符串转换为对象
    """
    return json.loads(data, object_hook=dict_to_object)


def safe_copy(source, target):
    """
    安全的从原值拷贝到目标值
    """
    for k, v in source.__dict__.items():
        if hasattr(target, k):
            setattr(target, k, v)

    return target


def dict_copy(source: dict, target):
    """
    安全的从原值拷贝到目标值
    """
    for k, v in source.items():
        if hasattr(target, k):
            setattr(target, k, v)

    return target


def remove_none_value(d: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    移除值为 None 的键值对
    """
    return {k: v for k, v in d.items() if v is not None}
