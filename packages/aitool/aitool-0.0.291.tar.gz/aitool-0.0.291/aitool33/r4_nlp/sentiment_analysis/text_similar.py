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
from collections import defaultdict
from typing import Dict, Union, List, Any, NoReturn, Tuple, Callable
from aitool import DATA_PATH, load_line, load_pickle, is_all_chinese, dump_pickle, get_ngram, get_aitool_data, \
    dump_lines, pool_map, exe_time, singleton
from tqdm import tqdm
from numpy import dot
from numpy.linalg import norm
from os import path, cpu_count
import math


def load_word2vec(path, dimension=300) -> Dict[str, List]:
    """
    TODO 目前只考虑空格分割的行格式文件
    加载词向量
    :param path:
    :param dimension:
    :return:
    """
    source_data = load_line(path)
    source_data_dict = {}
    for i, line in tqdm(enumerate(source_data), 'load word2vec {}'.format(path)):
        if i == 0:
            continue
        if i == 0 and 'word2vec' in line:
            continue
        line = line.strip().split(' ')
        if len(line) != dimension+1:
            raise ValueError('idx{}, len{}, {}'.format(i,len(line), line))
        word = line[0]
        word_vec_list = [float(x) for x in line[1:]]
        source_data_dict[word] = word_vec_list
    return source_data_dict


def cos_sim(v1: List, v2: List) -> float:
    """
    计算两个向量的余弦距离，输入向量是list格式。
    # TODO sklearn包有做比较多的集成，问题是sklearn包需要额外的下载模型过程未考虑好如何自动化
    # from sklearn.metrics.pairwise import cosine_similarity
    # simi = cosine_similarity(x, y)
    # TODO 基于np的方案, 可以通过判定输入参数的格式用不同的计算方案来融合
    # def distCosine(x, y):
    #     ""
    #     :param x: m x k array
    #     :param y: n x k array
    #     :return: m x n array
    #     ""
    #     xx = np.sum(x ** 2, axis=1) ** 0.5
    #     x = x / xx[:, np.newaxis]
    #     yy = np.sum(y ** 2, axis=1) ** 0.5
    #     y = y / yy[:, np.newaxis]
    #     dist = 1 - np.dot(x, y.transpose())  # 1 - 余弦距离
    #     return dist
    # def cos_sim(x, y):
    #     x = np.mat(x)
    #     y = np.mat(y)
    #     num = float(np.vstack([x,y]) * y.T)
    #     denom = np.linalg.norm(np.vstack([x,y])) * np.linalg.norm(y)
    #     cos = num / denom
    #     sim = 0.5 + 0.5 * cos
    #     return sim
    """
    sim = dot(v1, v2) / (norm(v1) * norm(v2))
    return sim


@singleton
class VectorSim:
    def __init__(self, path=None, dim=None):
        """
        基于词向量文件计算文本相似度
        :param path: 词向量文件路径
        :param dim: 向量维度数
        """
        if dim is None:
            self.dim = 300
        if path is None:
            path = get_aitool_data('sgns.weibo.word', packed=True, packed_name='sgns.weibo.word.zip', pack_way='zip')
            self.word2vector = load_word2vec(path, dimension=self.dim)

    def sim(self, s1: str, s2: str, chinese=False) -> float:
        """
        计算两个字符串的余弦相似度
        1. 取 1-gram, 2-gram, 3-gram
        2. 过滤gram
        3. 词向量相加
        4. 求余弦距离
        :param s1: 待比较的字符串
        :param s2: 待比较的字符串
        :param chinese: TODO 仅用中文gram做比较
        :return: 相似度
        """
        gram1 = set(get_ngram(s1, ngram=1)) | set(get_ngram(s1, ngram=2)) | set(get_ngram(s1, ngram=3))
        gram2 = set(get_ngram(s2, ngram=1)) | set(get_ngram(s2, ngram=2)) | set(get_ngram(s2, ngram=3))
        gram1 = [g for g in gram1 if is_all_chinese(g)]
        gram2 = [g for g in gram2 if is_all_chinese(g)]
        vct1 = [self.word2vector[g] for g in gram1 if g in self.word2vector]
        vct2 = [self.word2vector[g] for g in gram2 if g in self.word2vector]
        v1 = []
        v2 = []
        for i in range(self.dim):
            p = 0
            for k in range(len(vct1)):
                p += vct1[k][i]
            v1.append(p)
            p = 0
            for k in range(len(vct2)):
                p += vct2[k][i]
            v2.append(p)
        return cos_sim(v1, v2)


def vector_sim(text_1, text_2, chinese=False):
    vector_sim_class = VectorSim()
    return vector_sim_class.sim(text_1, text_2, chinese=chinese)


def char_sim(s1: str, s2: str) -> float:
    # 两个字符串里相同字数的占比
    c1 = set(s1)
    c2 = set(s2)
    c_intersection = len(c1 & c2)
    c_union = len(c1 | c2)
    if c_union == 0:
        return 0
    return c_intersection/c_union


@exe_time(print_time=True)
def de_sim(
        ordered_texts: List[str],
        method: Callable = char_sim,
        threshold: float = 0.8,
        show: bool = False,
) -> Tuple[List[str], Dict[str, str]]:
    """
    输入一组有顺序的文本，从前往后，仅保留和前面文本相似度低于阈值的文本。
    TODO 单纯的for循环太慢
    :param ordered_texts: 一组有顺序的文本
    :param method: 相似度方法，输出阈值[0,1]
    :param threshold: 大于等于该阈值被视为相似
    :param show: 打印信息
    :return: (保留下来的一组文本List[str]，删除详情{被删除的文本:高相似的保留的文本})
    """
    selected = []
    char2text = defaultdict(list)
    detail = {}
    count = 0
    for text in tqdm(ordered_texts, 'de_sim'):
        # 仅对有重复字的做相似度比较，提高速度
        candidate = []
        for char in text:
            candidate.extend(char2text[char])
        for char in set(text):
            char2text[char].append(text)
        candidate = set(candidate)
        match = False
        for st in candidate:
            count += 1
            sim_score = method(text, st)
            if sim_score >= threshold:
                if show:
                    print('sim', text, st, sim_score)
                detail[text] = st
                match = True
                break
        if not match:
            selected.append(text)
    print('len', len(ordered_texts), 'count', count)
    return selected, detail


