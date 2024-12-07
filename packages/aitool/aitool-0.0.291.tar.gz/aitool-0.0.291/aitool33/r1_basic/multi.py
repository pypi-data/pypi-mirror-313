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
共提供3种实现多进程的方式 pool_map，pool_starmap，multi_map。

- 修改**1行**代码将顺序执行改造为并行执行。
- 三种方法都**按序输出**，多次运行获得的结果**顺序是一致**的。
- 三种方法都基于multiprocess库，而非multiprocessing库。因为multiprocessing有[设计缺陷](https://bugs.python.org/issue25053)。）
- 三种方式是几乎等效的，在参数不复杂的情况下推荐使用pool_map
- 详细评测见[评估文档](./multi.md)

**NOTE**
- 被调用函数最好只有1个参数，即，将原本的输入参数用一个list或dict包装一下
- 是进程级并行，会复制整个进程，最好优化一下进程里内存消耗。
- python的线程级并行并没有实际用到多核，所以一下均使用的进程级并行
"""
import functools
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from os import cpu_count
from random import random
from time import sleep, time
from typing import Iterator, Callable, NoReturn, Tuple, List
import multiprocess as mp


def pool_map(
        func: Callable,
        conditions: Iterable,
        processes: int = cpu_count(),
        **kwargs,
) -> Iterable:
    """
    对multiprocess.Pool().map方法做封装

    :param func: 被多进程执行的函数
    :param conditions: 函数参数
    :param processes: 进程数
    :param kwargs: 其他multiprocess.Pool()的参数
    :return: 函数运行结果

    >>> def toy(x, y=1):
    ...     sleep(random())
    ...     return x, y
    >>> list(pool_map(toy, range(3)))
    [(0, 1), (1, 1), (2, 1)]

    >>> def toy(x, y):
    ...     sleep(random())
    ...     return x, y
    >>> list(pool_map(toy, zip(range(3),range(3))))
    Traceback (most recent call last):
        ...
    TypeError: toy() missing 1 required positional argument: 'y'
    """
    with mp.Pool(
            processes=processes,
            **kwargs
    ) as p:
        for result in p.map(func, conditions):
            yield result


def pool_starmap(
        func: Callable,
        conditions: Iterable,
        processes: int = cpu_count(),
        **kwargs,
) -> Iterable:
    """
    对multiprocess.Pool().starmap方法做封装

    :param func: 被多进程执行的函数
    :param conditions: 函数参数
    :param processes: 进程数
    :param kwargs: 其他multiprocess.Pool()的参数
    :return: 函数运行结果

    >>> def toy(x, y=1):
    ...     sleep(random())
    ...     return x, y
    >>> list(pool_starmap(toy, [[0, 1], [1, 2], [2, 3]]))
    [(0, 1), (1, 2), (2, 3)]

    >>> def toy(x, y):
    ...     sleep(random())
    ...     return x, y
    >>> list(pool_starmap(toy, [[0, 1], [1, 1], [2, 2]]))
    [(0, 1), (1, 1), (2, 2)]
    """
    # 基于pool.starmap实现
    with mp.Pool(
            processes=processes,
            **kwargs,
    ) as p:
        for result in p.starmap(func, conditions):
            yield result


def multi_map(
        func: Callable,
        conditions: Iterable,
        processes: int = cpu_count(),
        time_step: float = 0.01,
        ordered: bool = True,
        timeout: float = None,
) -> Iterable:
    """
    基于一组参数并行计算func

    :param func: 函数
    :param conditions: 一组参数
    :param processes: 同时启动的进程数量上限，默认为cpu核数
    :param time_step: 主进程每间隔time_step秒读取一次数据
    :param ordered: 是否按functions的顺序输出结果。ordered=True时，各function会等待排它前面的所有function输出后才输出。
    :param timeout: 最大运行时长，设置为None时表示不做时长限制
    :return: functions里各个函数的返回结果

    >>> def toy(x, y=1):
    ...     sleep(random())
    ...     return x, y
    >>> list(multi_map(toy, range(3)))
    [(0, 1), (1, 1), (2, 1)]
    """
    functions = list(get_functions(func, conditions))
    for result in multi(
            functions,
            processes=processes,
            time_step=time_step,
            ordered=ordered,
            timeout=timeout,
    ):
        yield result


def get_functions(_func: Callable, _iter: Iterable) -> Iterable:
    """
    依据一组参数和基础函数，生成一组对应的新函数。
    由于函数的参数结构是：*args, **keywords
    为了方便用户使用，将如下进行参数解析：
    * 如果参数是None，将视为不设置参数
    * 如果参数是不可迭代类型，且不是None，就会被当做*args处理
    * 如果参数是dict类型，就会被当做**keywords处理
    * 如果参数是list类型，就会被当做*arg处理
    * 如果参数是长度为2的tuple类型，就会被当做(*args, **keywords)处理
    * 如果是其他情况会报错

    :param _func: 基础函数
    :param _iter: 一组参数
    :return: 一组对应的新函数

    >>> def toy(x, y=1):
    ...     sleep(random())
    ...     return x, y
    >>> for function in get_functions(toy, range(3)):
    ...     print(function())
    (0, 1)
    (1, 1)
    (2, 1)
    >>> for function in get_functions(toy, [1, [2, 3], {'x': 4}, {'x': 6, 'y': 7}]):
    ...     print(function())
    (1, 1)
    (2, 3)
    (4, 1)
    (6, 7)
    """
    for condition in _iter:
        if condition is None:
            yield _func
        elif not isinstance(condition, Iterable):
            yield functools.partial(_func, condition)
        elif type(condition) == dict:
            yield functools.partial(_func, **condition)
        elif type(condition) == list:
            yield functools.partial(_func, *condition)
        elif type(condition) == tuple and len(condition) == 2:
            args, keywords = condition
            yield functools.partial(_func, *args, **keywords)
        else:
            # TODO 对condition的解析进行优化，使得能兼容更多数据格式
            raise ValueError(
                """
                Error: 不能识别的参数格式

                由于函数的参数结构是：*args, **keywords
                为了方便用户使用，将如下进行参数解析：
                * 如果参数是不可迭代类型（例如string、int），就会被当做*args处理
                * 如果参数是dict类型，就会被当做**keywords处理
                * 如果参数是list类型，就会被当做*arg处理
                * 如果参数是长度为2的tuple类型，就会被当做(*args, **keywords)处理
                * 如果是其他情况会报错
                """)


def multi(
        functions: Iterator[Callable],
        processes: int = cpu_count(),
        time_step: float = 0.01,
        ordered: bool = True,
        timeout: float = None,
) -> Iterable:
    """
    对输入的多个函数进行多进程并发运行，使用mp.Manager().Queue()做跨进程的进度管理，用apply_async做并发

    :param functions: 函数的列表或迭代器
    :param processes: 同时启动的进程数量上限，默认为cpu核数
    :param time_step: 主进程每间隔time_step秒读取一次数据
    :param ordered: 是否按functions的顺序输出结果。ordered=True时，各function会等待排它前面的所有function输出后才输出。
    :param timeout: 最大运行时长，设置为None时表示不做时长限制
    :return: functions里各个函数的返回结果

    >>> def toy_1(x=1, y=2):
    ...     sleep(0.4)
    ...     return x, y
    >>> def toy_2(x=3, y=4):
    ...     sleep(0.1)
    ...     return x, y
    >>> list(multi([toy_1, toy_2]))
    [(1, 2), (3, 4)]
    >>> list(multi([toy_1, toy_2], ordered=False))
    [(3, 4), (1, 2)]

    >>> def toy(x, y=1):
    ...     sleep(random())
    ...     return x, y
    >>> f = list(get_functions(toy, [1, [2, 3], {'x': 4}, {'x': 6, 'y': 7}]))
    >>> list(multi(f))
    [(1, 1), (2, 3), (4, 1), (6, 7)]

    >>> def toy(x, y=1):
    ...     return x, y
    >>> def bauble(x=1, y=2):
    ...     return x + y
    >>> toy_functions = list(get_functions(toy, [1, [2, 3], {'x': 4}, {'x': 6, 'y': 7}]))
    >>> bauble_functions = list(get_functions(bauble, [None, -2, [-3], [6, -1], {'y': 4}]))
    >>> list(multi(toy_functions + bauble_functions))
    [(1, 1), (2, 3), (4, 1), (6, 7), 3, 0, -1, 5, 5]
    """

    def _return_2_queue(_function: Callable, _index: int, _queue) -> NoReturn:
        """
        对function做封装，将function的执行结果储存到管道queue里。

        :param _function: 被封装的函数
        :param _index: function的序号
        :param _queue: 管道，用于和父进程通信
        :return: NoReturn
        """
        _result = _function()
        _queue.put((_index, _result))

    if processes < 1:
        raise ValueError('processes should bigger than 0')
    begin_time = time()

    def print_error(value):
        print("线程池出错: ", value)

    queue = mp.Manager().Queue()
    pool = mp.Pool(processes=processes)
    for index, function in enumerate(functions):
        pool.apply_async(_return_2_queue, args=(function, index, queue,), error_callback=print_error)
    pool.close()

    # ordered == True时用于控制输出顺序
    ordered_results = dict()
    ordered_requirement = 0

    # 每time_step秒进行一次巡察
    while True:
        # TODO
        # 有更好的方式监控queue并及时返回结果吗？
        # 目前用的yield很蠢，如果不及时消费，所有子进程都会阻塞
        # 想设计一个负责取值的子进程持续监控queue并传值给主进程，
        # 但是主进程的消费和取值的子进程好像可能导致读写冲突，不知道加个锁是否能解决这个问题，
        # 以及不确定这样设计后yield是否依然会阻塞所有子进程
        sleep(time_step)
        while not queue.empty():
            q_index, q_result = queue.get(False)
            if not ordered:
                yield q_result
            else:
                # TODO
                # ordered=True 时会对返回值做存储，
                # 在进程很多且运行时间很不均衡时，可能导致内存占用量不断增多，导致OutOfMemory
                ordered_results[q_index] = q_result

        while ordered and ordered_requirement in ordered_results:
            yield ordered_results.pop(ordered_requirement)
            ordered_requirement += 1

        # TODO
        # 怎么判断pool里所有进程都运行完了?
        # 考虑过pool.join()，它是阻塞的不符合需求。
        # 目前的实现有提前终止的风险，
        # 目前的实现是：判断在pool里的processes个进程是否都结束了，如果都结束就终止，
        # 但，如果由于其他原因导致还没执行的processes没有即使进入pool，就会误杀
        pool_finished = True
        for app in pool._pool:
            if app.exitcode != 0:
                pool_finished = False
                break
        if pool_finished:
            break
        if timeout and time() - begin_time > timeout:
            print('Warning: pool timeout')
            break

    # TODO
    # 不确定目前的逻辑是否会遗漏数据未返回
    if len(ordered_results):
        print('Warning: ordered_results 数据没有取完')
    if not queue.empty():
        print('Warning: queue 数据没有取完')
    pool.terminate()


def thread_pool(func: Callable, args: Iterable, queue: Queue = None, max_workers: int = 4) -> Tuple[List, Queue]:
    """
    多线程执行函数

    :param func: 被执行函数，函数参数最好只有一个param，如果有多个参数可以用list或dict封装成一个param
    :param args: 被执行函数的参数
    :param queue: 用于存下执行结果的Queue，本函数内不会消费此Queue，以便外部调用
    :param max_workers: 并发数量
    :return: (list格式的顺序结果, Queue结果队列)。注意，list格式的结果需要所有数据执行完后才能输出。
    Queue结果无序，能一边跑一边输出，通过传入Queue可以提高并行能力。

    >>> from random import random
    >>> from time import sleep
    >>> def f(param):
    ...     sleep(random())
    ...     return param
    >>> r, que = thread_pool(f, range(6), max_workers=2)
    >>> r
    [0, 1, 2, 3, 4, 5]
    >>> while not que.empty(): que.get()  # doctest: +SKIP
    ...

    """
    if queue is None:
        queue = Queue()

    def _func_queue(_func) -> Callable:
        def _func_new(*_args, **_kwargs):
            _rst = _func(*_args, **_kwargs)
            queue.put(_rst)
            return _rst

        return _func_new

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(_func_queue(func), args)
    return [p for p in results], queue


if __name__ == '__main__':
    import doctest

    doctest.testmod()
