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
import time
from os import path
from tqdm import tqdm
from collections import defaultdict
import re
import warnings
import jieba.analyse
from typing import List, Any, Tuple
from aitool import DATA_PATH, is_all_chinese, get_most_item, load_lines, dump_pickle, load_pickle, exe_time, \
    np2list, get_aitool_data, de_sim, char_sim, VectorSim, pip_install, singleton
from aitool import split_punctuation
from aitool.r4_nlp.sentiment_analysis.dict_match import Sentiment
from random import random


@singleton
class KeywordGraphTool():
    """
    用与优化函数的运行时间，仅第一次执行时加载
    """
    def __init__(self):
        print('init KeywordGraphTool')
        # 加载自定义词典，以避免一些不合适的分词
        cut_word = load_lines(path.join(DATA_PATH, 'cut_word.txt'))
        for w in cut_word:
            jieba.add_word(w)
        self.tfidf = jieba.analyse.TFIDF()
        self.split_method = self.tfidf.tokenizer.cut
        jieba.analyse.set_stop_words(path.join(DATA_PATH, 'stopwords.txt'))
        self.keyword2score = {
            'keyword.pkl': load_pickle(get_aitool_data('keyword.pkl'))
        }
        self.deny_word_set = set(load_lines(path.join(DATA_PATH, 'deny.txt')))

    def get_jieba_method(self):
        return self.tfidf, self.split_method

    def get_keyword2score_default(self, name='keyword.pkl'):
        return self.keyword2score[name]

    def get_deny_word_set(self):
        return self.deny_word_set


def get_keyword(text, method='idf', top=10000, pos=('ns', 'n', 'vn', 'v')) -> dict:
    """
    获取关键词和权重
    :param text:
    :param method:
    :param top:
    :param pos:
    :return:
    """
    keyword2score = {}
    if method == 'idf':
        extract = jieba.analyse.extract_tags(text, topK=top, withWeight=True, allowPOS=pos)
    elif method == 'textrank':
        extract = jieba.analyse.textrank(text, topK=top, withWeight=True, allowPOS=pos)
    else:
        extract = []
    for key, score in extract:
        keyword2score[key] = score
    return keyword2score


def get_fragment():
    # TODO 目前在get_keyword_graph里是直接用两个相邻关键词选择fragment
    # 需将此模块独立，支持不同的拼接方案：相邻的多个词、隔x个字的词
    pass


def connect(relation, weights):
    # 保证relation可以构成连通图
    try:
        import networkx as nx
    except ModuleNotFoundError as e:
        pip_install('networkx >= 2.6.3')
        import networkx as nx
    G = nx.Graph()
    for node1, node2, _ in relation:
        G.add_node(node1)
        G.add_node(node2)
        G.add_edge(node1, node2)
    graphs = list(nx.connected_components(G))
    if len(graphs) == 1:
        return relation
    for i in range(len(graphs) - 1):
        node1 = list(graphs[i])[0]
        node2 = list(graphs[i + 1])[0]
        weight = weights[node1] + weights[node2]
        relation.append([node1, node2, weight])
    return connect(relation, weights)


@exe_time(print_time=True)
def get_relation(nodes, num_connected=0):
    relation = []
    valid_nodes = nodes if num_connected == 0 else nodes[:num_connected]
    len_node = len(valid_nodes)
    for i in range(len_node):
        for j in range(i + 1, len_node):
            if j - i < 30:
                if random() < 1 / 30:
                    relation.append([valid_nodes[i][0], valid_nodes[j][0], valid_nodes[i][1] + valid_nodes[j][1]])
            else:
                if random() < 1 / (10 + 20 * i / 30):
                    relation.append([valid_nodes[i][0], valid_nodes[j][0], valid_nodes[i][1] + valid_nodes[j][1]])
    # 是否保证无子图
    if num_connected > 0:
        weights = dict()
        for node in valid_nodes:
            weights[node[0]] = node[1]
        connect(relation, weights)
    return relation


@exe_time(print_time=True, print_key='show_exe_time')
def keywords_filter(texts, keyword2score, keyword_filter_type, show_exe_time=True):
    # TODO: 装包+下载+加载总时间<10s，是否下载到本地，离线安装和加载
    if keyword_filter_type == 0:
        return keyword2score
    try:
        import text_cutter
    except ModuleNotFoundError:
        pip_install('https://luban-source.byted.org/repository/scm/search.nlp.libcut_py_2.3.0.52.tar.gz')
        import text_cutter
    cutter = text_cutter.load('libcut/zh_v19')
    pos = text_cutter.load('pos/zh_20201212_conv')

    article = []
    for text in texts:
        text = re.sub('@.*?[ ,.?!，。？！]', ' ', text)
        article.append(text)
    article = '\n'.join(article)
    words_s, words_l = cutter.segment(article)
    word_valid = []
    for val in set(words_l):
        if len(val) < 2 or not is_all_chinese(val):
            continue
        word_valid.append(val)
    if keyword_filter_type == 1:
        target = ['NR', 'NT', 'NN']
    elif keyword_filter_type == 2:
        target = ['NR', 'NT', 'NN', 'VV']
    else:
        raise NotImplementedError('Keyword_filter_type only support [0, 1, 2] currently!')

    word_pos_ori = pos.pos(word_valid)
    word_pos = [val[1][0] for val in word_pos_ori if len(val[1]) == 1 and val[2] in target]
    word_pos_set = set(word_pos)
    keyword2score_new = dict()
    for k, v in keyword2score.items():
        if k not in word_pos_set:
            continue
        keyword2score_new[k] = v

    return keyword2score_new


