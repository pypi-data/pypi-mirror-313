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
随机工具
"""
from typing import List
from random import random, randint
import base64


def weight_random(weight: List[float]) -> int:
    """
    输入一个被抽中概率的数组，代表每个下标被抽中的概率，返回被抽中的下标

    :param weight: 被抽中概率的数组
    :return: 被抽中的下标

    >>> weight_random([0.1, 0.3, 0.2, 0.4])     # doctest: +SKIP
    """
    if sum(weight) < 1 - 1e-3 or sum(weight) > 1 + 1e-3:
        raise ValueError('输入的概率之和应为1')
    choose = random()
    his = 0
    for i in range(len(weight)):
        his += weight[i]
        if his >= choose:
            return i


def random_base64(length: int = 64, no_symbol=True, seed: str = None) -> str:
    """
    生成一个base64格式的随机字符串

    :param length: 字符串长度
    :param no_symbol: 是否将字符串中的符号（-和_）替换为A
    :param seed: 种子
    :return: 字符串

    >>> print('Random64: ', random_base64(length=16))  # doctest: +SKIP
    Random64:  Ipx1BV0fAMwcFCCB
    >>> print('Random64: ', random_base64(seed='ABCDE'))
    Random64:  QUJDREUA
    """
    if seed is None:
        seed = randint(0, 2 ** (8 * length // 4 * 3)).to_bytes(length // 4 * 3, "little")
    else:
        seed = str.encode(seed)
    text = str(base64.urlsafe_b64encode(seed), "utf-8")
    if no_symbol:
        text = text.replace('-', 'A')
        text = text.replace('_', 'A')
        text = text.replace('=', 'A')
    return text


if __name__ == '__main__':
    import doctest

    doctest.testmod()
