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
计算向量的分布
"""
from typing import List
import numpy as np


def standard(v: List[float], precision=None) -> List[float]:
    """
    向量标准化（和为1）。如果输入是0向量，则输出0向量。

    :param v: 向量 List[float]
    :param precision: 结果的浮点位数
    :return: 标准化向量 List[float]

    >>> print(standard([0.5, 0.5, 0.5, 1.0]))
    [0.2, 0.2, 0.2, 0.4]
    """
    new_value = []
    sum_value = sum(v)
    if sum_value == 0:
        return v
    for vi in v:
        new_value.append(vi / sum_value)
    if precision is not None:
        new_value = list(map(lambda _: round(_, precision), new_value))
    return new_value


def normalize(v: List[float], precision=None) -> List[float]:
    """
    向量标准化（向量中的元素的绝对值最大为1）

    :param v: 向量
    :param precision: 结果的浮点位数
    :return: 单位向量

    >>> print(normalize([10, 0]))
    [1.0, 0.0]

    >>> print(normalize([-10, 0]))
    [-1.0, 0.0]

    >>> print(normalize([2, 1], precision=5))
    [0.89443, 0.44721]
    """
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    rst = (v / norm).tolist()
    if precision is not None:
        rst = list(map(lambda _: round(_, precision), rst))
    return rst


def cross_entropy(v1: List[float], v2: List[float]) -> np.float64:
    """
    计算交叉熵，需要确保每个值都是正数

    :param v1: 向量
    :param v2: 向量
    :return: 交叉熵

    >>> x = [1, 0, 0, 0]
    >>> y = [1, 0, 0, 0]
    >>> print('%.5f' % cross_entropy(x, y))
    0.00000

    >>> x = [0.5, 0.5, 0, 0]
    >>> y = [0.5, 0.5, 0, 0]
    >>> print('%.5f' % cross_entropy(x, y))
    0.69315

    >>> x = [0.25, 0.25, 0.25, 0.25]
    >>> y = [0.15, 0.30, 0.35, 0.20]
    >>> print('%.5f' % cross_entropy(x, y))
    1.38629

    >>> x = [0, 0, 0, 1]
    >>> y = [1, 0, 0, 0]
    >>> print('%.5f' % cross_entropy(x, y))
    16.11810
    """

    assert len(v1) == len(v2)
    a = np.array(v1)
    b = np.array(v2)
    # 添加一个微小值可以防止负无限大(np.log(0))的发生。
    delta = 1e-7
    rst = np.sum(b * np.log(a + delta))
    if rst < 0:
        rst = -rst
    return rst


def get_cos_similar(v1: list, v2: list) -> float:
    """
    计算cos相似度

    :param v1: 向量
    :param v2: 向量
    :return: cos相似度

    >>> x = [0.5, 0.5, 0, 0]
    >>> y = [0.5, 0.5, 0, 0]
    >>> print('%.5f' % get_cos_similar(x, y))
    1.00000

    >>> x = [0.25, 0.25, 0.25, 0.25]
    >>> y = [0.15, 0.30, 0.35, 0.20]
    >>> print('%.5f' % get_cos_similar(x, y))
    0.97673

    >>> x = [0, 0, 0, 1]
    >>> y = [1, 0, 0, 0]
    >>> print('%.5f' % get_cos_similar(x, y))
    0.50000
    """
    num = float(np.dot(v1, v2))  # 向量点乘
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)  # 求模长的乘积
    return 0.5 + 0.5 * (num / denom) if denom != 0 else 0


def scale_array(data: List[float], out_range=(-1, 1)) -> List[float]:
    """
    将数组中的每个元素变化到目标范围内

    :param data: 数组
    :param out_range: 目标范围
    :return: 数值被调整过的数组

    >>> print(scale_array([-2, 0, 2]))
    [-1.0, 0.0, 1.0]
    >>> print(scale_array([-3, -2, -1]))
    [-1.0, 0.0, 1.0]
    >>> print(scale_array([0, 2, 8, 4], out_range=(0, 100)))
    [0.0, 25.0, 100.0, 50.0]
    >>> print(scale_array([0, 2, 8, 4], out_range=(100, 0)))
    [100.0, 75.0, 0.0, 50.0]
    """
    data = np.array(data)
    domain = [np.min(data, axis=0), np.max(data, axis=0)]

    def _interp(_x):
        return out_range[0] * (1.0 - _x) + out_range[1] * _x

    def _uninterp(_x):
        if (domain[1] - domain[0]) != 0:
            b = domain[1] - domain[0]
        else:
            b = 1.0 / domain[1]
        return (_x - domain[0]) / b

    return _interp(_uninterp(data)).tolist()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
