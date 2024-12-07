# -*- coding: UTF-8 -*-
# Copyright©2020 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
缓存器
"""
from typing import Any, NoReturn
from random import choice
from aitool import get_str


class Cache(dict):
    """
    默认使用block模式，仅记录前size个样例。
    TODO 如果没有特殊需求，可以直接使用内部修饰器 @functools.cache 或 @functools.lru_cache(maxsize=128)

    >>> c = Cache({0:0, 1:1, 2:2}, size=2)
    >>> len(c)
    2
    >>> c[3] = 3
    >>> len(c)
    2
    >>> c.update({4:4, 5:5})
    >>> len(c)
    2
    >>> c.set_size(10)
    >>> c.update([(6,6), (7,7)])
    >>> len(c)
    4
    """
    def __init__(self, seq=None, size=100000, method='random', **kwargs):
        """
        :param seq: dict的默认参数
        :param size: cache存储的数量上限
        :param method: cache的控制模式。
            * 'block': 超出容量上限后不再更新
            * 'random':  超出容量上限后随机丢弃一条记录
        :param kwargs: dict的默认参数
        """
        self.size = size
        self.method = method
        super(Cache, self).__init__(**kwargs)
        if seq:
            for k in seq:
                self[k] = seq[k]

    def __setitem__(self, *args, **kwargs):
        if self.method == 'block':
            if self.__len__() < self.size:
                super().__setitem__(*args, **kwargs)
        elif self.method == 'FIFO':
            while self.__len__() >= self.size:
                super().popitem()
            super().__setitem__(*args, **kwargs)
        elif self.method == 'random':
            while self.__len__() >= self.size:
                key = choice(list(self))
                super().pop(key)
            super().__setitem__(*args, **kwargs)
        else:
            raise ValueError

    def update(self, mapping: Any, **kwargs: Any) -> NoReturn:
        if hasattr(mapping, 'keys'):
            for k in mapping.keys():
                self[k] = mapping[k]
        else:
            for k, v in mapping:
                self[k] = v
        for k in kwargs.keys():
            self[k] = kwargs[k]

    def set_size(self, size: int) -> NoReturn:
        assert isinstance(size, int)
        self.size = size

    def get_size(self) -> NoReturn:
        return self.size

    def set_method(self, method: str) -> NoReturn:
        assert isinstance(method, str)
        self.method = method


def get_cache(**kwargs) -> dict:
    """
    获取一个 Cache 对象
    """
    return Cache(**kwargs)


def cache(size=100000, get_key=get_str) -> NoReturn:
    """
    cache装饰器，记录函数的输入输出。

    :param size: 存储的输入输出对的数量
    :param get_key: 用函数的输入构建key的方法，默认为concat_all
    :return: Any

    >>> @cache()
    ... def repeat(x):
    ...    print('calculating')
    ...    return x
    >>> print(repeat(10))
    calculating
    10
    >>> print(repeat(10))
    10
    """
    def decorate(func):
        _cache = Cache(size=size)

        def implement(*args, **kwargs):
            key = get_key(*args, **kwargs)
            if key in _cache:
                return _cache[key]
            result = func(*args, **kwargs)
            _cache[key] = result
            return result
        return implement
    return decorate


if __name__ == '__main__':
    import doctest

    doctest.testmod()
