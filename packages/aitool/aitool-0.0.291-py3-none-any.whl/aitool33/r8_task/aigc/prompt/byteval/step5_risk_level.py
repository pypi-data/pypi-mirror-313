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
from aitool import load_excel, dump_excel

data = load_excel('./eval_1023.xlsx', to_list=True)
rst = []
for line in data:
    kind = line[0]
    text = line[2]
    ppt = '你是一个审核员。风险等级审核标准: R0（极高风险），R1（高风险），R2（中风险），R3（低风险）, NoRisk（无风险）。' \
          '请判断下述文本的风险等级：\n{}'.format(text)
    rst.append([kind, text, ppt])
dump_excel(rst, 'rst_risk_text_1023.xlsx')
