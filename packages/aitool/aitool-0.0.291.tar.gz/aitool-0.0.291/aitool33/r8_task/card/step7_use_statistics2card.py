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
from aitool import load_excel, is_all_chinese, singleton
from tqdm import tqdm
import jieba


@singleton
class StatisticsModelInfer:
    def __init__(self):
        train_df = load_excel('./word2hrl.xlsx', value=False)
        header = list(train_df.columns)
        effect = header[1:]
        words = train_df[header[0]].values.tolist()
        targets = train_df[header[1:]].values.tolist()
        self.effect = effect
        self.word2hrl = [defaultdict(int) for _ in range(len(effect))]
        for word, target in tqdm(zip(words, targets)):
            for idx, score in enumerate(target):
                self.word2hrl[idx][word] = score
        self.hrl2prb = [(0.00, 0.0), (0.2, 0.1), (0.5, 0.2), (0.7, 0.3), (0.8, 0.4), (1.0, 0.5), (1.2, 0.6), (1.5, 0.7), (1.8, 0.8), (2.0, 0.9), (2.5, 1.0), (2.5, 1.0),]

    def infer(self, text):
        words = jieba.cut(text, cut_all=False)
        words = [word for word in words if is_all_chinese(word)]
        scores = [[] for _ in range(len(self.effect))]
        for word in set(words):
            for idx in range(len(self.effect)):
                if self.word2hrl[idx][word] != -1:
                    scores[idx].append(self.word2hrl[idx][word])
        rst = []
        for score_list in scores:
            if len(score_list) == 0:
                rst.append(0)
            else:
                score_average = sum(score_list)/len(score_list)
                for sav, prb in self.hrl2prb[::-1]:
                    if score_average >= sav:
                        rst.append(prb)
                        break
        return rst


def infer(text):
    """
    用模型预测文本对应不同技能的概率
    """
    model = StatisticsModelInfer()
    outputs = model.infer(text)
    return outputs


if __name__ == '__main__':
    print(infer(
        '一位神秘的女巫，她的头发是白色的，戴着一顶尖帽子，身穿黑色的长袍，脸上带着一个古怪的面具，眼神犀利而深邃'))
    print(infer(
        '风元素 - 一只优雅的鹰隼在天空中翱翔，它的翅膀如同轻盈的风，揭示了空气的流动与变化。当鹰隼被召唤时，它会吹起狂风，让敌人无法站稳脚步。'))
    print(infer('一本书籍在空中翻滚，书页上写满了神秘的符文，每一个字母都在发光，散发着强大的魔力'))
