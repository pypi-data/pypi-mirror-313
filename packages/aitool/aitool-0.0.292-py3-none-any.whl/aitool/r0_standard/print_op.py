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
打印工具
"""
from typing import NoReturn


def print_color(text: str, special: str = 'none', letter: str = 'red', background: str = 'none') -> NoReturn:
    """
    打印有颜色的命令行输出

    :param text: 要输出的文本
    :param special: 特效
    :param letter: 文字颜色
    :param background: 背景色
    :return: None

    >>> print_color('case', special='none', letter='red', background='none')
    \033[0;31mcase\033[0m
    >>> print_color('case', special='underline', letter='red', background='none')
    \033[4;31mcase\033[0m
    >>> print_color('case', special='none', letter='red', background='yellow')
    \033[0;31;43mcase\033[0m
    >>> print_color('case', special='flicker', letter='red', background='green')
    \033[5;31;42mcase\033[0m
    """
    # 特效
    specials = {
        'none': '0',        # 无
        'highlight': '1',   # 高亮度
        'underline': '4',   # 下划线
        'flicker': '5',     # 闪烁
        'reaction': '7',    # 反显
        'blanking': '8',    # 消隐
    }
    # 文字颜色
    letters = {
        'none': ';0',       # 默认
        'black': ';30',     # 黑色
        'red': ';31',       # 红色
        'green': ';32',     # 绿色
        'yellow': ';33',    # 黄色
        'blue': ';34',      # 蓝色
        'amaranth': ';35',  # 紫红色
        'cyan': ';36',      # 青蓝色
        'grey': ';37',      # 灰色
    }
    # 背景色
    backgrounds = {
        'none': '',         # 默认
        'black': ';40',     # 黑色
        'red': ';41',       # 红色
        'green': ';42',     # 绿色
        'yellow': ';43',    # 黄色
        'blue': ';44',      # 蓝色
        'amaranth': ';45',  # 紫红色
        'cyan': ';46',      # 青蓝色
        'grey': ';47',      # 灰色
    }
    print("\033[{}{}{}m{}\033[0m".format(specials[special], letters[letter], backgrounds[background], text))


def print_red(text: str) -> NoReturn:
    """
    输出红色的文字

    :param text:
    :return: None

    >>> print_red('red')
    \033[0;31mred\033[0m
    """
    print_color(text, letter='red')


def print_green(text: str) -> NoReturn:
    """
    输出绿色的文字

    :param text:
    :return: None

    >>> print_green('green')
    \033[0;32mgreen\033[0m
    """
    print_color(text, letter='green')


def print_yellow(text: str) -> NoReturn:
    """
    输出黄色的文字

    :param text:
    :return: None

    >>> print_yellow('yellow')
    \033[0;33myellow\033[0m
    """
    print_color(text, letter='yellow')


def print_blue(text: str) -> NoReturn:
    """
    输出蓝色的文字

    :param text:
    :return: None

    >>> print_blue('blue')
    \033[0;34mblue\033[0m
    """
    print_color(text, letter='blue')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
