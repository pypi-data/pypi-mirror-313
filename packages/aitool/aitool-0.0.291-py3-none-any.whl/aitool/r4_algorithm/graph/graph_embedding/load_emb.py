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
from tqdm import tqdm
from collections import defaultdict
from aitool import load_csv, load_pickle, dump_lines

file_1_uid = '/Users/bytedance/Downloads/281475002856177-graph_online-1. 主要uid：处罚uid-查询23.csv'
file_2_uid_did = '/Users/bytedance/Downloads/281475002856178-graph_online-2. 扩展uid：与主要uid设备1跳关联-查询8.csv'
file_3_uid_info = '/Users/bytedance/Downloads/281475002856180-graph_online-3.uid属性：昵称+签名-查询5.csv'
file_4_uid_title = '/Users/bytedance/Downloads/281475002856181-graph_online-4.vid信息：uid, title, asr, ocr-查询8.csv'
file_5_uid_group_id = '/Users/bytedance/Downloads/281475002884053-graph_online-5.扩展uid_ group_id扩散-查询5.csv'

uid_core = load_csv(file_1_uid, to_list=True)
uid_did = load_csv(file_2_uid_did, to_list=True)
uid_info = load_csv(file_3_uid_info, to_list=True)
uid_title = load_csv(file_4_uid_title, to_list=True)
uid_group_id = load_csv(file_5_uid_group_id, to_list=True)

uids = set([u[0] for u in uid_core])
uid2did = defaultdict(set)
did2uid = defaultdict(set)
for u, d in tqdm(uid_did, 'uid_did'):
    if u not in uids:
        continue
    uid2did[u].add(d)
    did2uid[d].add(u)
uid2info = defaultdict(str)
for u, a, b in tqdm(uid_info, 'uid_info'):
    uid2info[u] = str(a)+str(b)
uid2title = defaultdict(list)
for u, t in tqdm(uid_title, 'uid_title'):
    uid2title[u].append(t)
uid2group = defaultdict(set)
group2uid = defaultdict(set)
for _, u, g in tqdm(uid_group_id, 'uid_title'):
    uid2group[u].add(g)
    group2uid[g].add(u)
embedding = load_pickle('sentences_all.pkl')
print('len emb', len(embedding))

uid2emb = {}
for uid in tqdm(uids, 'init emb'):
    infos = []
    if uid in uid2info:
        infos.append(uid2info[uid])
    else:
        kk = 1
    if uid in uid2title:
        for t in uid2title[uid]:
            infos.append(t)
    embs = []
    for info in infos:
        if info in embedding:
            embs.append(embedding[info])
    if len(embs) > 0:
        emb = np.mean(embs, axis=0)
        uid2emb[uid] = emb

epoch = 1
weight_self = 0.8
weight_extend = 0.2
uid2emb_new = {}
for i in range(epoch):
    for uid in tqdm(uids, 'in epoch'):
        nei = set()
        for did in uid2did[uid]:
            for _nu in did2uid[did]:
                nei.add(_nu)
        for gid in uid2group[uid]:
            for _nu in group2uid[gid]:
                nei.add(_nu)
        nei = nei - {uid}
        if uid in uid2emb:
            emb_self = uid2emb[uid]
        else:
            emb_self = None
        emb_extend = []
        for nu in nei:
            if nu in uid2emb:
                emb_extend.append(uid2emb[nu])
        if emb_self is not None and len(emb_extend) != 0:
            uid2emb_new[uid] = weight_self * emb_self + weight_extend * np.mean(emb_extend, axis=0)
        if emb_self is not None and len(emb_extend) == 0:
            uid2emb_new[uid] = emb_self
        if emb_self is None and len(emb_extend) != 0:
            uid2emb_new[uid] = np.mean(emb_extend, axis=0)
    uid2emb = uid2emb_new
    uid2emb_new = {}

rst = []
part = 0
for uid, emb in tqdm(uid2emb.items(), 'built rst'):
    rst.append(str(uid) + ',' + '\t'.join([str(score)[:8] for score in emb.tolist()]))
    if len(rst) >= 100000:
        dump_lines(rst, 'uid2emb_epo{}_part{}.txt'.format(epoch, part))
        rst = []
        part += 1
dump_lines(rst, 'uid2emb_epo{}_part{}.txt'.format(epoch, part))

rst = []
for uid, emb in tqdm(uid2emb.items(), 'built rst'):
    rst.append(str(uid) + ',' + '\t'.join([str(score)[:8] for score in emb.tolist()]))
dump_lines(rst, 'uid2emb_epo{}_all.txt'.format(epoch))
