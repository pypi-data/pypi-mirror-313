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
from aitool import load_excel, is_all_chinese, dump_excel, load_lines, char_sim
from random import shuffle
from tqdm import tqdm

data = load_excel('./rst_pre_check_1027.xlsx', to_list=True)
shuffle(data)
choose = []
rst = []

for line in tqdm(data):
    text = line[-1]
    is_sim = False
    for t in choose:
        sk = char_sim(text, t)
        if sk >= 0.8:
            print(text, t)
            is_sim = True
            break
    if not is_sim:
        rst.append(line)
        choose.append(text)
        if len(choose) % 500 == 0:
            print('choose', len(choose))
            dump_excel(rst, './rst_clean_sim_1027.xlsx')

dump_excel(rst, './rst_clean_sim_1027.xlsx')