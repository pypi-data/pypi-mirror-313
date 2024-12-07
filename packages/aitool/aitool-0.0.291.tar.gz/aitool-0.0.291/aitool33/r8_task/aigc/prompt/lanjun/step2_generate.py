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
from aitool import dump_pickle, dump_excel
from step1_prompts import prompt, task, idx2rule, restrain
from random import sample, shuffle
from tqdm import tqdm

rst = []
random_time = 1000
rids = list(idx2rule.keys())
use_meta = False   # 是否使用元素
for t in task:
    for rid in tqdm(rids, 'process'):
        rs = idx2rule[rid]
        for rule in rs:
            for _ in range(random_time):
                p = sample(prompt, 1)[0]  
                res = []
                if use_meta:
                    r_cs = sample(restrain['场所'], 1)[0]
                    r_cs = '涉及' + r_cs if r_cs != '' else ''
                    r_dz = sample(restrain['动作'], 1)[0]
                    r_dz = '涉及' + r_dz if r_dz != '' else ''
                    r_dx = sample(restrain['对象'], 1)[0]
                    r_dx = '涉及' + r_dx if r_dx != '' else ''
                    r_jg = sample(restrain['结果'], 1)[0]
                    r_jg = '涉及' + r_jg if r_cs != '' else ''
                    res.append(r_cs)
                    res.append(r_dz)
                    res.append(r_dx)
                    res.append(r_jg)
                res.append(sample(restrain['r1'], 1)[0])
                res.append(sample(restrain['r2'], 1)[0])
                res.append(sample(restrain['r3'], 1)[0])
                res.append(sample(restrain['r4'], 1)[0])
                res_string = '，'.join([_ for _ in res if _ != ''])
                # TODO 无case
                case_string = '\n{}：\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}'.format('.输出格式', '', '', '', '', '')
                fp = p
                fp = fp.replace('【任务】', t)
                # TODO 规则&主题 都使用rule，暂不使用topic
                fp = fp.replace('【规则】', '\"{}\"'.format(rid.replace('未授权的自动行为-','')))
                if '，内容必须涉及' in rule:
                    pos = rule.find('，内容必须涉及')
                    rule_new = '\"{}\"'.format(rule[:pos]) + rule[pos:]
                    fp = fp.replace('【主题】', rule_new)
                else:
                    fp = fp.replace('【主题】', '\"{}\"'.format(rule))
                fp = fp.replace('【约束】', res_string)
                fp = fp.replace('【例子】', case_string)
                fp = fp.replace('【N】', '10条')
                rst.append([t, p, rid, rule, res_string, case_string, fp])


shuffle(rst)
print('len', len(rst))
dump_pickle(rst, 'prompts_lanjun_1120.pkl')
dump_excel(rst, 'prompts_lanjun_1120.xlsx')
