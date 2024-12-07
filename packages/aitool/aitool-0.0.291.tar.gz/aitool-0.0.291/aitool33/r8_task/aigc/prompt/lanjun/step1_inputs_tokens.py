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
from aitool import dump_pickle, dump_excel, load_excel
from step1_prompts import prompt, task, idx2rule, restrain
from random import sample, shuffle, random
from tqdm import tqdm
from collections import defaultdict


data = load_excel('./[01_05] 涉政样本生成.xlsx', to_list=True)
tyc = load_excel('./同义词.xlsx', to_list=True)
tyd = defaultdict(list)
for line in tyc:
    key = line[0]
    for ty in line:     # 包含本身
        if len(ty) >= 1:
            tyd[key].append(ty)


def set_ty(text):
    for k in tyd:
        if k in text:
            p = sample(tyd[k], 1)[0]
            text = text.replace(k, p)
    return text


rst = []
random_time = 5000
for line in data:
    op, ph = line[0], line[1]
    if len(op) <= 1 or len(ph) <= 1:
        continue
    for _ in range(random_time):
        opr = set_ty(op)
        phr = set_ty(ph)
        rst.append([op, ph, opr, phr])

shuffle(rst)
print('len', len(rst))
rst = [['操作', '现象', '操作（同义词替换）', '现象（同义词替换）']] + rst
dump_pickle(rst, 'inputs_tokens_0105.pkl')
dump_excel(rst, 'inputs_tokens_0105.xlsx')
