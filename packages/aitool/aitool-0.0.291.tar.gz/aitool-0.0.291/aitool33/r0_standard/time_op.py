# -*- coding: UTF-8 -*-
# @Time    : 2021/3/10
# @Author  : xiangyuejia@qq.com
# Apache License
# Copyright©2020-2021 xiangyuejia@qq.com All Rights Reserved
"""
监控函数执行时间
"""
from functools import wraps
from typing import Union, Optional, Any, NoReturn
from time import sleep
import time
import sys
import threading
from logging import Logger


def exe_time(
        print_time: bool = False,
        print_key: Optional[str] = None,
        detail: bool = False,
        get_time: bool = False,
        logger: Logger = None,
) -> Union[Any]:
    """
    计算函数执行时间的装饰器

    :param print_time: 是否打印执行时间
    :param print_key: 用户自定义的bool类型参数名，用于控制是否打印执行时间。
    :param detail: 额外打印开始和结束的时间点
    :param get_time: 返回值是否附带执行时间
    :param logger: 日志logger.Logger
    :return: 被修饰的函数的返回值, [执行时间]

    >>> @exe_time()
    ... def demo0():
    ...     # 默认情况下exe_time无打印
    ...     pass
    >>> demo0()

    >>> @exe_time(print_time=True)
    ... def demo1():
    ...     # 打印执行时间/秒
    ...     pass
    >>> demo1() # doctest: +ELLIPSIS
    @...s taken for {demo1}

    >>> @exe_time(print_time=True)
    ... def demo2():
    ...     # 打印执行时间/秒
    ...     print('demo2')
    >>> demo2() # doctest: +ELLIPSIS
    demo2
    @...s taken for {demo2}

    >>> @exe_time(detail=True)
    ... def demo3():
    ...     # 打印被装饰函数开始和结束的时间点
    ...     print('demo3')
    >>> demo3() # doctest: +ELLIPSIS
    @..., {demo3} start
    demo3
    @..., {demo3} finish

    >>> @exe_time(get_time=True)
    ... def demo4():
    ...     # 返回值的最后额外附加执行时间
    ...     return 'demo4'
    >>> print(demo4()) # doctest: +ELLIPSIS
    ('demo4', ...)

    >>> @exe_time(print_time=True, print_key='show')
    ... def demo5(show=False):
    ...     # 通过print_key指定的show来控制是否打印执行时间
    ...     # 以便和被修饰函数用统一的变量控制打印状态
    ...     if show:
    ...         print('demo5')
    >>> demo5(show=True) # doctest: +ELLIPSIS
    demo5
    @...s taken for {demo5}
    >>> demo5(show=False)
    """
    def wrapper(func):
        @wraps(func)
        def decorate(*args, **kw):
            t0 = time.time()
            if detail:
                print('@%s, {%s} start' % (time.strftime('%X', time.localtime()), func.__name__))
                if logger is not None:
                    logger.info('@%s, {%s} start' % (time.strftime('%X', time.localtime()), func.__name__))
            back = func(*args, **kw)
            if detail:
                print('@%s, {%s} finish' % (time.strftime('%X', time.localtime()), func.__name__))
                if logger is not None:
                    logger.info('@%s, {%s} finish' % (time.strftime('%X', time.localtime()), func.__name__))
            time_dif = time.time() - t0
            # print_key设置后，会依据其值来修改print_time的值
            # TODO 默认值取不到，即必须在调用函数时指定参数后才能取到
            do_print = print_time
            if print_key is not None:
                if isinstance(print_key, str) and print_key in kw and isinstance(kw[print_key], bool):
                    do_print = kw[print_key]
            if do_print:
                print('@%.3fs taken for {%s}' % (time_dif, func.__name__))
                if logger is not None:
                    logger.info('@%.3fs taken for {%s}' % (time_dif, func.__name__))
            if get_time:
                return back, time_dif
            return back
        return decorate
    return wrapper


