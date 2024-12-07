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
from step1_prompts import prompt, idx2theme, idx2action, idx2restrain
from random import sample, shuffle
"""需要写【N】【动作】【主题】的话。【限制】。【例子】""",
rst = []
random_time = 1000
idxs = list(idx2theme.keys())
for idx in idxs:
    for _ in range(random_time):
        p = sample(prompt, 1)[0]
        theme = sample(idx2theme[idx], 1)[0]
        action = sample(idx2action[idx], 1)[0]
        res = []
        res.append(sample(idx2restrain[idx], 1)[0])
        res.append(sample(idx2restrain['r1'], 1)[0])
        res_string = '，'.join([_ for _ in res if _ != ''])
        case_string = '\n{}：\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}'.format('输出格式', '', '', '', '', '')
        fp = p
        fp = fp.replace('【动作】', '{}'.format(action))
        fp = fp.replace('【主题】', '{}'.format(theme))
        fp = fp.replace('【约束】', res_string)
        fp = fp.replace('【例子】', case_string)
        fp = fp.replace('【N】', '5条')
        rst.append([idx, p, theme, action, res_string, case_string, fp])
shuffle(rst)
print('len', len(rst))
dump_pickle(rst, 'prompts_1008.pkl')
dump_excel(rst, 'prompts_1008.xlsx')
