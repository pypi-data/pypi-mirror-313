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
计算准确率等评分指标
"""
from typing import List, Any, Tuple, Dict
from collections import defaultdict


def apr(label: List, predict: List, precision: int = 100) -> Tuple[List[float], Dict[Any, List[float]]]:
    """
    计算 acc, precision, recall

    :param label: 真实标签
    :param predict: 模型预测的标签
    :param precision: 小数位
    :return: a, p, r, 细粒度apr

    >>> apr([1, 1, 1, 2, 2], [1, 2, 2, 2, 1], precision=3)
    ([0.25, 0.4, 0.4], {1: [0.25, 0.333, 0.5], 2: [0.25, 0.5, 0.333]})
    >>> apr([1, 1, 2, 2, 3, 3, 3, 3], [1, 2, 2, 1, 1, 2, 3, 4], precision=3)
    ([0.231, 0.375, 0.375], {1: [0.25, 0.5, 0.333], 2: [0.25, 0.5, 0.333], 3: [0.25, 0.25, 1.0]})
    """
    if len(label) != len(predict):
        raise ValueError('label和predict的数量应该一致')

    label_set = set()
    tp = defaultdict(int)
    tn = defaultdict(int)
    fp = defaultdict(int)
    tpc = 0
    tnc = 0
    fpc = 0
    for lb, pr in zip(label, predict):
        label_set.add(lb)
        if lb == pr:
            tp[lb] += 1
            tpc += 1
        else:
            tn[lb] += 1
            fp[pr] += 1
            tnc += 1
            fpc += 1
    a = round(tpc / (tpc + tnc + fpc), precision) if (tpc + tnc + fpc) > 0 else -1
    p = round(tpc / (tpc + tnc), precision) if (tpc + tnc) > 0 else -1
    r = round(tpc / (tpc + fpc), precision) if (tpc + fpc) > 0 else -1
    label_apr = {}
    for lb in label_set:
        al = round(tp[lb] / (tp[lb] + tn[lb] + fp[lb]), precision) if (tp[lb] + tn[lb] + fp[lb]) > 0 else -1
        pl = round(tp[lb] / (tp[lb] + tn[lb]), precision) if (tp[lb] + tn[lb]) > 0 else -1
        rl = round(tp[lb] / (tp[lb] + fp[lb]), precision) if (tp[lb] + fp[lb]) > 0 else -1
        label_apr[lb] = [al, pl, rl]
    return [a, p, r], label_apr


if __name__ == '__main__':
    import doctest

    doctest.testmod()
