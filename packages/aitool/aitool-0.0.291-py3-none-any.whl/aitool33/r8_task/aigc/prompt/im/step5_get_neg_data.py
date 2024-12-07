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

"""
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import load_csv, dump_excel, load_excel, term_similar, term_similar_bag
from random import randint, sample, shuffle
from collections import defaultdict
from tqdm import tqdm


def check_neg(text):
    if '{' in text:
        return False
    if '音乐需求' in text:
        return False
    if '搜索反馈' in text:
        return False
    if '\n' in text:
        return False
    if len(text) < 25:
        return False
    return True


if __name__ == '__main__':
    data_pos = load_excel('/Users/bytedance/PycharmProjects/aitool/aitool/r8_task/aigc/prompt/im/rst_im_0913.xlsx', to_list=True)
    data_neg = load_csv('/Users/bytedance/PycharmProjects/aitool/aitool/r8_task/aigc/prompt/im/data/281475006366508-AIGC对抗-离线反馈数据-查询5.csv', to_list=True)
    pos_num = 50
    neg_num = 200
    rst = []
    negs = []
    for line in tqdm(data_neg, 'load_neg'):
        text = line[0]
        if check_neg(text):
            negs.append(text)
    pos = defaultdict(list)
    rule2theme = defaultdict(set)
    for task, prompt, rule, theme, rest, hint, query, output in tqdm(data_pos, 'load pos'):
        pos[rule].append([output, term_similar(theme, output)])
        rule2theme[rule].add(theme)
    for rule, pos_cases in tqdm(pos.items(), 'rule'):
        pos_cases.sort(key=lambda _: _[1], reverse=True)
        neg_cases = sample(negs, min(neg_num * 10, len(negs)))
        neg_cases = [[c, term_similar_bag(rule2theme[rule], c)] for c in neg_cases]
        neg_cases.sort(key=lambda _: _[1], reverse=False)
        for c in pos_cases[:pos_num]:
            rst.append([rule, 'P', c[0]])
        for c in neg_cases[:neg_num]:
            rst.append([rule, 'N', c[0]])
    shuffle(rst)
    dump_excel(rst, 'extend_cases_9713.xlsx')