@exe_time(print_time=True, print_key='show_exe_time')
def get_keyword_graph(
        texts: List[str],
        split_method=None,
        top=10000,
        pos=('ns', 'n', 'vn', 'v'),
        use_short=False,
        short_weight=1.0,
        new=1.0,
        default_keyword=False,
        keyword_dict=None,
        deduplication=False,
        deny_word=True,
        fix_deny_fragment=True,
        max_len=10,
        min_count=3,
        score_negative=1.0,
        score_positive=-0.1,
        num_connected=0,
        sim_method=None,
        sim_threshold=0.97,
        sim_cut=1000,
        keyword_filter_type=0,
        keyword_skip_limit=0,
        all_chinese=True,
        track_all_keyword=True,
        track_head_end_keyword=False,
        track_head_end_distance_keyword=False,
        head_end_distance_smooth=3,
        show_detail=True,
        show_exe_time=True,
        skip_de_sim=False,
        skip_novelty=False,
        skip_graph=False,
) -> Tuple[List, List, Any]:
    """
    输入一组文本。提取关键词和边。
    :param texts: 一组文本
    :param split_method: 分词方法
    :param top: 保留原始keyword的个数
    :param pos: 保留原始keyword的词性
    :param use_short: 保留短词
    :param short_weight: 短词的权重，权重越高短词排序越靠前
    :param new: 新颖性得分权重
    :param default_keyword: False时从输入的文本中计算关键词，True时用实现计算好的（此时deduplication无效）。
    :param keyword_dict: 非None时，直接用输入的关键词和分数
    :param deduplication: 对输入的文本去重
    :param deny_word: 是否向词表中加入所有否定词
    :param fix_deny_fragment: 是否补齐短语前的否定词
    :param max_len: 短语的最大长度
    :param min_count: 短语至少重复出现min_count次
    :param score_negative: 负向情感加分
    :param score_positive: 正向情感加分
    :param num_connected: 保证前num_connected个全连通
    :param sim_method: 计算文本相似度的方法
    :param sim_threshold: 显示度的阈值
    :param sim_cut: 只考虑前sim_cut个词
    :param keyword_filter_type: 0: 默认值，不二次筛选; 1: 筛选出名词; 2: 筛选出名词和动词
    :param keyword_skip_limit: 用关键词两两构建长词是，运行2个关键字之间跳过的关键词数量
    :param all_chinese: 要求输出的词全部由汉字构成
    :param track_all_keyword: 将所有关键词记录为特征
    :param track_head_end_keyword: 将首尾关键词记录为特征
    :param track_head_end_distance_keyword: 将首尾关键词及其距离记录为特征
    :param head_end_distance_smooth: 计算距离时的平滑参数
    :param show_detail: print出一些提示信息
    :param show_exe_time: 是否输出运行时长
    :param skip_de_sim: 跳过de_sim流程
    :param skip_novelty: 跳过新颖性得分流程
    :param skip_graph: 跳过建图流程
    :return: 节点表，边表，附加信息
    """
    # 选用分词方法
    if split_method is None:
        kgt = KeywordGraphTool()
        tfidf, split_method = kgt.get_jieba_method()

    # 选用相似度方法
    if sim_method == 'char':
        sim_method = char_sim
    elif sim_method == 'vector':
        vs = VectorSim()
        sim_method = vs.sim
    elif sim_method is None:
        sim_method = char_sim

    # sim_cut
    if sim_cut is None:
        sim_cut = 100000

    # 初始化情感分析方法
    stm = Sentiment()

    # 确保texts里都是字符串
    texts = list(map(str, texts))

    # 记录key的相关信息
    keyword_filtered = set()
    keyword2count = defaultdict(int)
    keyword2sentence = defaultdict(list)
    keyword2sentiment = {}
    keyword2sentiment_negative = {}

    tb = time.time()
    if keyword_dict is None and default_keyword is False:
        if deduplication:
            texts = list(set(texts))
        concat_text = '\n'.join(texts)
        if show_detail:
            print('sentence:', len(texts), 'char', len(concat_text))
        keyword2score = get_keyword(concat_text, top=top, pos=pos)
    else:
        if default_keyword:
            kgt = KeywordGraphTool()
            keyword2score_all = kgt.get_keyword2score_default()
        else:
            keyword2score_all = keyword_dict
        keyword2score = dict()
        meet_word = set()
        for sentence in tqdm(texts, 'select default keyword', disable=not show_detail):
            meet_word |= set(list(split_method(sentence)))
        for k, v in keyword2score_all.items():
            if k in meet_word:
                keyword2score[k] = v
    te = time.time()
    if show_detail:
        print('load keyword2score', te - tb)

    keyword2score = keywords_filter(texts, keyword2score, keyword_filter_type, show_exe_time=show_exe_time)

    keyword_set = set(list(keyword2score.keys()))

    # 作为单独输出的短词，要求全中文
    for kw in tqdm(keyword_set, 'filter keyword', disable=not show_detail):
        if not is_all_chinese(kw):
            continue
        keyword_filtered.add(kw)
        sentiment_score = stm.score(kw)
        keyword2sentiment[kw] = abs(sentiment_score)
        keyword2sentiment_negative[kw] = 0
        if sentiment_score == -1:
            keyword2sentiment_negative[kw] = 1

    # 导入否定词,并给定一个固定的分数
    kgt = KeywordGraphTool()
    deny_word_set = kgt.get_deny_word_set()
    if deny_word:
        for word in deny_word_set:
            if word not in keyword2score:
                keyword2score[word] = 0.1
        keyword_set = keyword_set | deny_word_set
    keyword_len = len(keyword_set)
    keyword2id = {}
    id2keyword = {}
    for _id, _k in enumerate(keyword_set):
        keyword2id[_k] = _id
        id2keyword[_id] = _k
    if show_detail:
        print('keyword_len', keyword_len)
    # 记录keypair的相关信息
    keypair2distance = defaultdict(list)  # 两个关键词间的距离
    keypair2id = {}
    keypair2fragment = defaultdict(list)
    keypair2sentence = defaultdict(list)
    keypair_score_sum = defaultdict(int)
    for sentence in tqdm(texts, 'connect keypair', disable=not show_detail):
        sp = list(split_method(sentence))
        # 记录关键词的信息
        kw_record = set()  # 避免重复记录到keyword2sentence

        # 处理1个关键词
        for kw in sp:
            if kw in keyword_filtered:
                keyword2count[kw] += 1
                if kw not in kw_record:
                    kw_record.add(kw)
                    if len(keyword2sentence[kw]) < 10:
                        keyword2sentence[kw].append(sentence)

        # 处理2个关键词
        # 计算关键词的下标位置
        sp_pos = [[sp[i], len(''.join(sp[:i]))] for i in range(len(sp))]
        sp_word = set(sp)
        word_select = sp_word & keyword_set
        sp_pos_select = [[_k, _p] for _k, _p in sp_pos if _k in word_select]
        # 统计单各词直接的有向共现
        # TODO：用于计算词之间是否建边
        # keyword_relation = [[0] * keyword_len for _ in range(keyword_len)]
        # for i in range(len(sp_pos_select) - 1):
        #     for j in range(i + 1, len(sp_pos_select)):
        #         wi = keyword2id[sp_pos_select[i][0]]
        #         wj = keyword2id[sp_pos_select[j][0]]
        #         keyword_relation[wi][wj] += 1
        # 构建组合词, 组合两个不同的关键词
        for i in range(len(sp_pos_select) - 1):
            for j in range(i+1, len(sp_pos_select)):
                if j - i - 1 > keyword_skip_limit:
                    continue
                if sp_pos_select[i][0] == sp_pos_select[j][0]:
                    continue
                fragment = sentence[sp_pos_select[i][1]:sp_pos_select[j][1] + len(sp_pos_select[j][0])]
                # 检查fragment前的否定词,仅考虑最多3个词
                if fix_deny_fragment:
                    if sentence[max(sp_pos_select[i][1] - 3, 0):sp_pos_select[i][1]] in deny_word_set:
                        fragment = sentence[max(sp_pos_select[i][1] - 3, 0):sp_pos_select[i][1]] + fragment
                    elif sentence[max(sp_pos_select[i][1] - 2, 0):sp_pos_select[i][1]] in deny_word_set:
                        fragment = sentence[max(sp_pos_select[i][1] - 2, 0):sp_pos_select[i][1]] + fragment
                    elif sentence[max(sp_pos_select[i][1] - 1, 0):sp_pos_select[i][1]] in deny_word_set:
                        fragment = sentence[max(sp_pos_select[i][1] - 1, 0):sp_pos_select[i][1]] + fragment
                # 仅保留全中文的短语
                if all_chinese and not is_all_chinese(fragment):
                    continue
                # 去除过长的短语
                if len(fragment) > max_len:
                    continue
                # 记录特征的方式
                kp_distance = -sp_pos_select[i][1] - len(sp_pos_select[i][0]) + sp_pos_select[j][1]
                if track_all_keyword:
                    kp = ''.join([sp_pos_select[k][0] for k in range(i, j+1)])
                elif track_head_end_keyword:
                    kp = sp_pos_select[i][0] + sp_pos_select[j][0]
                elif track_head_end_distance_keyword:
                    kp = sp_pos_select[i][0] + sp_pos_select[j][0] + int(kp_distance/head_end_distance_smooth)
                else:
                    kp = ''.join([sp_pos_select[k][0] for k in range(i, j+1)])
                if len(kp) < 1:
                    sddd = 1
                keypair2distance[kp].append(kp_distance)
                # 记录keypair和keyword的关系
                keypair2id[kp] = (keyword2id[sp_pos_select[i][0]], keyword2id[sp_pos_select[j][0]])
                keypair2fragment[kp].append(fragment)
                if len(keypair2sentence[kp]) <= max_len:
                    keypair2sentence[kp].append(sentence)
                keypair_score_sum[kp] = keyword2score[sp_pos_select[i][0]] + keyword2score[sp_pos_select[j][0]]

    if show_detail:
        print('find keypair', len(keypair_score_sum))
    # keypair算特征
    keypair2times = {}
    keypair2distance_average = {}
    keypair2best_fragment = {}
    keypair2sentiment = {}
    keypair2sentiment_negative = {}

    for kp, (id1, id2) in tqdm(keypair2id.items(), 'analysis keypair', disable=not show_detail):
        # 出现次数
        keypair2times[kp] = len(keypair2distance[kp])
        # 平均距离
        keypair2distance_average[kp] = sum(keypair2distance[kp])/keypair2times[kp]
        # 最频繁段短语
        if all_chinese:
            keypair2fragment_chinese = [_ for _ in keypair2fragment[kp] if is_all_chinese(_)]
            keypair2best_fragment[kp] = get_most_item(keypair2fragment_chinese)
        else:
            keypair2best_fragment[kp] = get_most_item(keypair2fragment[kp])
        # 情感倾向
        keypair2sentiment_negative[kp] = 0
        if stm.score(id2keyword[keypair2id[kp][0]]) == -1:
            keypair2sentiment_negative[kp] += 1
        if stm.score(id2keyword[keypair2id[kp][1]]) == -1:
            keypair2sentiment_negative[kp] += 1
        keypair2sentiment[kp] = abs(stm.score(id2keyword[keypair2id[kp][0]])) + \
                                abs(stm.score(id2keyword[keypair2id[kp][1]]))
    # 对特征汇总并计算排序分
    # all_feature 里仅在最后加新特征，不要改动前面特征的顺序
    # TODO 这种数据结构不好
    tb = time.time()
    all_feature = []
    keypair2rank_score = {}
    for kp in keypair2id.keys():
        keypair2rank_score[kp] = 0
        keypair2rank_score[kp] += keypair_score_sum[kp]
        if keypair2times[kp] > 100:
            keypair2rank_score[kp] += 0.8
        elif keypair2times[kp] > 10:
            keypair2rank_score[kp] += 0.3
        keypair2rank_score[kp] += keypair2sentiment_negative[kp] * score_negative
        keypair2rank_score[kp] += (keypair2sentiment[kp] - keypair2sentiment_negative[kp]) * score_positive
        all_feature.append([kp, keypair2sentence[kp], keypair_score_sum[kp], keypair2times[kp],
                            keypair2distance_average[kp], keypair2best_fragment[kp], keypair2sentiment[kp],
                            keypair2sentiment_negative[kp], keypair2rank_score[kp]])

    # 加入短词
    if use_short:
        keyword2rank_score = {}
        for kw in keyword_filtered:
            keyword2rank_score[kw] = keyword2score[kw] \
                                     + 0.8 if keyword2count[kw] > 100 else 0.3 if keyword2count[kw] > 10 else 0 \
                                     + keyword2sentiment_negative[kw] * score_negative\
                                     + (keyword2sentiment[kw]-keyword2sentiment_negative[kw]) * score_positive
            keyword2rank_score[kw] = keyword2rank_score[kw] * short_weight
            all_feature.append([kw, keyword2sentence[kw], keyword2score[kw], keyword2count[kw],
                               0, kw, keyword2sentiment[kw],
                               keyword2sentiment_negative[kw], keyword2rank_score[kw]])

    # 排序
    all_feature.sort(key=lambda _: _[8], reverse=True)
    # 下标映射
    kp2feature_idx = {}
    for idx, kpl in enumerate(all_feature):
        kp2feature_idx[kp] = idx
    te = time.time()
    if show_detail:
        print('time collect all_feature @%.3fs' % (te - tb))

    # 筛选
    tb = time.time()
    keypair_selected = []
    keypair_selected2rank_score = {}

    # 计算显著重复的keypair2best_fragment
    best_fragments = [kpl[5] for kpl in all_feature]
    if skip_de_sim:
        de_sim_selected, de_sim_detail = best_fragments[:sim_cut], {}
    else:
        de_sim_selected, de_sim_detail = de_sim(best_fragments[:sim_cut], method=sim_method, threshold=sim_threshold)

    for idx, kpl in enumerate(all_feature):
        kp = kpl[0]
        kp2feature_idx[kp] = idx
        # 去除有显著重复的短语
        if kpl[5] not in de_sim_selected:
            continue
        # 去除出现次数过少的短语
        if kpl[3] < min_count:
            continue
        keypair_selected.append(kp)
        keypair_selected2rank_score[kp] = kpl[8]
    if show_detail:
        print('select keypair', len(keypair_selected))
    te = time.time()
    if show_detail:
        print('time de-similary @%.3fs' % (te - tb))

    # 对入选的词做新颖性加分
    if skip_novelty:
        keypair_selected_new = [[kp, score] for kp, score in keypair_selected2rank_score.items()]
        keypair_selected_new.sort(key=lambda _: _[1], reverse=True)
    else:
        tb = time.time()
        keypair_selected_new = []
        word_count = defaultdict(int)
        word_whole = 0
        for kp, score in keypair_selected2rank_score.items():
            word_count_avg = (word_whole + 1) / (len(word_count) + 1)
            new_score = 0
            for _char in kp:
                if word_count[_char] < word_count_avg:
                    new_score += 1 - word_count[_char] / word_count_avg
                word_count[_char] += 1
                word_whole += 1
            new_score /= len(kp)
            new_score *= new
            keypair_selected_new.append([kp, keypair_selected2rank_score[kp] + new_score])
        keypair_selected_new.sort(key=lambda _: _[1], reverse=True)
        te = time.time()
        if show_detail:
            print('time novelty @%.3fs' % (te - tb))

    # 整理出node表
    node = []
    for kp, score in keypair_selected_new:
        kp_feature = all_feature[kp2feature_idx[kp]]
        node.append([
            kp_feature[5],  # keyword or keypair
            kp_feature[8],  # 综合score
            kp_feature[1],  # 详情信息
            kp_feature[3],  # 出现次数
            kp_feature[2],  # tfidf score
        ])

    # 构建边
    if skip_graph:
        relation = []
    else:
        relation = get_relation(node, num_connected=num_connected)
    return all_feature, node, relation


