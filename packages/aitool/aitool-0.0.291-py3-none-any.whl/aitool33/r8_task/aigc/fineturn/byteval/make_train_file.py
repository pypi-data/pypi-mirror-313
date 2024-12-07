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
from collections import defaultdict
from aitool import load_excel, add_noise, dump_json, dump_lines
from tqdm import tqdm
from random import sample


if __name__ == '__main__':
    case_num = 1000000
    rst = []
    input_output = []
    data_file = load_excel('./风险等级标注结果0912.xlsx', to_list=True)
    for d in data_file:
        input_output.append((d[0], d[1]))
    for _ in tqdm(range(case_num)):
        input, output = sample(input_output, 1)[0]
        input = input.replace('\n', ' ')     # 删除\n，以确保模型能用\n识别出要判断的部分
        input = add_noise(input)
        instruction = '你是一个审核员。风险等级审核标准: R0（极高风险），R1（高风险），R2（中风险），R3（低风险）, NoRisk（无风险）。' \
                      '请判断下述文本的风险等级：\n{}'.format(input)
        rst.append({"instruction": instruction, "input": "", "output": output})

    print('len rst', len(rst))
    dump_json(rst, 'risk0912_s0.3.json')
    dump_lines(rst, 'risk0912_s0.3.txt')
