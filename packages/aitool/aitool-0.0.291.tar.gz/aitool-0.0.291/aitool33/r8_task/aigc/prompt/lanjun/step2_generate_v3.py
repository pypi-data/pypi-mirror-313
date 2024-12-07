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
from random import sample, shuffle
from tqdm import tqdm

tokens = load_excel('./inputs_tokens_0105.xlsx', to_list=True)
rst = []
random_time = 5
use_meta = False   # 是否使用元素
for a, b, c, d in tokens:
    rule = '\"' + c + '，' + d + '\"'
    for _ in range(random_time):
        p = sample(prompt, 1)[0]
        res = []
        res.append(sample(restrain['r1'], 1)[0])
        res.append(sample(restrain['r2'], 1)[0])
        res.append(sample(restrain['r3'], 1)[0])
        res.append(sample(restrain['r4'], 1)[0])
        res_string = '，'.join([_ for _ in res if _ != ''])
        # TODO 无case
        case_string = '\n{}：\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}'.format('.输出格式', '', '', '', '', '')
        fp = p
        fp = fp.replace('【任务】', '离线反馈')
        # TODO 规则&主题 都使用rule，暂不使用topic
        fp = fp.replace('【规则】', rule)
        fp = fp.replace('【主题】', rule)
        fp = fp.replace('【约束】', res_string)
        fp = fp.replace('【例子】', case_string)
        fp = fp.replace('【N】', '10条')
        rst.append([a, b, c, d, fp])


shuffle(rst)
print('len', len(rst))
dump_pickle(rst, 'prompts_lanjun_0105.pkl')
dump_excel(rst, 'prompts_lanjun_0105.xlsx')
