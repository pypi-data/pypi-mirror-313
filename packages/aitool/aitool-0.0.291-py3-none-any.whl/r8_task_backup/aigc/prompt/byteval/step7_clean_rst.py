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
from aitool import load_excel, is_all_chinese, dump_excel, load_lines
import random
data = []
#
# data.extend(load_excel('/Users/bytedance/Downloads/rst_risk_text_1023_with_level_p0.xlsx', to_list=True))
# is_with_risk_level = True
#
data.extend(load_excel('/Users/bytedance/PycharmProjects/aitool/aitool/r8_task/aigc/prompt/byteval/eval_1027.xlsx', to_list=True))
is_with_risk_level = False

rst = []
print(len(data))
for line in data:
    if is_with_risk_level:
        tag, text, ppt, risk = line
    else:
        tag, ppt, text = line
        risk = 'UNK'
    rc = []
    if 'R0' in risk:
        rc.append('R0')
    if 'R1' in risk:
        rc.append('R1')
    if 'R2' in risk:
        rc.append('R2')
    if 'R3' in risk:
        rc.append('R3')
    if 'NoRisk' in risk:
        rc.append('NoRisk')
    if 'UNK' in risk:
        rc.append('UNK')
    if len(rc) != 1:
        continue

    badword = ['模型', '作为', '做为']
    bad = 0
    for bw in badword:
        if bw in text:
            bad = 1
            break
    if bad == 1:
        continue

    if len(text) < 20:
        continue
    text = text.strip()
    text = text.replace('\n', '')
    if not is_all_chinese(text[0]):
        continue
    char_num_ch = 0
    for c in text:
        if is_all_chinese(c):
            char_num_ch += 1
    if char_num_ch / len(text) < 0.8:
        continue
    text = text.replace('\"', '')

    if is_all_chinese(text[-1]):
        print(text)
    rst.append([tag, rc[0], text])

random.shuffle(rst)
print(len(rst))
rst = [['tag', 'risk', 'text']] + rst
dump_excel(rst, 'rst_clean_1027.xlsx')