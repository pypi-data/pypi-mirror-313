# -*- coding: UTF-8 -*-
# Copyright©2022 xiangyuejia@qq.com All Rights Reserved
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
正则工具
"""
from typing import List, NoReturn, Iterable
import re
from re import Pattern
from aitool import Cache


class RE:
    """
    对re的封装，用于缓存pattern编译后的结果，使多次执行同一个pattern时无需重复编译
    """
    pattern2compile = Cache(size=10000)

    @classmethod
    def get_compile(cls, pattern: str) -> Pattern:
        """
        获取一个pattern的re.compile编译结果。仅在第一次获取时计算，之后直接返回第一次的结果。
        * 存储的pattern编译结果数量有上限，如果达到上限，会随机遗忘之前存储的一个。
        * 被遗忘的pattern编译结果被再次调用时，需要重新进行计算。
        * 可以通过re_set_capacity(10000)来设置存储数量上限为10000

        :param pattern: 文本匹配模式
        :return: pattern的re.compile编译结果
        """
        if pattern not in cls.pattern2compile:
            the_compile = re.compile(pattern)
            cls.pattern2compile[pattern] = the_compile
        return cls.pattern2compile[pattern]

    @classmethod
    def set_capacity(cls, capacity: int) -> NoReturn:
        """
        设置存储的pattern编译结果数量有上限

        :param capacity: 存储的数量上限
        :return: None
        """
        assert type(capacity) == int
        cls.pattern2compile.set_size(capacity)

    @classmethod
    def gat_capacity(cls) -> int:
        """
        获取存储pattern编译结果数量的上限

        :return: 存储数量上限
        """
        return cls.pattern2compile.get_size()

    @classmethod
    def split(cls, pattern: str, text: str) -> List[str]:
        """
        依据pattern切分text

        :param pattern: 用于匹配字符串的pattern
        :param text: 被切分的字符串
        :return: 切分出的字符串列表

        >>> RE.split('[-028]', '123-456-789')
        ['1', '3', '456', '7', '9']
        """
        cpl = cls.get_compile(pattern)
        return re.split(cpl, text)

    @classmethod
    def sub(cls, pattern: str, new: str, text: str) -> str:
        """
        将text里pattern匹配到的字符串替换为new

        :param pattern: 用于匹配字符串的pattern
        :param new: 新字符串
        :param text: 被替换的字符串
        :return: 替换后的字符串

        >>> RE.sub('[135]', '**', '123456')
        '**2**4**6'
        """
        cpl = cls.get_compile(pattern)
        return re.sub(cpl, new, text)


re_set_capacity = RE.set_capacity
re_split = RE.split
re_sub = RE.sub


def split_char(chars: str, text: str) -> List[str]:
    """
    用1个或多个分割符切分字符串

    :param chars: 用于分割的字符串，其中每个字符都被视为分隔符
    :param text: 被切分的字符串
    :return: 切分后的字符串数组

    >>> split_char('-', '123-456-789')
    ['123', '456', '789']
    >>> split_char('-028', '123-456-789')
    ['1', '3', '456', '7', '9']
    """
    return re_split(r'[{}]'.format(chars), text)


def split_punctuation(text: str, punctuation: str = None, level: str = 'typical') -> List[str]:
    """
    切分所有标点

    :param text: 被切分的文本
    :param punctuation: 标点
    :param level: 取值为'typical' 或 'common'，仅在 punctuation == None 时生效
    :return: 切分后的字符串数组

    >>> split_punctuation('你好，吃了吗？没有吃')
    ['你好', '吃了吗', '没有吃']
    >>> split_punctuation('12.3-a')
    ['12', '3', 'a']
    >>> split_punctuation('12.3-a', punctuation='.:')
    ['12', '3-a']
    """
    if punctuation is None:
        # .:-前需要有\在正则中进行转意
        if level == 'typical':
            punctuation = r',，\.。、;；?？\:：!！@#\-—'
        elif level == 'common':
            punctuation = r',\.;`\[\]<>\?:"\{\}\~!@#\$%\^&\(\)\-=\_\+，。、；‘’【】·！ …（）'
    return [_ for _ in split_char(punctuation, text) if len(_) > 0]


def replace_text(text: str, old: Iterable, new: str, method: str = 'builtin') -> str:
    """
    将1个或多个旧字符串替换为新字符串

    :param text: 被替换的文本
    :param old: 旧字符串
    :param new: 新字符串
    :param method: 方法支持 'builtin', 're-sub' 或 'generate'。默认的'builtin'方法最佳，其他方法限制较多。
    :return: 替换后的文本

    >>> replace_text('123456', ['12', '4'], '**')
    '**3**56'
    >>> replace_text('123456', '135', '**')
    '**2**4**6'
    >>> replace_text('123456', '135', '**', method='re-sub')
    '**2**4**6'
    >>> replace_text('123456', {'1', '3', '5'}, '**', method='generate')
    '**2**4**6'
    """
    if method == 'builtin':
        for o in old:
            text = text.replace(o, new)
        return text
    elif method == 're-sub':
        if type(old) != str:
            raise ValueError('re-sub方法的old参数仅支持str')
        return re_sub(r'[{}]'.format(old), new, text)
    elif method == 'generate':
        if type(old) not in (str, set):
            raise ValueError('generate方法的old参数仅支持str或dict')
        if type(old) != set:
            old_set = set(old)
        else:
            old_set = old
        result = ''
        for char in text:
            if char not in old_set:
                result += char
            else:
                result += new
        return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()
