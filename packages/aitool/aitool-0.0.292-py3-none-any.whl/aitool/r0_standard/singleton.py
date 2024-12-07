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
单例工具
"""
from typing import Callable
from functools import wraps
import threading


def singleton(cls) -> Callable:
    """
    单例修饰器

    :param cls: 被修饰的类
    :return: 单例修饰器

    >>> @singleton
    ... class A:
    ...    def __init__(self, x):
    ...        self.x = x
    >>> a = A(1)
    >>> b = A(2)
    >>> a == b
    True
    """
    _instance = {}

    @wraps(cls)
    def inner(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return inner


def synchronized(func):
    """
    线程锁
    """
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


class Singleton(object):
    """
    线程安全的单例，不保证进程安全

    >>> class SClass(Singleton):
    ...     def __init__(self, a):
    ...         self.a = a
    >>> x = SClass(1)
    >>> y = SClass(2)
    >>> x == y
    True
    >>> x.a
    2
    """
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance


if __name__ == '__main__':
    import doctest

    doctest.testmod()
