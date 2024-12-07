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
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from aitool import load_csv, dump_pickle, dump_lines
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('bert-base-chinese')

file_1_uid = '/Users/bytedance/Downloads/281475002856177-graph_online-1. 主要uid：处罚uid-查询23.csv'
file_2_uid_did = '/Users/bytedance/Downloads/281475002856178-graph_online-2. 扩展uid：与主要uid设备1跳关联-查询8.csv'
file_3_uid_info = '/Users/bytedance/Downloads/281475002856180-graph_online-3.uid属性：昵称+签名-查询5.csv'
file_4_uid_title = '/Users/bytedance/Downloads/281475002856181-graph_online-4.vid信息：uid, title, asr, ocr-查询8.csv'

uid = load_csv(file_1_uid, to_list=True)
uid_did = load_csv(file_2_uid_did, to_list=True)
uid_info = load_csv(file_3_uid_info, to_list=True)
uid_title = load_csv(file_4_uid_title, to_list=True)

sentences_info = [str(b)+str(c) for _, b, c in uid_info]
print('len sentences_info', len(sentences_info))
sentences_title = []
u2t = defaultdict(int)
for _u, t in uid_title:
    u2t[_u] += 1
    if u2t[_u] <= 3:
        sentences_title.append(t)
print('len sentences_title', len(sentences_title))
sentences_all = sentences_info + sentences_title
sentences_all = sentences_all
print('len sentences_all', len(sentences_all))
dump_lines(sentences_all, 'sentences_all.txt')

embeddings_all = []
for i in tqdm(range(len(sentences_all)//3200)):
    sentence_embeddings = model.encode(sentences_all[i*3200:i*3200+3200])
    embeddings_all.extend(sentence_embeddings)

rst = {}
for sentence, embedding in zip(sentences_all, embeddings_all):
    rst[sentence] = embedding
dump_pickle(rst, 'sentences_all_0530.pkl')

