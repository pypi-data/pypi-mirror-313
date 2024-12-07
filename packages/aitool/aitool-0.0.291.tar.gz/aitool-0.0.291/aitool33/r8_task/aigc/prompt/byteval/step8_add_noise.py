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
from aitool import load_excel, dump_excel, add_noise, get_stop_word, get_punctuation
from tqdm import tqdm
from random import sample

data = load_excel('./rst_clean_1027.xlsx', to_list=True)
rst = [['tag', 'noise', 'risk', 'text']]
tokens = list(get_punctuation())
for idx, level, text in tqdm(list(sample(data, 1000))):
    rst.append([idx, 'ori', level, text])
    for _ in range(10):
        noised_p1 = add_noise(text, tokens=tokens, prob_ori=0, prob_add=0.10, prob_dlt=0.00, prob_rpl=0.00, prob_pmt=0.10, range_pmt=1,)
        noised_p2 = add_noise(text, tokens=tokens, prob_ori=0, prob_add=0.20, prob_dlt=0.00, prob_rpl=0.00, prob_pmt=0.20, range_pmt=2,)
        noised_p3 = add_noise(text, tokens=tokens, prob_ori=0, prob_add=0.30, prob_dlt=0.00, prob_rpl=0.00, prob_pmt=0.30, range_pmt=3,)
        rst.append([idx, 'p1', level, noised_p1])
        rst.append([idx, 'p2', level, noised_p2])
        rst.append([idx, 'p3', level, noised_p3])
dump_excel(rst, './rst_noise_1102.xlsx')
