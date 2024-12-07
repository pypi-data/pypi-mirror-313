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
重试
"""
from typing import Any
from functools import wraps
from time import sleep
import logging


def retry(
        max_retry_time: int = 3,
        interval: float = 0,
        condition: str = 'not_error',
        callback: Any = None,
        show: bool = False,
) -> Any:
    """
    一个装饰器

    :param max_retry_time: 重试次数上限
    :param interval: 重试间隔
    :param condition: 控制指令。not_error：执行如果没有报错就视为成功并终止重试。not_none：执行如果非空就视为成功并终止重试
    :param callback: 重试次数到上限后依然未成功时返回callback
    :param show: 输出细节信息
    :return: 被装饰的函数的返回值或callback

    >>> from random import randint
    >>> @retry(max_retry_time=100)
    ... def x():
    ...     t = randint(0, 1)
    ...     if t != 0:
    ...         raise ValueError
    ...     return t
    >>> x()
    0

    >>> from random import randint
    >>> @retry(max_retry_time=100, interval=0.01, condition='not_error not_none')
    ... def y():
    ...     t = randint(0, 1)
    ...     if t != 0:
    ...         return
    ...     return t
    >>> y()
    0
    """
    if max_retry_time < 0:
        max_retry_time = 0
    if interval < 0:
        interval = 0

    def retry_func(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            retry_time = 0
            result = callback

            while retry_time <= max_retry_time:
                catch_exception = False
                result_none = False
                try:
                    result = func(*args, **kwargs)
                    if result is None:
                        result_none = True
                except Exception as e:
                    if show:
                        print(e)
                    logging.warning(e)
                    catch_exception = True
                if show:
                    logging.warning('retry {} time {} result {}'.format(func.__name__, retry_time, result))
                    print('retry_time', retry_time, 'result', result)
                stop_retry = True
                if 'not_error' in condition and catch_exception:
                    stop_retry = False
                if 'not_none' in condition and result_none:
                    stop_retry = False
                if stop_retry:
                    break

                sleep(interval)
                retry_time += 1

            return result
        return decorator
    return retry_func


if __name__ == '__main__':
    import doctest

    doctest.testmod()
