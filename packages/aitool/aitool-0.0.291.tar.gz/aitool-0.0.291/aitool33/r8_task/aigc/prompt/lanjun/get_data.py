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
from aitool import load_pickle, dump_excel
from tqdm import tqdm

# 这是旧版的panda生成的pickle,不兼容2.1的版本
# ARCHFLAGS="-arch arm64" pip install pandas==1.3.5 -i https://pypi.tuna.tsinghua.edu.cn/simple --compile --no-cache-dir
data = load_pickle('/Users/bytedance/Downloads/df_all_test_20230903.pkl')
rst_fb = []
rst_im = []
for scr, tag, speak in tqdm(data.values.tolist()):
    if 'feedback' in tag:
        rst_fb.append([scr, speak[0]])
    if 'im' in tag:
        rst_im.append([scr, ' $$$ '.join(speak)])
dump_excel(rst_fb, 'feadbacks.xlsx')
dump_excel(rst_im, 'im.xlsx')
