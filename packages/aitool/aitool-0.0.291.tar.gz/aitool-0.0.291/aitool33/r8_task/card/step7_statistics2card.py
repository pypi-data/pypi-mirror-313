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
基于字级别的ngram概率统计来预测概率
"""
from typing import Dict, Union, List, Any, NoReturn, Tuple
from collections import defaultdict
from aitool import load_excel, is_all_chinese, dump_excel
from tqdm import tqdm
import jieba

train_df = load_excel('../bert_cls/生成_用户描述2分数_1225.xlsx', value=False)
header = list(train_df.columns)
sentences = train_df[header[0]].values.tolist()
targets = train_df[header[1:]].values.tolist()
effect = header[1:]
high_thr = 0.8
low_thr = 0.2
least_count = 20
word2high = [defaultdict(int) for _ in range(len(effect))]
word2low = [defaultdict(int) for _ in range(len(effect))]
high_sent_c = [0 for _ in range(len(effect))]
low_sent_c = [0 for _ in range(len(effect))]
for sentence, target in tqdm(zip(sentences, targets)):
    for idx, score in enumerate(target):
        if score >= high_thr:
            counter = word2high[idx]
            high_sent_c[idx] += 1
        else:
            counter = word2low[idx]
            low_sent_c[idx] += 1
        words = jieba.cut(sentence, cut_all=False)
        words = [word for word in words if is_all_chinese(word)]
        for word in set(words):
            counter[word] += 1
word2hrl = [defaultdict(int) for _ in range(len(effect))]
for idx in range(len(effect)):
    for w in (set(word2high[idx].keys()) | set(word2low[idx].keys())):
        if w not in word2high[idx] and word2low[idx][w] >= least_count:
            word2hrl[idx][w] = 0
        elif w not in word2low[idx] and word2high[idx][w] >= least_count:
            word2hrl[idx][w] = 1000000
        elif word2low[idx][w] + word2high[idx][w] >= least_count:
            word2hrl[idx][w] = (word2high[idx][w]/high_sent_c[idx]) / (word2low[idx][w]/low_sent_c[idx])
        else:
            word2hrl[idx][w] = -1
rst = []
rst.append(header)
for w in (set(word2high[idx].keys()) | set(word2low[idx].keys())):
    line = []
    line.append(w)
    for idx in range(len(effect)):
        line.append(word2hrl[idx][w])
    rst.append(line)
dump_excel(rst, 'word2hrl.xlsx')