@singleton
class SentenceKeyword():
    # 用于做单句的处理，以废弃，改用filter_words_with_pos
    def __init__(self):
        warnings.warn("推荐使用filter_words_with_pos", DeprecationWarning)
        # self.keyword2score = load_pickle(path.join(DATA_PATH, 'keyword.pkl'))
        self.keyword2score = load_pickle(get_aitool_data('keyword.pkl'))
        print('len keyword', len(self.keyword2score))
        tfidf = jieba.analyse.TFIDF()
        self.split_method = tfidf.tokenizer.cut

    @classmethod
    @exe_time(print_time=True)
    def update_keyword(cls, doc_file, top=1000000):
        texts = load_lines(doc_file)
        print('len corpus', len(texts))
        concat_text = '\n'.join(texts)
        keyword2score = get_keyword(concat_text, top=top)
        dump_pickle(keyword2score, path.join(DATA_PATH, 'keyword.pkl'))

    def get_sentence_keyword(self, sentence, not_empty=False, use_label=True, **kwargs):
        # 提取fragment
        _, node, _ = get_keyword_graph(
            [sentence],
            split_method=self.split_method,
            keyword_dict=self.keyword2score,
            min_count=1,
            **kwargs,
        )
        rst = [n[0] for n in node]
        if not_empty and len(rst) == 0:
            # 取标签
            if use_label:
                label_text = sentence.split('#', 1)
                if len(label_text) >= 2:
                    label_ori = label_text[1].split('#')
                    for _l in label_ori:
                        strip_l = _l.strip()
                        if len(strip_l) > 0:
                            rst.append(strip_l)
            if len(rst) == 0:
                pieces = split_punctuation(sentence)
                if len(pieces) >= 1:
                    return rst.append(split_punctuation(sentence)[-1])
                else:
                    return rst.append(sentence[:6])
        return rst


