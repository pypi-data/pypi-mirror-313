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
from aitool import load_json, load_excel, get_keyword, dump_json, dump_excel
from tqdm import tqdm

long_text = load_excel('./fb.xlsx', to_list=True)
cases = []
cases_show = []
for line in tqdm(long_text):
    text = line[0]
    keyword = list(get_keyword(text).keys())
    if len(keyword) == 0:
        continue
    if len(text) < 50:
        continue
    ist = "生成一个抖音用户的反馈，口语化，需要涉及词：{}".format('，'.join(keyword[:8]))
    case = {
        "instruction": ist,
        "input": "",
        "output": "{}".format(text)
    }
    cases.append(case)
    cases_show.append([text, ist])
dump_json(cases, 'task_fb.json', formatting=True)
dump_excel(cases_show, 'task_fb.xlsx', index=False)

common_cases = load_json('./common.json')
all_cases = common_cases + cases
dump_json(all_cases, 'all_cases_fb.json', formatting=True)