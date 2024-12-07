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
import jieba
from math import log2
from aitool import get_ngrams, is_all_chinese, is_no_symbol
from collections import defaultdict
from tqdm import tqdm


def _jieba_tfidf():
    tfidf = jieba.analyse.TFIDF()
    return tfidf.tokenizer.cut


def _split_char(text):
    return [_ for _ in text]


def _idf_log(time, all_count):
    return log2((all_count+1)/(time+1))


def _idf_rate(time, all_count):
    return 1-time/(all_count+1)


def get_ngram_idf(
        texts,
        split_method=None,
        idf_method=None,
        max_char=6,
        min_gram=1,
        max_gram=6,
        all_chinese=True,
        all_content=False,
        no_space=False,
        no_border_space=True,
        round_len=6,
):
    if split_method is None:
        split_method = _split_char
    elif split_method == 'char':
        split_method = _split_char
    elif split_method == 'jieba':
        split_method = _jieba_tfidf()
    else:
        # TODO
        pass
    if idf_method is None:
        idf_method = _idf_rate
    elif idf_method == 'log':
        idf_method = _idf_log
    elif idf_method == 'rate':
        idf_method = _idf_rate
    else:
        # TODO
        pass
    all_count = len(texts)
    term2time = defaultdict(int)
    for text in tqdm(texts, 'building terms', delay=60, mininterval=60, maxinterval=120):
        terms = set()
        text = text.replace('\t', ' ')
        tokens = list(split_method(text))
        for ntoken in get_ngrams(tokens, min_gram, max_gram):
            term = ''.join(ntoken)
            if all_chinese and not is_all_chinese(term):
                continue
            if all_content and not is_no_symbol(term):
                continue
            if no_space and ' ' in term:
                continue
            if no_border_space and len(term) >= 1 and (term[0] == ' ' or term[-1] == ' '):
                continue
            if len(term) > max_char:
                continue
            terms.add(term)
        for term in terms:
            term2time[term] += 1
    term2idf = {}
    for k, v in tqdm(term2time.items(), 'calculate idf', delay=5):
        term2idf[k] = round(idf_method(v, all_count), round_len)
    print('len terms', len(term2idf))
    return term2idf


def get_ngram_tf(
        texts,
        deduplication=False,
        split_method=None,
        max_char=6,
        min_gram=1,
        max_gram=6,
        all_chinese=True,
        show=True,
        show_detail=False,
        show_detail_time=3,
        no_space=True,
        no_border_space=True,
        get_info=False,
        examples_num=0,
        extra_info: List[str] = None,
        round_len=6,
):
    if extra_info:
        assert len(texts) == len(extra_info)
    else:
        extra_info = [''] * len(texts)
    if split_method is None:
        split_method = _split_char
    elif split_method == 'char':
        split_method = _split_char
    elif split_method == 'jieba':
        split_method = _jieba_tfidf()
    else:
        # TODO
        pass
    all_count = len(texts)
    term2time = defaultdict(int)
    term2example = defaultdict(set)
    term2extra = defaultdict(set)
    show_detail_count = 0
    for text, ext in tqdm(zip(texts, extra_info), 'building terms', delay=60, mininterval=60, maxinterval=120):
        if deduplication:
            terms = set()
        else:
            terms = []
        tokens = list(split_method(text))
        for ntoken in get_ngrams(tokens, min_gram, max_gram):
            term = ''.join(ntoken)
            if all_chinese and not is_all_chinese(term):
                continue
            if no_space and ' ' in term:
                continue
            if no_border_space and len(term) >= 1 and (term[0] == ' ' or term[-1] == ' '):
                continue
            if len(term) > max_char:
                continue
            if deduplication:
                terms.add(term)
            else:
                terms.append(term)
        if show_detail and show_detail_count < show_detail_time:
            print(text)
            print(terms)
            show_detail_count += 1
        for term in terms:
            term2time[term] += 1
            if get_info and len(term2example[term]) < examples_num:
                term2example[term].add(text)
            term2extra[term].add(ext)
    term2tf = {}
    for k, v in tqdm(term2time.items(), 'calculate idf', delay=20):
        term2tf[k] = round(v/all_count, round_len)
    if show:
        print('len terms', len(term2tf))
    if show_detail:
        print('term2time')
        term2time_rank = [[k, v] for k, v in term2time.items()]
        term2time_rank.sort(key=lambda _: _[1], reverse=True)
        print(term2time_rank[:300])
    if get_info is False:
        return term2tf
    else:
        return term2tf, term2time, term2example, term2extra


if __name__ == '__main__':
    data = [
        'yw ibiee pp ii eeie ke adeui sie ek mabiw dage  laiei|u wi  pp i eewezke apew j sie ely wad e eeaab e|',
        'ilu ie llelikiw seailea 水|',
        'xipig aqamsiz ayrim gap kilig|',
        'kino ba|QQ kino ba|kino ba QQ|来小世界 探索更有趣的生活|来小世界 探索更有趣的生活 1 关注我|来小世界 探索更有趣的生活 关注我',
        '纨绔的游戏，不知道正义能不能到来',
        '严打之下，应该没有保护伞。恶魔，早点得到应有的报应。',
        '父母什么责任？？你24小时跟着你14岁的孩子的吗？',
        '我要当父亲别说三个了，他三家人都要去团聚[抠鼻][抠鼻]',
        '不是有意违规',
        '怎么就违规了，违规，违规，违规，违规，违规，违规，违规，违规，违规，违规，违规，违规，违规'
    ]

    rst = get_ngram_idf(data, split_method='jieba', idf_method='log')
    for _k, _v in rst.items():
        print(_k, _v)

    rst = get_ngram_tf(data, split_method='jieba')
    for _k, _v in rst.items():
        print(_k, _v)
