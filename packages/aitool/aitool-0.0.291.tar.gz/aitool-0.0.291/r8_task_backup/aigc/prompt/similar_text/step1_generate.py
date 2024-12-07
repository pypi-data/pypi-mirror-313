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
from random import sample, shuffle
from tqdm import tqdm

data = load_excel('./截止20231029的线上case.xlsx', to_list=True)
sent_old = set()
data_old = load_excel('./rst_similar_1113.xlsx', to_list=True)
for line in data_old:
    sent_old.add(line[0])

rst = []
for line in data:
    if line[0] in sent_old:
        continue
    for _ in range(1000):
        core = line[0].replace('\'', ' ').replace('\"', ' ').replace('\n', ' ')
        text = '请仿照示例反馈"{}"写5个类似的关于抖音的反馈。要求模仿用户说的话，偏口语化，每条反馈和示例的字数差不多。输出格式1. \n2. \n3. \n4. \n5. \n'.format(core)
        rst.append(line + [text])

print('len', len(rst))
shuffle(rst)
dump_pickle(rst, 'prompts_similar_1117.pkl')
dump_excel(rst, 'prompts_similar_1117.xlsx')
