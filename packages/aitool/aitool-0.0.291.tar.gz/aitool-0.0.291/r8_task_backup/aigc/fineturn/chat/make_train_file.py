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
import json
from typing import Dict, Union, List, Any, NoReturn, Tuple
from collections import defaultdict
from aitool import load_excel, add_noise, dump_json, load_lines, dump_lines, send_feishu_sheet
from tqdm import tqdm
from random import sample


if __name__ == '__main__':
    rst = []
    data_file = load_lines('./sensitive_detection_bloom_train_data_xx_prompt.jsonl')
    for d in data_file:
        df = json.loads(d)
        input = df['input']
        output = df['output']
        rst.append({"instruction": input, "input": "", "output": output})

    print('len rst', len(rst))
    dump_json(rst, 'chat0919.json')
    dump_lines(rst, 'chat0919.txt')
