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
from step1b_prompts_fine import prompt, task, idx2rule_l2, restrain
from random import sample, shuffle

rst = []
random_time = 100
ids = list(idx2rule_l2.keys())
for t in task:
    for p in prompt:
        for id in ids:
            rs = idx2rule_l2[id]
            for _ in range(random_time):
                rule = sample(rs, 1)[0]
                res = []
                if t == '离线反馈':
                    res.append(sample(restrain['r1'], 1)[0])
                elif t == '用户客服对话':
                    continue
                    res.append(sample(restrain['r0'], 1)[0])
                res.append(sample(restrain['r2'], 1)[0])
                res.append(sample(restrain['r3'], 1)[0])
                res.append(sample(restrain['r4'], 1)[0])
                res_string = '，'.join([_ for _ in res if _ != ''])
                # TODO 无case
                case_string = '\n{}：\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}'.format('输出格式', '', '', '', '', '')
                fp = p
                fp = fp.replace('【任务】', t)
                # TODO 规则&主题 都使用rule，暂不使用topic
                fp = fp.replace('【规则】', '\"{}\"'.format(rule))
                fp = fp.replace('【主题】', '\"{}\"'.format(rule))
                fp = fp.replace('【约束】', res_string)
                fp = fp.replace('【例子】', case_string)
                fp = fp.replace('【N】', '5条')
                rst.append([t, p, id, rule, res_string, case_string, fp])
shuffle(rst)
print('len', len(rst))
dump_pickle(rst, 'prompts_0913.pkl')
dump_excel(rst, 'prompts_0913.xlsx')
