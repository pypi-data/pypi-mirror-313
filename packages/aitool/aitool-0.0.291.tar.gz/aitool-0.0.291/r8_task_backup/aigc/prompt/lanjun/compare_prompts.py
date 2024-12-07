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
epo = 100
rst += epo * ['假设你是抖音用户，发现自己的隐私权受到侵犯，需要向抖音反馈。请模拟用户语气，根据如下规则生成5条反馈：规则一，生成的反馈需要是连贯的句子，必须体现4部分内容，分别是用户行为、用户预期、抖音行为、用户疑问；规则二，生成的反馈需要参考如下场景：用户行为是打开私信列表，用户预期是看到自己收发过的私信，抖音行为是将其他用户的信息泄露到该用户的私信中，用户疑问是为什么会收到他人私信']
rst += epo * ["""模拟用户语气，生成离线反馈数据5条，描述抖音"用户发现自己的隐私权受到侵犯，需要向抖音反馈"方面的问题，围绕"隐私权受到侵犯"。生成的反馈需要是连贯的句子，必须体现4部分内容，分别是用户行为、用户预期、抖音行为、用户疑问。生成的反馈需要参考如下场景：用户行为是打开私信列表，用户预期是看到自己收发过的私信，抖音行为是将其他用户的信息泄露到该用户的私信中，用户疑问是为什么会收到他人私信。
输出格式：
1. 
2. 
3. 
4. 
5. 。"""]
dump_pickle(rst, 'prompts_lanjun_compare_1129.pkl')
dump_excel(rst, 'prompts_lanjun_compare_1129.xlsx')