def get_keyword_graph4panda(info, **kwargs):
    # info 的格式为comment_id	group_id	text
    # todo 计算vv的逻辑可以优化
    # 格式处理
    info_list = np2list(info)
    texts = []
    text2info = {}
    for comment_id, group_id, vv, text in info_list:
        if text != text:  # NaN
            continue
        if text == '':
            continue
        texts.append(text)
        if vv == 'NULL':
            vv = 0
        elif vv != vv:  # NaN
            vv = 0
        else:
            vv = int(vv)
        text2info[text] = (comment_id, group_id, vv)
    # 调用标准的方法
    rst, node, rel = get_keyword_graph(texts, **kwargs)
    # 统计vv
    node_detail = []
    for kp, rank_score, sents, times, score_sum in node:
        svv = 0
        detail = []
        for _text in text2info.keys():
            if kp in _text:
                svv += text2info[_text][2]
        for sent in sents:
            if sent in text2info:
                detail.append({'text': sent, 'comment_id': text2info[sent][0], 'group_id': text2info[sent][1]})
        node_detail.append([kp, rank_score, svv, detail])
    rel_rs = get_relation([[n[0], n[1]] for n in sorted(node_detail, key=lambda _: _[1], reverse=True)],
                          num_connected=kwargs.get('num_connected', 0))
    rel_vv = get_relation([[n[0], n[2]] for n in sorted(node_detail, key=lambda _: _[2], reverse=True)],
                          num_connected=kwargs.get('num_connected', 0))
    return node_detail, rel, rel_rs, rel_vv


