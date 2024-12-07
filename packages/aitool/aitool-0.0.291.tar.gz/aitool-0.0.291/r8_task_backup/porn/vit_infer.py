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
对一批图片路径做预测
"""
from typing import Dict, Union, List, Any, NoReturn, Tuple
# -*- coding: UTF-8 -*-
from transformers import pipeline
from time import time
from math import ceil
from aitool import load_lines, dump_lines
from tqdm import tqdm

model_checkpoint = "/mnt/bn/mlxlabzw/xiangyuejia/porn/swin-tiny-patch4-window7-224-finetuned-eurosat"
ori_data = load_lines('/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0825_13_pic_index.txt')
classifier = pipeline("r5_image-classification", model=model_checkpoint, device="cuda:0", num_workers=32)

widx = 7
work = 6
num_piece = len(ori_data) // 8
bs = 128
bss = bs * 10
data = ori_data[widx*num_piece: (widx+1)*num_piece]
rst = []
for i in tqdm(range(ceil(num_piece//bss))):
    bdata = data[i*bss: (i+1)*bss]
    outputs = classifier(bdata, batch_size=bs)
    if len(bdata) != len(outputs):
        print('bad')
        continue

    for p, s in zip(bdata, outputs):
        o = {'noporn': 0, 'porn': 0}
        o[s[0]['label']] = s[0]['score']
        o[s[1]['label']] = s[1]['score']
        if o['porn'] > o['noporn']:
            rst.append(p)

    dump_lines(rst, '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0828_10_pic_index_rst_p{}.txt'.format(widx))
