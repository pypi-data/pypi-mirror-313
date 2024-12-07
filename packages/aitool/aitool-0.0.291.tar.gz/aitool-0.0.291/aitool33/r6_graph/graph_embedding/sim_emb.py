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
from aitool import load_lines
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from aitool import load_csv, load_pickle, dump_lines

file_1_uid = '/Users/bytedance/Downloads/281475002856177-graph_online-1. 主要uid：处罚uid-查询23.csv'
file_2_uid_did = '/Users/bytedance/Downloads/281475002856178-graph_online-2. 扩展uid：与主要uid设备1跳关联-查询8.csv'
file_3_uid_info = '/Users/bytedance/Downloads/281475002856180-graph_online-3.uid属性：昵称+签名-查询5.csv'
file_4_uid_title = '/Users/bytedance/Downloads/281475002856181-graph_online-4.vid信息：uid, title, asr, ocr-查询8.csv'

uid_core = load_csv(file_1_uid, to_list=True)
uid_info = load_csv(file_3_uid_info, to_list=True)
uid_title = load_csv(file_4_uid_title, to_list=True)

uids = set([u[0] for u in uid_core])
uid2info = defaultdict(str)
for u, a, b in tqdm(uid_info, 'uid_info'):
    uid2info[u] = str(a)+str(b)
uid2title = defaultdict(list)
for u, t in tqdm(uid_title, 'uid_title'):
    uid2title[u].append(t)

uid2level = {}
for uid in tqdm(uids, 'init emb'):
    if uid in uid2title:
        uid2level[uid] = 2
    elif uid in uid2info and len(uid2info[uid]) >= 20:
        uid2level[uid] = 1
    else:
        uid2level[uid] = 0


def get_cos_similar(v1: list, v2: list):
    num = float(np.dot(v1, v2))  # 向量点乘
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)  # 求模长的乘积
    return 0.5 + 0.5 * (num / denom) if denom != 0 else 0


embedding = {}
data = load_lines('uid2emb.txt', separator='\t')
for line in data:
    uid = line[0]
    emb = [float(_) for _ in line[1:]]
    embedding[uid] = emb

for u1 in embedding.keys():
    for u2 in embedding.keys():
        if uid2level[u1] != 2 or uid2level[u1] != 2:
            continue
        n1 = np.array(embedding[u1])
        n2 = np.array(embedding[u2])
        score = get_cos_similar(n1, n2)
        if score < 0.90:
            continue
        print(u1, u2, score)