class KThread(threading.Thread):
    """
    对threading.Thread封装，额外添加killed属性来控制
    """
    def __init__(self, *args, **kwargs) -> NoReturn:
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self) -> NoReturn:
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self) -> NoReturn:
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg) -> NoReturn:
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg) -> NoReturn:
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self) -> NoReturn:
        self.killed = True


def timeout(seconds: float, callback: Any):
    """
    若被装饰的方法在指定的时间内未返回，会提前终止，并返回callback

    :param seconds: 超时时长（秒）
    :param callback: 超时时的返回值
    :return:

    >>> @timeout(2, None)  # 限时 2 秒超时
    ... def connect(_time):  # 要执行的函数
    ...     sleep(_time)  # 函数执行时间，写大于2的值，可测试超时
    ...     print('Finished without timeout.')
    ...     return 'success'
    >>> x = connect(1)
    Finished without timeout.
    >>> print(x)
    success
    >>> y = connect(2.5)
    >>> print(y)
    None
    """
    def timeout_func(func):
        def _new_func(target_func, result, target_func_args, target_func_kwargs):
            result.append(target_func(*target_func_args, **target_func_kwargs))

        def decorate(*args, **kwargs):
            result = []
            new_kwargs = {
                'target_func': func,
                'result': result,
                'target_func_args': args,
                'target_func_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.is_alive()
            thd.kill()  # kill the child thread
            if alive:
                try:
                    pass
                finally:
                    return callback
            else:
                if len(result) > 0:
                    return result[0]
                return
        decorate.__name__ = func.__name__
        decorate.__doc__ = func.__doc__
        return decorate
    return timeout_func


def format_time(_time: Union[str, int]):
    """
    将秒时间格式转化为年月日时分秒格式

    :param _time: 秒时间
    :return: 年月日时分秒格式

    >>> format_time('1698017090')
    '2023-10-23 07:24:50'
    """
    _time = int(_time)
    time_array = time.localtime(_time)
    other_style_time = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
    return other_style_time


def timestamp(style=None):
    """
    获取现在的时间

    :param style: 时间格式
    :return: 现在的时间

    >>> timestamp()  # doctest: +SKIP
    '2023_12_18_18:9:45'
    >>> timestamp(style='day')  # doctest: +SKIP
    '2023_12_18'
    >>> timestamp(style='hour')  # doctest: +SKIP
    '2023_12_18_18'
    >>> timestamp(style='min')  # doctest: +SKIP
    '2023_12_18_18_12'
    >>> timestamp(style='sec')  # doctest: +SKIP
    '2023_12_18_18_12_10'
    """
    _t = time.localtime(time.time())
    if style == 'day':
        describe = '{}_{}_{}'.format(_t.tm_year, _t.tm_mon, _t.tm_mday)
    elif style == 'hour':
        describe = '{}_{}_{}_{}'.format(_t.tm_year, _t.tm_mon, _t.tm_mday, _t.tm_hour)
    elif style == 'min':
        describe = '{}_{}_{}_{}_{}'.format(_t.tm_year, _t.tm_mon, _t.tm_mday, _t.tm_hour, _t.tm_min)
    elif style == 'sec':
        describe = '{}_{}_{}_{}_{}_{}'.format(_t.tm_year, _t.tm_mon, _t.tm_mday, _t.tm_hour, _t.tm_min, _t.tm_sec)
    elif style is None:
        describe = '{}'.format(time.asctime(_t))
        describe = describe.replace('  ', '_')
        describe = describe.replace(' ', '_')
    else:
        raise ValueError('style: {}'.format(style))
    return describe


def get_lastday_timestamp():
    """
    获取24小时前的日期

    >>> get_lastday_timestamp()
    '20231217'
    """
    _t = time.localtime(time.time() - 86400)
    mon = str(_t.tm_mon)
    day = str(_t.tm_mday)
    if len(mon) == 1:
        mon = '0' + mon
    if len(day) == 1:
        day = '0' + day
    print(_t.tm_mon)
    rst = '{}{}{}'.format(_t.tm_year, mon, day)
    return rst


if __name__ == '__main__':
    import doctest

    doctest.testmod()