def generate_offline_sim() -> None:
    """
    TODO 本函数还未整理
    并发计算批量的相似度
    :return: None
    """

    def _word_select() -> None:
        """
        输出特定词向量和特定词表的交集, 为后续计算离线的两两相似词表减少计算量。
        :return:
        """
        from aitool import dump_lines

        word_vector = load_word2vec('../../develop/develop_similar/sgns.weibo.word')
        keyword2score_all = load_pickle(path.join(DATA_PATH, 'keyword.pkl'))
        word_list = list(word_vector.keys())
        len_word_list = len(word_list)
        print('word_vector', len(word_vector))
        print('keyword2score_all', len(keyword2score_all))

        dump_lines(list(word_vector.keys()), '../../develop/develop_similar/word_vector')
        dump_lines(list(keyword2score_all.keys()), '../../develop/develop_similar/keyword2score_all')
        # dump_lines(same, 'same')
        # dump_lines(dif, 'dif')
        # print('same', len(set(word_vector.keys()) & set(keyword2score_all.keys())))
        word_pair = {}
        print('word_pair', id(word_pair))
        print('len_word_list', len(word_list))
        word_list_select = []
        for w in word_list:
            if len(w) > 6:
                continue
            if not is_all_chinese(w):
                continue
            word_list_select.append(w)
        print('word_list_select', len(word_list_select))
        word_list_select = list(set(word_list_select) & set(keyword2score_all))
        print('word_list_select', len(word_list_select))
        dump_lines(word_list_select, '../../develop/develop_similar/word_list_select')
        len_word_list_select = len(word_list_select)

        word_vector_select = {}
        for w in word_list_select:
            word_vector_select[w] = word_vector[w]

        dump_pickle(word_vector_select, 'word_vector_select')

    _word_select()

    word_vector_select = load_pickle('word_vector_select.pkl')
    word_list = list(word_vector_select.keys())
    len_word_list = len(word_list)
    print('len_word_list', len_word_list)

    def _cal(data):
        b, e = data
        box = []
        dump_time = 0
        for p1 in tqdm(range(b, e), 'task_{}'.format(b), mininterval=1.0):
            for p2 in range(p1 + 1, len_word_list):
                w1 = word_list[p1]
                w2 = word_list[p2]
                v1 = word_vector_select[w1]
                v2 = word_vector_select[w2]
                score = dot(v1, v2) / (norm(v1) * norm(v2))
                if score > 0.8:
                    box.append([w1, w2, round(score, 6)])
            if len(box) > 1000 * (dump_time + 1):
                dump_time += 1
                dump_lines(box, 'task_{}_len_{}'.format(b, len(box)))
        dump_lines(box, 'task_{}_len_{}_finish'.format(b, len(box)))
        return box

    # 均衡任务
    all_time = (len_word_list - 1) * len_word_list // 2
    print('all_time', all_time)
    avg_time = max(math.ceil(all_time / (cpu_count()-1)), 1)
    print('avg_time', avg_time)
    task = []
    step = 0
    pos = 0
    head = 0
    while pos < len_word_list:
        step += len_word_list - pos - 1
        if step >= avg_time or pos == len_word_list - 1:
            task.append([head, pos + 1])
            head = pos + 1
            step = 0
        pos += 1
    print(task)

    all = {}
    for rst in pool_map(_cal, task):
        for w1, w2, s in rst:
            if s > 0.80:
                all[(w1, w2)] = s

    print(len(all))
    dump_pickle(all, 'word_similar')


if __name__ == '__main__':
    print(vector_sim('杀人该死!', '杀人有罪。'))
    print(vector_sim('爸爸打儿子~', '爸爸打孩子'))
    print(vector_sim('父亲打儿子', '爸爸打孩子'))
    print(vector_sim('杀人该死！', '杀人有罪。', chinese=True))
    print(vector_sim('爸爸打儿子~', '爸爸打孩子', chinese=True))
    print(vector_sim('父亲打儿子', '爸爸打孩子', chinese=True))

    nodes = [
        '犯罪的代价',
        '纵容犯罪',
        '减少犯罪',
        '年龄还能强奸',
        '估计强奸',
        '强奸丢脸',
        '强奸幼女',
        '强奸小孩',
        '强奸缺德',
        '欲望去强奸',
        '强奸对象',
        '强奸无语',
        '强奸吹牛',
        '讨厌强奸',
        '奇怪强奸',
        '诱骗强奸',
        '强奸违法',
        '制服被强奸',
        '强奸的是残疾',
        '发抖还能强奸',
        '强奸抢劫',
        '蹒跚还强奸',
        '丢脸抹黑',
        '后人遭殃',
        '浪费粮食',
        '绝望的凝视',
        '没收作案工具',
        '敲诈未遂',
        '色狼变态',
        '拘留罚款',
        '拉屎撒尿',
        '走路都成问题',
        '犯人最看不起',
        '肯定是强奸',
    ]
    print('char_sim')
    _, de = de_sim(nodes, method=char_sim, threshold=0.8, show=True)
    vs = VectorSim()
    print('vs.sim')
    _, de = de_sim(nodes, method=vs.sim, threshold=0.8, show=True)