if __name__ == '__main__':
    # SentenceKeyword()
    # from aitool import load_excel, dump_excel

    # 更新词表
    # SentenceKeyword.update_keyword('./mini.csv')

    # 测试批量生产
    # data = [
    #     '纨绔的游戏，不知道正义能不能到来',
    #     '严打之下，应该没有保护伞。恶魔，早点得到应有的报应。',
    #     '父母什么责任？？你24小时跟着你14岁的孩子的吗？',
    #     '我要当父亲别说三个了，他三家人都要去团聚[抠鼻][抠鼻]',
    #     '不是有意违规',
    #     '怎么就违规了'
    # ]

    # from aitool import get_keyword_graph
    # data = [
    #     "唉，你好，你那边声音能不能大一点？。噢，我那个抖音账号无缘无故被封禁了，我什么东西都没有发他给我那个上面搞个医疗保险。。对对对，我都没发那个东西，他说我涉嫌违规的什么。。你那个有申诉过？申诉不通过。。我都没发他，无缘无故他给我那个抖音号给我封了。。已被封禁！。你肯定不理想我，关键是我什么都没发。。没有发昨天哪里有发？啥都没发。。对，昨天都没发，无缘无故他那个给我那个账号被封了。就是昨天嘛。。不是你，关键你现在是要查一下我到底发了没发，我就是没有发，他无缘无故给我那上面搞个医疗保险，我都没发过。我上一次以前发过，已被封禁，然后我都没敢再发，他无缘无故我玩一个抖音发个自己的那个，为了他被就这样被封了。。我知道那个抖音平台，关键是没有方案的，无缘无故把人家那个账号封了，这个属于什么情况？。我知道如果我违规行为，我关键是没在这个抖音上发布，就是这个号，这个账号，一八五这个账号都都没有发过那个东西，他他被封了。嗯，我在快手，不是，我在那个快手平台，那快手平台这个抖音没有前面对不对？。没有了！。所以说，。啊，那你看吧，你这个平台怎么弄的，弄的胡乱封号。。唉呀，你看看能不能截一下嘛！看看能不能截一下嘛！。就是18559691329这个号码。。嗯，你看一下什么时候能解试一下。我都关键是没有发过作品的无缘无故给我封了。。嗯，好的好的，你看一下是什么情况啊？。四、九。。嗯嗯，好。",
    #     "唉，你好，我问一下那个昨天晚上一个抖音号那个是说是违反什么社区什么什么规定啊，被禁言，那是什么时候能解封啊？。不是另一个手机号。。啊对，是我。。哎你，你帮我看我这个手机号的账号是怎么回事？他是被永永久性永久性封啊还是怎么回事？。唉，好嘞。。他这个封禁能不能解了？。不会。。不申诉了不也不会申诉，但是自己申诉了好几次，然后都通过不了，我不知道申诉不合适还是怎么回事。。我是看了他确实是违反人家的规定啊，说什么健康啊之类的，有什么违反广告啊之类的，所以说这。但是现在这个抖音号打开以后，我的以前发的视频就看不到。。两一年多了。。噢！。噢，行了行了，唉，我想问一下，一般情况下一直今年，那个今年的话是多少钱就能接好了？。短期都是几天。。噢，因为今年很多功能都不能用了吗？就是留言发发，看视频留言都不能留。。我是我主要是发一些东，发一些什么养生这些东西吧。那那那些也违反规定啊！。噢噢噢！。哎呀，估计是估计截图截的人家哪个地方你闹的，好像就把它下载下来再发，发布到微信里头啊，抖音里头是不是应该有什么字体啊，咱也没看，就是因为这些原因涉及的这这这些违反规定啊，医疗啊这些。。嗯？什么样的情况下能发？能发这些？你们需要注册啊还是？。个人医疗认证是个人认证，怎么个认证法？。好嘞！好嘞！好嘞！。唉，行了好嘞。。嗯，好，那没有别的问题了。嗯。。那没有了。。唉好的好的。。嗯，好的好的。。嗯嗯！。嗯，再见。",
    #     "你好，我想问一下，我这个号他怎么动不动就又给我封广告，就我又没有发广告，有个视频呢，我也没发，怎么动不动就给我封掉了，又封又封，三天五天，然后四五天。。是啥子？。不是这个账号，是另外一个我，我告诉你是那个嗯，4713的。。那我告诉你电话号码呀，或者说抖音账号。。嗯。。那我问一下你们，你们怎么这个这个这个老是动不动就又又给封号了，我的作品都没有发。。他是私信功能，这个封禁。。不是他，我没有那个什么呀，我又没有怎么去回人家，回都没回一下，就是这个莫名其妙，然后又给封封了，每次都是这样子。。那作品那，那之前那我都好久都没有发过了，怎么你要不就一次性就把那些是吧这个这个作品，然后就给我不适宜公开了，那为什么我等两天又来一个，等两天又又说不行，那都多少多久发过的视频呢？那个这个去年的11月发的作品呢？到现在，然后说不行，那之前发的时候怎么说呢？是的。。就是昨，呃前天呢？呃昨天，呃前天，对。。就是发的那个什么？嗯，就是写的那个？就是普及的24岁就漏尿的那个！那关键是十一月份发的呢？那到现在我跟你讲这都几月份了？二月份了！。每次都是这样子，你们这个我所有的作品都是都是这个去年的作品了，也要审核通过审核做做作品的通知，结果呢，这个一出现，那个就封我号。。那都是多少多少去年的东西了，那你要么一次性就把这些问题是吧，这作品说不行一次性就不适宜公开就得了嘛，过两天又封过两天又封。。我关键是我都没有发作品啊！我现在。。那你那你如果是说不行对吧，这个视频不行，那你就一次性就那个弄完它吗？。而且又没有说发，发只是就是普及的，又没有发什么。。又没有说那个发什么东西对不对，只是一个知识普及的东西。。就是那个呃，说了一些这个嗯，产后用料的问题啊，那又没有说什么东西。。没有啥专业订单呀，就就是就是一个异常的问题啊，产后的一些问题啊，就讲了一些这种啊。。他是普及知识，那人家都不到很多都是这种普及的吗？那人家怎么没有什么事呢？。那你就如果是这样子的话，就你就一就是不要你看十一月份的作品了。那现在二月份，那之前怎么说不行呢？现在怎么说？说是又那个什么之前就行，现在又不行了？。那都多久了对不对，都十一月份呢。。那你如果说这样子的话，你就不要动不动的对吧？这个这个又又要给我封呗？。那有问题？那你就是那就很奇怪那多久了对吧？然后你就说多次这个对吧？那你就一次性就搞完嘛。。你不行，那你就直接这个这个不适宜公开不就行了，我就把它删掉就行了吗？。哎呦，我真是无语了什么？。这都作品都没有发，刚剪出来一天，什么东西都没有发，又给我这个又又来个15天。。是不是每次都是这这这这样子搞？。那你。。那怎么之前又又不说呢？。不是说我不了解，根本原因呢是你们这个这个你要是一次性就弄完嘛，不要老是整一下又整一下对不对？而且的话我当时多久的时候发的都没问题。。那这个问题怎么解决呢？就一直就这样子封封封吗？。我都没有，我都没有发发作品啊大哥我你看一下我账号有多久没发作品了？对，你们老是这样子审核审核，我一直都没有发作品了！。我之前发过，那是去年的事情呢。。那你们就不能改变一下吗？就一次性就搞完吗？。什么？就是某一个？那你们都是这样子的吧？。如果说我是这样子的，大家都是这样子，什么叫做某一个改变，那就不能调整一下吗？你们这个不是有问题吗？那到底还玩不玩了这抖音？。那你讲这个是什么意思呢？那你们就不能去那个那个去去调整一下吗？这就有问题啊，都接受不了别人的意见吗？。这个东西不是说。。这个东西不是说是我一个人，而是大部分的我只是只是这个这个用户当中，这种用户当中的某一个之一而已，不是说为我某一个人而为我来去改变你的规则，不是的，那我现在是跟你们说这个是不是可以调整的，这个问题本身就已经已经这个影响了别人的使用，使用的时候，那抖音本身就是就是一个平台嘛，对不对？那你要去接受体用户的一个体验那？。那我在不发违规的情况下，那我本身我就没有发这个东西啊，对不对？我又没有发，我也没有说啊发广告啊什么的。。账号有问题那是那是之前之前发我好久都没有发过作品了，就是你们老是动不动就给我就是刚给他昨天解出来的又封，刚解出来又又封。。那你那是不这还怎么怎么用这个？呃，用抖音啊，对不对？那同样的，你们也是也是这个想把抖音去做好，然后的话，那你们也有有去接广告，也去做这个生意，那你们这个做大都不让大家来去玩了，那还怎么弄？。不是说你这个问题是普遍的都是这样子的。不是说，只是说针针对我。。那我哪是你就比如说这个东西是吧，那多久的作品了，我每次这个你要不要，是当时不行就不行吗？而且的话那你已经处罚过了，你就不要弄一个，然后又又给封，那还怎么用抖音怎么怎么去使用感受好呢？。他刚刚封我三天，然后写出来就给我封15天。。对呀，就是就是，又是那个什么不适宜公开呀！。可是，可是他每一次都是作品。嗯，这个审核通知之后，然后第二天就给我封了。。哎。。我昨天解出来之后我没有任何评论别人，然后那个别人一点那个我也没有回别人什么东西，就一个都没有，你可以去去进我账号去看一下都可以。。我都没跟人聊天呢！。禁言！。可是我你你说我私信有问题我都那个人家也没人来找我我也没跟人家私信啥的我也没回人家什么的然后我我这个就是前天前天的时候呢他他给我这个作品审核了然后呢这个反正每一次都是这样子只要有作品审核然后过个一天等到第二天24小时之后肯定立马遇到我点。。几年了？。作品也不能发，然后。。什么故意？那你们这个就是有问题啊。对啊。。我知道啊，那那就是你们现在的这个现在，现在这个这个就是有问题吗？你们这个操作就是有问题的。。不是，你们现在就是有问题啊，你们这个操作不是有问题吗？我现在我的这个这个作品都不发，我作品都不发，我就是发一个这个自拍的，那有什么问题呢？我也不发漏的，那你后期还要封我啥呢？我就不明白了。。我早就删了呀，那天你们一审核我就把这个作品删掉了。嗯嗯嗯？。有作品啊，我都发了几百个作品。。意思就是要把我把所有的作品删掉。。那你。。那那你那你那那我拿另外一个电话打还是还是怎么回事？我打给但是又不一定是你接的呀。。可是我等会又要重新去描述一遍不是吗？。对呀！。那那我那个那要不？。那意思就是只能只能用我那个号码打？那我把这个号码报给你，你可不可以打给我嘞？。嗯。。那行吧嗯嗯嗯！。好，嗯。。嗯。。好好好，谢谢，嗯。。好好。。嗯。",
    #     "唉，你好，那个我想申请企业蓝 v， 然后呢？咱这边能帮助我吗？。哎？哪位？。啊，我知道我那个我就现在想了解一下吧，就是说现在的这个抖音的这个规则，社区规则，因为呢，原来呢就是说嗯，发视频不允许有医疗周边的对不对？。对呀，那我们认证认证的话，现在不是说之前是不给认证的嘛？。唉，对啊，之前就是医疗周边的，因为我是做那个培诊的啊，之前在咱这申请过，申请过呢，然后就是提交了500块钱，然后呢说是我这个是在培诊俩字，然后呢就是不能过，不能审核过。。唉不是我知道你你说的不就是电子那就是那个什么就是打字的那个客服吗？他他给我他给我回复的呢就是说啊有有那个专专人过来跟我联系专人跟我过来联系一直没联系过。。唉，对你们这个他说的这个专员专员呢，还是一个外包的企业，他还啥都不知道。。就是那那个啥，就是账号底下有个那个叫我的客服，然后呢，就一一直打客服一就一直就人工服务一直呃人工服务？他不就出来一个人工服务了吗？。对呀，他就出来一个电子的吗？。不是我知道对他出来的不也是就是以文字形式出来的客服吗然后你把问题发给他呢他说好的稍等我们那个这边呃会在官方时间有人给你你回复怎么样的给我打过来的呢就是一个外包的一个企业然后呢他只是说可以协助我办理协助我办理呢然后呢问他问题呢他还不知道因为这个东西吧我已经失败了一次已经就是给。。就给你们贡献了500块钱，然后呢？这次我就想，就是说怎么能把这个雷毕过去！。对，因为吧，现在我看规则应该是有所改动，因为吧，别的别就是其他的那个同行，他们已经申请通过了，我现在就想了解一下这个规则，现在是我应该是怎么办？。嗯。。噢，那就这个吧，那个就这个8818他绑定的是不是个集顺陪审同存。。啊对，他这个是绑定的是一个2334的一个账号对不对？。啊？那点开里面是几分陪整吗？这个是应该是吧？应该是，我看一下。。不管。。噢不对不对，是一三七。。啊，我我我们有好，我们有好多账号，然后呢就是说之前呢就是说用那个一八六的，有一个电话咨询的。。啊1175175。。啊？那那就是之前咨询过那个是不是啊？。噢，那你就那你还是记我这个吧！就我这个到时候让他给我回这个吧。。啊啊，1864357啊，我电话多少？。啊，18643578818。。对呀，抖音号的是848975239，但是这个他俩绑定的电话不是一个呀，没问题吗？。嗯，对对对。。哎。。啊，不算医疗，医疗周边，就是说做培训服务的，因为呢，之前呢就是说为什么说我失败的呢，他说是我第一个，我我的那个营业执照上面带的是病人服务。。啊，第二个呢，说是说在我的那个村里，上面是在集顺培诊，在培诊了，就这两点，他说是审核不过，但是呢现在呢，我感觉啊，我感觉现在应该是好像你们那个已经规则已经变了，因为呢我看别人就是说我们当地的啊，我看已经申请蓝 v 已经申请过了，而且是呢他的那个上面那个说你们也是在培训的，也是长春培训。。唉，对唉对蓝蓝 v 也是。然后呢？就给他。唉，给他已经置顶了。。对呀！。那我不，我不能二次上当了是不是啊头，头一次咱交学费了，不能第二次还交学费吧？。嗯，行，大概什么时候你给我打电话？。噢，行。。噢，行行那行。。啊没有了。好，谢谢。。嗯，好的。。那就这样。",
    #     "您好，我我问一下，那个就是直播三个人斗地主，怎么弄啊？。噢，就是就是，抖音是不可以那个就是直播那个，三个人打斗地主是吧？。那我说的意思就是那个抖音不让那个打，三个人打服了是吧，斗地主那种的。。噢，那行那好了，知道了。唉，那还有人打？",
    #     "，你好，尊敬的抖音官方审核员，您好，某某2022年7月我的抖音账号被封禁，封禁原因涉嫌医疗，恳请审核员明察，我并无涉嫌任何广告因素，如果真有存在违规，也绝对是无意触犯的，在此我深深的向您致歉，请求审核员给予我账号恢复正常，将封禁改为警告，我保证以后一定遵守“抖音网络社区自律公约”，共同维护良好的社区氛围，吸取教训，做一个诚实的公民，请官方审核员给予我一次机会将账号恢复正常！感激不尽。",
    #     "唉，您好，我想问一下，我的这个那个抖音账号也不知道因为什么原因被封了，咱们申诉了一次也没有，没有成功。。嗯？能不能给咱们对对？。就是你帮我弄，就是那个嗯，解开吧，我也啥也没弄，真的啥也没弄，就是中途有一次账号被盗了，盗过一次我又弄回来改了一下密码，后来没过几天我再登录的时候就不能用了，你帮我把它解封了以后，我我再重新设一个比较难一点的密码。。你看为啥我啥也没发过，也没发老发过评论，你看我的那个里边就发了几个孩子的日常生活呀，啥也没发吗？怎么就违规了呀？。噢噢，我真的没发，就发点孩子的，正常孩子们有时候玩的，发一个他们自己玩的那小视频啥也没发，真的，你帮我弄弄解封开了吧，我以后多注意一点。。对，咱们正常使用，尤其是现在孩子，有时候学校让你在抖音上看一下，啥呀？。我没弄呢，看看视频呀。啥？咱没有？没有多余的手机，有些都完成不了，老是那那些。。留着作业你真的帮帮忙给我弄开呗。。噢，那你帮我弄一下嗯？。麻烦你了，你帮我看一下啊。。没了，我就这一个要求！。嗯。。嗯。。好，谢谢你，嗯。。嗯，祝您生活愉快！",
    #     "就是我有一个账号，然后我不知道什么时候实名的问题，我记得我都没有实名过，然后现在我不是注册一个新的一个新的抖音号吗？然后我想实名的时候，发现还有另外一个号绑定我这个实名。。然后这个号我现在就是另外实实名，这个我还能登上，然后我突然就是我登上发现这个让人家我搞封禁了。。我知道啊。。问题是我。。我都不知道上面还有很多聊天这种东西，然后我都我都没有发过。。问题是我都不知道我。。未知的也不行吗？。我知道呀，就是他，我现在问题是我想把这个给注销了，然后问题是这东西他他那种什么就是涉嫌发布违规医疗健康内容，这些东西我都没发过呀，我我都不知道什么时候搞的。。如果我知道，我也我也不会去打电话给你们。。意思是解？不？你意思是这也解不开？然后我也不能去把这个号注销解解除实名对吧？。嗯，我服了。。我我知道呀，问题是我这些东西我都没发过然后实名我也不知道是谁给我搞的这种东西，不是说要你们说的那样就是不是我的不是本人都。。实名不了，我不知道，我都不知道。。啊！。嗯，好。。解？解除也解除不了，对吧？。我知道呀！。嗯，那行吧。。但是他这个手机号，。问题是这个号的。那我看一下啊。。像什么 f 七了，七 p 还有那种。。问题是这不是我的手机啊！。嗯。。服了，哎。。那好吧好吧。。嗯。",
    #     "医疗机构还可以入住抖音吗。医疗机构还可以入住抖音吗。对，三甲医院科室入驻。好的，谢谢",
    #     "账号相关问题。账号相关问题。是的。怎么操作呢。那上面显示的好像是永久封号。好的谢谢。我看一下。封禁处罚（账号/投稿/私信/评论/开播）。封禁处罚（账号/投稿/私信/评论/开播）。那上面显示的是是的。是的。那什么时候能解封呢[嘿哈]。大概得多长时间呀。啊。[流泪]。可是我妈妈也没发什么涉及违规的视频呢，为什么会被封[大哭]。现在好像也发不了作品呢。视频为什么会提示违规。没有呀[流泪][流泪][流泪]。就不知道怎么回事。就可以刷别人的抖音。私信也发不了。我妈妈发的平时也挺正能量的啊，就也不知道为什么。[衰][泣不成声]。封禁处罚（账号/投稿/私信/评论/开播）。害。我妈妈这个抖音号玩了很久了。注销也很…。真是很无语啊，怎么无缘无故违规也不知道啊。确实是没有啊。没有想要咨询的作品。没有啊，就正常的给别人点赞或者评论[赞][赞][赞][赞][赞]。真服了，莫名其妙就被封号了，这个抖音很也玩了挺久了。可是我妈妈发布的视频和评论也没涉及这样呀。裂开。她平时发的也挺积极向上的。作品。有解决办法吗。无语死了。视频状态查询",
    #     "对。我想咨询为什么突然就被封号啊。是哪个视频还是什么。希望可以重新检测一下！。可以注销重新创新创号嘛。或者有没有别的什么办法。那要被封禁到什么时候。可是并没有什么违规行为啊。就这样被封掉了吗。没有别的办法吗",
    #     "我没有推销任何医疗产品",
    #     "喂，你好，我想咨询一下，就是嗯，咱们不是和这个小和医生合作人吗？。小何医生，。小何医生，。我不是我认证的我嗯，那个没有我的选项。。对，因为我我不是个医生啊，我从小号医生 app 那个平台不是嗯，就是咱抖音官方认证那没有我的个人选项。。嗯。。嗯，就是他链接，不是链接上面抖音，抖音这个的话上面医疗医疗这个行业了进行认证，我因为进去了就没有，没有我的选项认证不了。。审核审核，医医生已经认证过了，现在在抖音上认证，现在没有我的选项。。对啊。。嗯，对。。因为我是个住院医了。。住院医生。。嗯。。噢，行。。嗯，对对，没有我，没有我他他只有院长了，主任，副主任了。主持人没有没有住院异地的环节，等一下。。嗯，我看医疗只有这个，只有这个认证呀。。嗯。。嗯嗯！。嗯，行，好的，嗯。。嗯嗯，没事，嗯。。嗯，好好。",
    #     "哪一点是有关医疗的仔细看看哪一点有关医疗，你给我圈出来，第三幅图是我另一个号上面发的同样的内容",
    #     "喂，你好你好噢！你这边的话我这边的账号私信和评论的啊，关注的这个被封了，就是为什么？。他说我诈骗我就对啊，我就正常评论，我关注多了，我就呃关注几个主播，然后在上面回复一下，然后就就把我封了，他说我诈骗了我我都不知道。。我就聊关注十个八个魔术他就把我封了，这个有什么问题吗？这样子关注人不行了吗？现在？。对对对对，你查一下我那个账号，就关注了几个博主，我喜欢的抖音博主，然后他就把我封了，说我不能关注，而且也不能私信，我就私信了一两个人。。我就想表我就对这个主播很喜欢嘛！我就我就把前期呃问一下主播最近怎么样，然后你就把我封了。我就我就私聊了两个，我就发了一句话你好，然后他就把我封了。。嗯嗯嗯！。噢噢，你查一下你查一下。辛苦了，帅哥。。嗯他说我发现我都不知道我我发个你好就就需要什么照片啊就是吧啊啊啊。。我你这是谈聊天记录？我就说你好，说你好帅！。我就是把我封了，我就把我这两句话。。嗯，对。。你查一下那些。。嗯，您说。。对啊。。嗯。。评论也不行？。嗯。。在直接买的有的啊，嗯。。问题是我没有！有没有看到行为啊！。主要是我没有这个行为啊！。大哥走了！。我没有说过这些，我什么都没说过。这些，这些我都没说过。我就我我就比如说我就发了一个私信的话，一个你好你好帅啊你没了。另外另外就我知道博主，我关注了一个博主，然后你就把我封了？。嗯，你这应该有记录，可以查得到的。。对！。那为什么我的被限制了呢？。我就这样子操作一下。。没有啊，问题是。。我这个问题是我没有啊，能帮我解封吗？啊？。但是，。噢？我该怎么做？你给我看一下。。啊？他抖音噢，稍微等一下啊。。啊？右下角什么？。你好啊！。好好好，你等我一下。。我这个电话号码是一八九。。啊啊对呀。。嗯。。噢，好的，189340011。。噢，我这个账号你把我封下来了。。对啊，我现在在不好的登录，我刚刚看到你看一下，你能帮我解封吗？。那，。他这边就是无法登录啊，就是你我这边该怎么做才能取消？呃，取消那个处罚？。等一下，等一下啊！。你等一下，我现在登录一下。。那我。。好，知道他说了。。嗯，行。。等一下啊！等一下啊。。那你这个吗？。行，好好好，我现在重新登录一下，等一下我嗯嗯好嗯，不好意思。。那我这边我到时候该怎么处理呢？我现在有点事要去忙。。噢！结束时间七天！三天！。噢，对他说我要七天！三天。。你？。这我知道我知道，但是我想解封开啊，但是不能这样子啊，我就评论一下你就把我封了，要是这个，。你你这个取消，你这个处罚是说我诈骗？那是我账号没有刷什么都会有这个标啊，你肯定要帮我取消啊，你帮我取消处罚，那我现在评论也评论不了，关注主播也关注不了，那我刷抖音干嘛呢？。我刷抖音就是看帅哥美女的吗？。对啊，我。。好吧。。提供。。那我评论为什么评论不了呢？。噢，我等一下，我看一下。你稍微等我一下下。我现在的一个处分是什么？有两个处分，一个是说我禁止私信功能，然后新发表评论仅自己可见。。就这两个处分！。对对对对！。是吧？。现在屏幕是正常的吗？。嗯，那我这边私信的功能你怎么帮我解除呢？。以前你这个对我账号直接说我诈骗的话，那对我的账号标签有问题啊！。行！。那我可以关注了吗？现在评论评论几次？。评论呢？。那那这个，你这个对我处罚了之后对我账号有什么影响啊？以后我开直播也不能开直播了。。我。。其他功能都是正常的，就是可以正常开播对吧？。以后我开播的话，对我的流量有处罚吗？。没有。。你确定啊？那好好，那就这样啊。。我可以也可以关注，暂时没了，谢谢。",
    #     "唉，你好，就是我我我，不知道为什么我的账号被封了。。嗯，他那个是违反违反社区规定。但是我已经有有有一个多月没有发作品了，一两个月没发作品了。。嗯，绑定的手机号码是一八一。。噢，需要需要需要需要绑定另外一个那个那个抖音的电话号码原电话号码才可以是吧？。好，那那您看一下我这个账号能解封吗？。嗯。。那我可以实名制释放吗？。实名也不能释放出来是吧？。嗯。。嗯，就是我您我我其他的账号也有，但是不是绑定的这个电话号码，你可以就是随便帮我查一下吗？。我姓顾。。嗯。。行行，我用另外一个电话号码打过来吧！。没有了，好的，谢谢您。。好好，谢谢你。",
    # ]
    #
    # _, n, r = get_keyword_graph(
    #     data,
    #     use_short=True,
    #     deny_word=False,
    #     max_len=12,
    #     keyword_skip_limit=1,
    #     all_chinese=True,
    #     track_all_keyword=True,
    #     top=1000,
    #     score_negative=0,
    #     deduplication=False,
    #     min_count=1,
    #     pos=(),
    #     sim_method='char',
    #     sim_threshold=0.97,
    #     skip_de_sim=True,
    #     skip_novelty=True,
    #     skip_graph=True,
    #     show_detail=True,
    #     show_exe_time=True,
    # )
    # for item in n:
    #     print(item)

    from aitool import get_stop_word
    print(get_stop_word())
    x = 1
    # jieba的分词结果
    # _tfidf = jieba.analyse.TFIDF()
    # _split_method = _tfidf.tokenizer.cut
    # for sent in data:
    #     print(sent)
    #     print(list(_split_method(sent)))

    # 标准的长词分词方案
    # _, n, r = get_keyword_graph(
    #     data,
    #     use_short=True,
    #     deny_word=False,
    #     max_len=6,
    #     top=5000,
    #     score_negative=0,
    #     deduplication=False,
    #     min_count=1,
    #     pos=(),
    #     sim_method='vector',
    # )
    # for _ in n:
    #     print(_)

    # 特别长的长词
    # _, n, r = get_keyword_graph(
    #     data,
    #     use_short=True,
    #     deny_word=False,
    #     max_len=12,
    #     keyword_skip_limit=3,
    #     all_chinese=True,
    #     track_all_keyword=True,
    #     top=1000,
    #     score_negative=0,
    #     deduplication=False,
    #     min_count=1,
    #     pos=(),
    #     sim_method='vector',
    #     sim_threshold=0.97,
    # )
    # print([_[0] for _ in n])

    # sk = SentenceKeyword()
    # for line in data:
    #     print(line)
    #     print(sk.get_sentence_keyword(line))

    # 单句处理模式，将多余的处理流程skip掉，一句话仅需要8ms
    # from aitool import filter_words_with_pos
    # sent = '唉，就是你退我款你受理，受理我3张没错，那我看了3张连着的就说退那个受理退款一一一张两张3张两三个，3个39块9，完了以后退款呢？是有一天退了一个39，我139块9，我再一问，他说过两天。'
    # _, n, r = get_keyword_graph(
    #     [sent],
    #     use_short=False,
    #     deny_word=False,
    #     max_len=12,
    #     keyword_skip_limit=1,
    #     all_chinese=True,
    #     track_all_keyword=True,
    #     top=1000,
    #     score_negative=0,
    #     deduplication=False,
    #     min_count=1,
    #     pos=(),
    #     sim_method='char',
    #     sim_threshold=0.97,
    #     skip_de_sim=True,
    #     skip_novelty=True,
    #     skip_graph=True,
    #     show_detail=False,
    #     show_exe_time=False,
    # )
    # rst = [x[0] for x in n]
    # print(rst)
    # f_rst = filter_words_with_pos(rst, show_detail=False)   # 默认
    # print(f_rst)
    # f_rst_2 = filter_words_with_pos(rst, show_detail=False, ths_target=0.8, ths_vv=0.5)     # 更强的过滤情况
    # print(f_rst_2)
    # f_rst_2 = filter_words_with_pos(rst, show_detail=False, ths_target=0.8, ths_vv=1.0)  # 更强的过滤情况
    # print(f_rst_2)
    #
    # from aitool import SentenceKeyword
    #
    # sk = SentenceKeyword()
    #
    # keyword_res = sk.get_sentence_keyword('。'.join([
    #     '转发点赞关注 我的微博视频号 Yuqi-214 来微博,观看更多视频 截图保存,查看二维码',
    #     '真是辣条[流泪], 2个[流泪], 别瞎看[微笑], 好家伙, 正经的小男生不敢开口[流泪], 锦鲤附体！, 加油[抱抱你], 哈哈哈, 千万不要看我橱窗啊 我求你们了 不要看[看], 艾特喜欢的人520一起去看电影《请别相信她》吧 对着彼此开怀大笑, b9m是夏城南的“恋不舍”权望柯挺挺, 信[色], [看], 你怎么知道[微笑], 信我这个[看], 真的是辣条好嘛[流泪], 王靖雯唱的《妈妈》太有感触了, , 相信[看], 嗯呢[看], [色][色][色], 我错了哥哥[流泪], [微笑][微笑][微笑], 除了辣条没了[微笑], [色], 凉了[看], [泪奔], 橱窗有你们想要的辣条[舔屏], 对[流泪], 对的，而且我橱窗更加炸裂[看], 这种爱情的苦 让兄弟来替你扛吧, 别说了姐姐[流泪], 宫崎骏电影《天空之城》6月1日重映啦，终于能再次在大银幕看到宫崎骏的电影了！, 我错了[流泪], 是啊, 真的哎[流泪], 羡慕了[流泪], 手表:得勿davena小金穗, 正义的 孝顺的 不顾一切的, 🎵《花束》-江皓南, 千万不要看我橱窗啊 我求你们了 不要看[流泪], [玫瑰],',
    #     '《谢谢》, 拿捏[看], 情人节脱单秘籍在我橱柜[舔屏], [看], 别太离谱[干饭人], 希望你是真的喜欢[舔屏], 别乱翻啊[发怒], 可以的话大家可以长按视频赞赏3朵免费的小红花嘛 谢谢大家[猪头], 不是 你一恋爱博主你橱窗是啥啊[微笑][微笑], 进去出不来了 别怪我没提醒[调皮], 更炸裂了对吧[微笑], 我的错[微笑], 520情人节送什么 看我橱窗[看], 别太荒谬[调皮], 警察：精彩精彩，所以这就是你作案过程？, 抖音搜“神图壁纸” 进小程序输 96  取我全部表情包, 谁问你了，我问谁问你了[发怒], 你小子怎么算的，明明是“相亲相爱一家人(7）”, 你是会打算盘的, 别乱翻[调皮], 痛，太痛了[流泪], 特朗普最近可不好过[看], 进去出不来了 别怪我没提醒[干饭人], 你小子别乱翻[干饭人], 我劝你少管闲事[调皮], 我知道你很急，我再催催[耶], 本以为聊天足够炸裂了 直到看到了我的橱柜……, 终极答案[看], 爱情需要放长假[看], 是不是心动了[得意], 情人节表白神器[干饭人], 连夜上架[舔屏], 你小子[流泪], [干饭人], [笑哭], 本来',
    # ]), use_label=False)
    #
    # print(keyword_res)