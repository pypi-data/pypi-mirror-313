# -*- coding: UTF-8 -*-
# Copyright xiangyuejia@qq.com All Rights Reserved
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
Created on
"""
from typing import List, Tuple
from collections import defaultdict
from itertools import combinations
from time import time

from tqdm import tqdm

from aitool import load_pickle, load_excel, get_ngrams, ngrams_permutation, is_all_chinese, dump_pickle


class Text2Text(object):
    """
    基于ngram，对输入文本query，输出一个文本ans
    """

    def __init__(
            self,
            file_data: str = None,
            query_max_length=200,
            ans_max_length=200,
            word_min_char=1,
            word_max_char=3,
            word_min_time=2,
            rank_min=2,
            rank_max=2,
            all_chinese=True,
            num_word_recall=500,
            update: bool = False,
            text2name: List = None,
    ):
        """
        生成或加载概率参数

        :param file_data: 参数文件的路径
        :param query_max_length: 输入文本的最大字长
        :param ans_max_length: 输出文本的最大字长
        :param word_min_char: 词包含的最小字数
        :param word_max_char: 词包含的最大字数
        :param word_min_time: 词被存储需要出现的最小次数
        :param rank_min: 一个rank的最小词数
        :param rank_max: 一个rank的最大词数
        :param all_chinese: 词是否必须由中文构成
        :param num_word_recall: query中的词召回的可能词数
        :param update: 更新参数
        :param text2name: 输入到输出的数据List[Tuple[str,str]]
        """
        if file_data is None:
            file_data = "./model_fine/text2text.pkl"
        self.file_data = file_data
        self.query_max_length = query_max_length
        self.ans_max_length = ans_max_length
        self.word_min_char = word_min_char
        self.word_max_char = word_max_char
        self.word_min_time = word_min_time
        self.rank_min = rank_min
        self.rank_max = rank_max
        self.all_chinese = all_chinese
        self.num_word_recall = num_word_recall
        self.text2name = text2name
        self.head_token = "[head]"
        self.end_token = "[end]"

        if update:
            self.update_data()

        data = load_pickle(self.file_data)
        self.w2id = data["w2id"]
        self.id2w = data["id2w"]
        self.qw2aw2prb = data["qw2aw2prb"]
        self.order2prb = data["order2prb"]
        head_token = "[head]"
        end_token = "[end]"
        self.head_wid = self.w2id[head_token]
        self.end_wid = self.w2id[end_token]

    def infer(
        self,
        text,
        word_min_char=1,
        word_max_char=3,
        max_cand_word=20,
        min_combine=2,
        max_combine=5,
        min_length=3,
        max_length=6,
        name_cnt=10,
        head_score_power=2,
        end_score_power=1.5,
    ):
        """
        基于输出的文本输出name_cnt个输出

        :param text: 输入的文本
        :param word_min_char: 词的字数下限
        :param word_max_char: 词的字数上限
        :param max_cand_word: 构成输入的后续词的数量（和输出的长度有关）
        :param min_combine: 输出包含的词数下限
        :param max_combine: 输出包含的词数上限
        :param min_length: 输出的最小字数
        :param max_length: 输出的最大字数
        :param name_cnt: 获取name_cnt个输出
        :param head_score_power: 开头词的通顺度得分加权
        :param end_score_power: 结尾词的通顺度得分加权
        :return: name_cnt个输出

        >>> p = Text2Text()
        >>> p.infer('一位神秘的女巫，她的头发是白色的，戴着一顶尖帽子，身穿黑色的长袍，脸上带着一个古怪的面具，眼神犀利而深邃')
        >>> p.infer('风元素 - 一只优雅的鹰隼在天空中翱翔，它的翅膀如同轻盈的风，揭示了空气的流动与变化。当鹰隼被召唤时，它会吹起狂风，让敌人无法站稳脚步。')
        >>> p.infer('一本书籍在空中翻滚，书页上写满了神秘的符文，每一个字母都在发光，散发着强大的魔力')

        """
        print("text", text)
        b = time()
        text_w = set(get_ngrams(text, word_min_char, word_max_char))
        text_wids = [self.w2id[w] for w in text_w if w in self.w2id]
        nwid2score = defaultdict(float)
        for twid in text_wids:
            if twid not in self.qw2aw2prb:
                continue
            for nwid in self.qw2aw2prb[twid].keys():
                nwid2score[nwid] += self.qw2aw2prb[twid][nwid]
        print("nwid2score", time() - b)
        b = time()
        nwid_score = [[k, v] for k, v in nwid2score.items()]
        nwid_score.sort(key=lambda _: _[1], reverse=True)
        cand_wid = [k for k, v in nwid_score[:max_cand_word]]
        cand_word = [self.id2w[wid] for wid in cand_wid]
        print("cand_word", cand_word)
        print("cand_word", time() - b)
        b = time()

        all_permutate = []
        for cb in range(min_combine, max_combine + 1):
            all_permutate += list(combinations(cand_wid, cb))
        print("len all_permutate", len(all_permutate))
        print("len all_permutate", time() - b)
        b = time()
        pmt_infos = []
        for permutate_wid in tqdm(all_permutate, "all_permutate"):
            pmt_name = "".join([self.id2w[wid] for wid in permutate_wid])
            name_length = len(pmt_name)

            if name_length > max_length:
                continue
            if name_length < min_length:
                continue
            if pmt_name[0] in {"之", "者"}:  # 去除第一个字不合理的badcase
                continue
            if name_length != len(set(pmt_name)):  # 去除含有重复的字的case
                continue

            permutate_wid = [self.head_wid] + list(permutate_wid) + [self.end_wid]
            ww2prbs = []
            for i in range(len(permutate_wid) - 1):
                wid1 = permutate_wid[i]
                wid2 = permutate_wid[i + 1]
                if (wid1, wid2) in self.order2prb:
                    score = self.order2prb[(wid1, wid2)]
                    if i == 0:
                        score = score * head_score_power
                    if i == len(permutate_wid) - 2:
                        score = score * end_score_power
                    ww2prbs.append(score)
                else:
                    ww2prbs.append(0.0)

            pmt_ww2prb = sum(ww2prbs) / len(ww2prbs)
            pmt_infos.append([pmt_name, pmt_ww2prb])

        print("get infos", time() - b)
        b = time()
        name2score_unique = defaultdict(
            float
        )  # 如果一个名字被多种方式构建出来，其分数累加
        for name, score in pmt_infos:
            name2score_unique[name] += score
        pmt_infos_unique = [[k, v] for k, v in name2score_unique.items()]
        name2score_rank = sorted(pmt_infos, key=lambda _: _[1], reverse=True)
        name2score_unique_rank = sorted(
            pmt_infos_unique, key=lambda _: _[1], reverse=True
        )
        names = [info[0] for info in name2score_rank[:name_cnt]]
        names_unique = [info[0] for info in name2score_unique_rank[:name_cnt]]
        print("get names", time() - b)
        print("names", names)
        print("names_unique", names_unique)
        return names_unique

    def update_data(self):
        w2cnt = defaultdict(int)  # w出现的次数
        qw2aw2cnt = defaultdict(int)  # query_w关联出ans_w的次数,用于召回w
        order2cnt = defaultdict(int)  # w与w在name里前后顺序共现次数
        for query, ans in tqdm(self.text2name, "qw2aw2cnt & order2cnt"):
            query = query[:self.query_max_length]
            ans = ans[:self.ans_max_length]
            
            # 统计query中的词与ans中的词共现的次数（去重）
            query_w = set(get_ngrams(query, self.word_min_char, self.word_max_char))
            ans_w = set(get_ngrams(ans, self.word_min_char, self.word_max_char))
            w2cnt[self.head_token] += 2
            w2cnt[self.end_token] += 2
            for w in query_w:
                w2cnt[w] += 1
            for w in ans_w:
                w2cnt[w] += 1
            for qw in query_w:
                for aw in ans_w:
                    qw2aw2cnt[(qw, aw)] += 1
            
            # 统计ans中词序列的出现次数 TODO 目前仅考虑长度为2的序列
            for pmt in ngrams_permutation(ans, self.word_min_char, self.word_max_char):
                pmt = [self.head_token] + pmt + [self.end_token]
                for order in get_ngrams(pmt, self.rank_min, self.rank_max):
                    order2cnt[tuple(order)] += 1
        
        # 获取词id
        w2id = {}
        id2w = {}
        for w, c in w2cnt.items():
            if c < self.word_min_time:
                continue
            if self.all_chinese and not is_all_chinese(w):
                if w != self.head_token and w != self.end_token:
                    continue
            wid = len(w2id)
            w2id[w] = wid
            id2w[wid] = w

        # query中的词召回ans中的词共现的概率
        qw2aw2prb = {}  # 例如{"书": {"写作":0.5, "笔":0.3}}，表示query中出现词“书”时，ans中可能出现词“写作”的概率是0.5，ans中出现"笔"的概率是0.3
        qw2aw2prb_whole = {}
        qw2aw_whole = defaultdict(set)
        qw2cnt = defaultdict(int)
        for (qw, aw), c in tqdm(qw2aw2cnt.items(), "qw2aw2prb_step1"):
            qw2cnt[qw] += c
        for (qw, aw), c in tqdm(qw2aw2cnt.items(), "qw2aw2prb_step2"):
            if qw in w2id and aw in w2id:
                qw2aw_whole[w2id[qw]].add(w2id[aw])
                qw2aw2prb_whole[(w2id[qw], w2id[aw])] = c / qw2cnt[qw]
        for qw, aws in tqdm(qw2aw_whole.items(), "qw2aw2prb_step3"):
            qw2aw2prb[qw] = {}
            aw_score = []
            for aw in aws:
                aw_score.append([aw, qw2aw2prb_whole[qw, aw]])
            aw_score.sort(key=lambda _: _[1], reverse=True)
            the_num_word_recall = self.num_word_recall
            if qw == self.head_token:   # 开始符不限制recall长度
                the_num_word_recall = len(aw_score)
            for aw, sc in aw_score[:the_num_word_recall]:
                qw2aw2prb[qw][aw] = sc

        # 统计ans中词序列的概率 p(w_1,w_2, ..., w_(n-1) | w_n)
        order2prb = {}  # {'我们':0.4} 表示 p('我'|'们')=0.3
        order_head2cnt = defaultdict(int)
        for order, c in tqdm(order2cnt.items(), "order2prb_step1"):
            order_head2cnt[order[:-1]] += c
        for order, c in tqdm(order2cnt.items(), "order2prb_step2"):
            order_id = tuple(map(w2id.get, order))
            if None in order_id:
                continue
            order2prb[order_id] = c / order_head2cnt[order[:-1]]

        dump_data = {
            "w2id": w2id,
            "id2w": id2w,
            "qw2aw2prb": qw2aw2prb,
            "order2prb": order2prb,
        }
        print("存储数据...")
        dump_pickle(dump_data, self.file_data)


if __name__ == "__main__":
    file_text2names = '/Users/bytedance/card-effect-editor/model_docs/生成_用户描述2名称_1225.xlsx'
    _data = load_excel(file_text2names, to_list=True)
    q2a = []
    for line in tqdm(_data, "format qa"):
        _text = line[0]
        names = line[1:]
        for name in names:
            if len(name) <= 1:
                continue
            q2a.append([_text, name])
    p = Text2Text(update=False, text2name=q2a)
    p.infer('一位神秘的女巫，她的头发是白色的，戴着一顶尖帽子，身穿黑色的长袍，脸上带着一个古怪的面具，眼神犀利而深邃')
    p.infer(
        '风元素 - 一只优雅的鹰隼在天空中翱翔，它的翅膀如同轻盈的风，揭示了空气的流动与变化。当鹰隼被召唤时，它会吹起狂风，让敌人无法站稳脚步。')
    p.infer('一本书籍在空中翻滚，书页上写满了神秘的符文，每一个字母都在发光，散发着强大的魔力')
