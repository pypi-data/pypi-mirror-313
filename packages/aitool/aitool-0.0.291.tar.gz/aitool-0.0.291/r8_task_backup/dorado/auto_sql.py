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
from statistics import mean
import numpy as np
from typing import List
from tqdm import tqdm
from aitool import sql_uid2video_info, sql_vid2video_info, get_ngram_tf, load_line, get_aitool_data, singleton, \
    get_ngram, sql_video_keyword_rank, sql_result2text, normalize, cross_entropy, scale_array, print_yellow, \
    dict2ranked_list, print_red, sql_result2list, dump_excel, customize_sentence_clear, send_file2tos, \
    send_feishu_sheet, get_keyword2fields, get_log, is_contains_chinese,\
    sql_video_keyword_rank_with_collect_set, is_no_symbol


# TODO 改logging输出信息


def customize_clear(texts):
    new_texts = []
    for text in texts:
        new_texts.append(customize_sentence_clear(text))
    return new_texts


@singleton
class Colloquial:
    # 计算一个文本的口语化程度分
    def __init__(self, idf_dict=None, split_method='char', idf_method='log', multilingual=True, limit=1000000):
        # 仅从词典中读取出现概率前limit的词，以减小内存压力
        # idf分数越高表示越罕见
        # 为更精确的评估，会分别对不同字长l，计算idf_l的μ_l和σ_l
        self.gaussian_distributions = dict()
        if idf_dict is None:
            if split_method == 'jieba' and idf_method == 'log' and not multilingual:
                idf_file_path = get_aitool_data('idf_jieba_log.txt', sub_path='dorado', packed=True,
                                                packed_name='idf_jieba_log.txt.zip', pack_way='zip')
            elif split_method == 'jieba' and idf_method == 'log' and multilingual:
                idf_file_path = get_aitool_data('idf_jieba_log_multilingual_0605.txt', sub_path='dorado', packed=True,
                                                packed_name='idf_jieba_log_multilingual_0605.txt.zip', pack_way='zip')
            elif split_method == 'char' and idf_method == 'log':
                idf_file_path = get_aitool_data('idf_char_log_multilingual_0606.txt', sub_path='dorado', packed=True,
                                                packed_name='idf_char_log_multilingual_0606.txt.zip', pack_way='zip')
            else:
                raise ValueError('not matched idf_file_path')
            idf_list = load_line(idf_file_path, separator='\t', limit=limit)
            idf_dict = {}
            for idf_line in tqdm(idf_list, 'load idf dict', delay=5):
                if len(idf_line) != 2:
                    continue
                word, score = idf_line
                if len(word) == 0:
                    continue
                idf_dict[word] = float(score)
        self.idf_dict = idf_dict
        self.max_len = 0        # 词典中最长的词的长度
        self.do_init()

    def get_idf_dict(self):
        return self.idf_dict

    def do_init(self):
        print('init Colloquial')
        len2score = defaultdict(list)
        len2diff_square = defaultdict(list)
        len2mean = defaultdict(float)
        len2deviation = defaultdict(float)
        for k, v in tqdm(self.idf_dict.items(), 'check idf_dict', delay=5):
            len2score[len(k)].append(v)
            self.max_len = max(len(k), self.max_len)
        for k, v in tqdm(len2score.items(), 'calculate mean', delay=5):
            # 数据量过大时会导致数值溢出
            len2mean[k] = np.mean(v)
        for k, v in tqdm(len2score.items(), 'calculate diff_square', delay=5):
            for s in v:
                len2diff_square[k].append((s - len2mean[k]) ** 2)
        for k, v in tqdm(len2diff_square.items(), 'calculate gaussian_distributions', delay=5):
            len2deviation[k] = np.mean(v) ** 0.5
            self.gaussian_distributions[k] = [len2mean[k], len2deviation[k]]
        print('idf gaussian_distributions')
        print(self.gaussian_distributions)
        # TODO 默认的jieba分词导致len2的分数最小，影响后续计算

    def get_colloquial_score(self, word, min_g=1, max_g=5):
        # 由于读取idf时是从低向高读的前limit个，导致在3-gram、4-gram的idf会被严重低估。
        # TODO 最优解是在生成词典时直接出均值和标准差说明文件。
        # 目前是补丁写法，对3-gram、4-gram的idf做人工修正。
        mean_correction = [0, 0.1, 2, 3, 4, 5, 6, 7, 8]
        # 假设数据的idf值符合正太分布，对i-gram设置其σ的倍数。
        # 例如 departure = [0, 2, 1] 表示：departure[0]无意义，1-gram的idf值为μ_1+2*σ_1，2-gram的idf值为μ_2+1*σ_2
        departure = [0, 0.5, 1, 1, 1, 1, 1, 1, 1]
        # 对各层估算出的均idf值加权累积得到最终idf值。
        # 例如 level_weight = [[], [1],[0.4, 0.6]] 表示：
        #     1、level_weight[0] 无意义
        #     2、如果word只计算1种长度(i)的gram，其均值为s_(i-gram)，那么最终的得分S=1*s_(i-gram)
        #     3、如果word需计算2种长度(i，i+1)的gram，其均值分别为s_(i-gram)、s_(i+1-gram)，
        #        那么最终的得分S=0.4*s_(i-gram)+0.6*s_(i+1-gram)
        level_weight = [
            [],
            [1],
            [0.4, 0.6],
            [0.15, 0.25, 0.7],
            [0.05, 0.15, 0.2, 0.7],
            [0.05, 0.05, 0.1, 0.1, 0.7],
            [0, 0.05, 0.05, 0.1, 0.1, 0.7],
            [0, 0, 0.05, 0.05, 0.1, 0.1, 0.7],
            [0, 0, 0, 0.05, 0.05, 0.1, 0.1, 0.7],
        ]

        level_score = []
        for wl in range(max(1, min_g), min(self.max_len + 1, max_g, len(word) + 1)):
            wn = list(get_ngram(word, ngram=wl))
            l_count = len(wn)
            l_score = 0
            for wni in wn:
                if wni in self.idf_dict:
                    l_score += self.idf_dict[wni]
                else:
                    l_score += (
                            self.gaussian_distributions[wl][0] +
                            mean_correction[wl] +
                            departure[wl] * self.gaussian_distributions[wl][1]
                    )
            if l_count == 0:
                # 处理未知错误
                level_score.append(0)
                print('Error: len wn is 0')
                print('word', word)
                print('wl', wl)
                print('wn', wn)
            else:
                level_score.append(l_score / l_count)

        score = 0
        level_count = len(level_score)
        for ls, lw in zip(level_score, level_weight[level_count]):
            score += ls * lw

        return score


def get_sentence_idf(text, min_g=1, max_g=5, idf_dict=None, round_len=6):
    # idf_dict，limit 仅第一次调用本方法时生效，用于初始化singleton的类Colloquial
    colloquial = Colloquial(idf_dict=idf_dict)
    idf_score = colloquial.get_colloquial_score(text, min_g=min_g, max_g=max_g)
    idf_score = round(idf_score, round_len)
    return idf_score


def keyword_rank_score(keyword, tf_score, idf_score):
    # idf分和tf分相乘
    # 如果只有1个字，对分数做惩罚
    rank_score = tf_score * idf_score
    if len(keyword) == 1:
        rank_score = 0
    return rank_score


def get_keywords(
        texts,
        idf_dict,
        split_method,
        deduplication,
        keyword_rank_score,
        all_chinese=True,
        no_space=False,
        no_border_space=True,
        show=True,
        show_detail=False,
        max_key=200,
        delete_short_in_long=True,
        delete_long_in_short=False,
):
    if show:
        print('calculate tf dict')
    tf_dict = get_ngram_tf(
        texts,
        split_method=split_method,
        deduplication=deduplication,
        show=show,
        show_detail=show_detail,
        all_chinese=all_chinese,
        no_space=no_space,
        no_border_space=no_border_space,
    )

    score_tfidf = []
    for k, tf in tqdm(tf_dict.items(), 'count tf-idf', delay=60, mininterval=60, maxinterval=120):
        _idf = get_sentence_idf(k, min_g=1, max_g=4, idf_dict=None)
        score_tfidf.append([k, tf, _idf, keyword_rank_score(k, tf, _idf)])
    score_tfidf.sort(key=lambda _: _[3], reverse=True)
    if show:
        print('### score_tfidf_ori ###')
        for line in score_tfidf[:100]:
            print(line)

    # 非全中文减分 & 顺序被完全包含关系略过 & 包含空格略过
    score_tfidf_new = []
    chosen = set()
    for k, _tf, _idf, _score in score_tfidf:
        is_new = True
        _score_new = _score
        for c in chosen:
            if delete_short_in_long and (k in c):
                # TODO 特殊情况不视为已覆盖，例如母字符串不是全中文而k是全中文：chosen='*人们'， k='人们'
                is_new = False
                break
            if delete_long_in_short and (c in k):
                is_new = False
                break
        if not is_new:
            continue
        if ' ' in k or '\n' in k or '。' in k or not is_contains_chinese(k):
            continue
        if not is_no_symbol(k):
            # _score_new = _score * 0.5
            # TODO仔细分析会导致sql表达式异常的符号做排除
            continue
        chosen.add(k)
        score_tfidf_new.append([k, _tf, _idf, _score_new])
        if len(score_tfidf_new) >= max_key:
            break
    score_tfidf_new.sort(key=lambda _: _[3], reverse=True)
    # idf接近且被完全包含关系略过
    score_tfidf_new2 = []
    score_len = len(score_tfidf_new)
    for i in range(score_len):
        k, _tf, _idf, _score = score_tfidf_new[i]
        is_new = True
        for j in range(i, score_len):
            if i == j:
                continue
            k2, _tf2, _idf2, _score2 = score_tfidf_new[j]
            if -0.00001 < _tf - _tf2 < 0.00001 and -0.5 < _score - _score2 < 0.5:
                if k in k2:
                    is_new = False
                    break
        if is_new:
            score_tfidf_new2.append([k, _tf, _idf, _score])

    if show:
        print('### score_tfidf ###')
        for line in score_tfidf[:50]:
            print(line)
        print('### score_tfidf_new ###')
        for line in score_tfidf_new[:50]:
            print(line)
        print('### score_tfidf_new2 ###')
        for line in score_tfidf_new2[:50]:
            print(line)

    return tf_dict, score_tfidf_new2


def select_keyword(
        similar_score_whole,
        word2similar_score,
        query_keyword,
        query_badword,
        tf_dict_ori,
        score_tfidf_ori,
        use_top_tfidf=30,
        update_speed_keyword=5,  # 从高于总体分的词里选keyword的数量
        update_speed_badword=3,  # 从高于关键词平均分的词里选badword的数量
        keyword_limit=30,
        badword_limit=30,
        de_similar=False,
        show=True,
        show_help=True,
):
    if word2similar_score is None:
        # 第一次选关键词时，使用ori里排序高的
        count = 0
        for info in score_tfidf_ori:
            query_keyword.append(info[0])
            count += 1
            if count >= use_top_tfidf:
                break
    else:
        # 分数越小的词越好
        word_score = dict2ranked_list(word2similar_score)

        # 腾出空位
        def _after_remove(_words, _word2score, _remove, default, reverse=False):
            _tmp = []
            for _w in _words:
                if _w in _word2score:
                    _tmp.append([_w, _word2score[_w]])
                else:
                    print('not find in word2dict', _w)
                    _tmp.append([_w, default])
            _tmp.sort(key=lambda _: _[1], reverse=reverse)
            if _remove > 0:
                _tmp = _tmp[:-_remove]
            return [_w for _w, _s in _tmp]

        keyword_remove = max(update_speed_keyword - (keyword_limit - len(query_keyword)), 0)
        query_keyword = _after_remove(query_keyword, word2similar_score, keyword_remove, 100000, reverse=False)
        badword_remove = max(update_speed_badword - (badword_limit - len(query_badword)), 0)
        query_badword = _after_remove(query_badword, word2similar_score, badword_remove, -100000, reverse=True)

        # 更新好词和坏词
        word_score.sort(key=lambda _: _[1])
        count = 0
        for w, k in word_score:
            if count == update_speed_keyword:
                break
            if w not in query_keyword + query_badword:
                query_keyword.append(w)
                count += 1
        word_score.sort(key=lambda _: _[1], reverse=True)
        count = 0
        for w, k in word_score:
            if count == update_speed_badword:
                break
            if w not in query_keyword + query_badword:
                query_badword.append(w)
                count += 1
    return query_keyword, query_badword


def get_distribution_similarity(
        all_word_rank: List[str],
        score_new,
        score_ori,
        show=False,
):
    # 计算交叉熵
    # 构建词频分布时考虑词的idf值，降低不重要词的影响、
    # TODO 支持不同分别的tf-idf分
    word2score_new = {}
    word2score_ori = {}
    for w, tf, idf, score in score_new:
        word2score_new[w] = score
    for w, tf, idf, score in score_ori:
        word2score_ori[w] = score

    distribution_new = []
    distribution_ori = []
    for w in all_word_rank:
        if w in word2score_new:
            distribution_new.append(word2score_new[w])
        else:
            distribution_new.append(0.0)
        if w in word2score_ori:
            distribution_ori.append(word2score_ori[w])
        else:
            distribution_ori.append(0.0)

    distribution_new = normalize(distribution_new)
    distribution_ori = normalize(distribution_ori)
    if show:
        print('distribution_new', distribution_new[:10])
        print('distribution_ori', distribution_ori[:10])
    rst = cross_entropy(distribution_new, distribution_ori)
    return rst


def analysis_query_rst(
        query_rst,
        tf_dict_ori,
        score_tfidf_ori,
        idf_dict,
        split_method,
        deduplication,
        keyword_rank_score,
        all_chinese=True,
        no_space=False,
        no_border_space=True,
        top_tfidf=200,  # 仅考虑top200的词
        min_hit=10,
        show=False,
        show_detail=False,
        do_customize_clear=True,
        delete_short_in_long=True,
        delete_long_in_short=False,
):
    # 分析查询结果，输出所有词的评估分
    texts = sql_result2text(query_rst)
    # 对查询结果里的干扰词做清洗
    if do_customize_clear:
        texts = customize_clear(texts)
    # 计算总体结果的评分
    print('get all word in query_rst')
    tf_dict_all, score_tfidf_all = get_keywords(
        texts,
        idf_dict,
        split_method,
        deduplication,
        keyword_rank_score,
        all_chinese=all_chinese,
        no_space=no_space,
        no_border_space=no_border_space,
        show=show,
        show_detail=show_detail,
        delete_short_in_long=delete_short_in_long,
        delete_long_in_short=delete_long_in_short,
    )

    selected_word = \
        set([_[0] for _ in score_tfidf_all[:top_tfidf]]) \
        | set([_[0] for _ in score_tfidf_ori[:top_tfidf]])
    selected_word = list(selected_word)
    print('len selected_word', len(selected_word))

    similar_score_whole = get_distribution_similarity(
        selected_word,
        score_tfidf_all,
        score_tfidf_ori,
    )
    # 对query_keyword做独立评分
    word2similar_score = {}
    for word in tqdm(selected_word, 'analysis each selected word', delay=5):
        related_text = []
        for line in texts:
            if word in line:
                related_text.append(line)
        if len(related_text) < min_hit:
            continue
        tf_dict_word, score_tfidf_word = get_keywords(
            related_text,
            idf_dict,
            split_method,
            deduplication,
            keyword_rank_score,
            show=show,
            show_detail=show_detail,
            delete_short_in_long=delete_short_in_long,
            delete_long_in_short=delete_long_in_short,
        )
        tmp_selected_word = \
            set([_[0] for _ in score_tfidf_word[:top_tfidf]]) \
            | set([_[0] for _ in score_tfidf_ori[:top_tfidf]])
        tmp_selected_word = list(tmp_selected_word)
        similar_score = get_distribution_similarity(
            tmp_selected_word,
            score_tfidf_word,
            score_tfidf_ori,
        )
        word2similar_score[word] = similar_score
    return similar_score_whole, word2similar_score


def get_base_vids_similar(vif, ori_vids_info):
    v = vif.asDict()
    vif_str = v['nickname'] + v['signature'] + v['item_title'] + v['music_title'] + v['asr1'] + v['asr2'] + v['ocr']
    vif_set = set(vif_str)

    ori_str = ''
    for ovif in ori_vids_info:
        v = ovif.asDict()
        ovif_str = v['nickname'] + v['signature'] + v['item_title'] + v['music_title'] + v['asr1'] + v['asr2'] + v['ocr']
        ori_str = ori_str + ovif_str
    ori_set = set(ori_str)

    rate = len(vif_set & ori_set) / len(vif_set)
    print(vif.asDict()['item_id'], rate)
    return rate


def select_uid_video_base_vids(vid_info, ori_vids):
    # 先全转为字符串格式
    ori_vids = [str(_) for _ in ori_vids]

    ori_vids_info = []
    uid_related_vids_info = []
    rst = []
    for vif in vid_info:
        item_id = str(vif.asDict()['item_id'])
        if item_id in ori_vids:
            ori_vids_info.append(vif)
        else:
            uid_related_vids_info.append(vif)
    for vif in uid_related_vids_info:
        if get_base_vids_similar(vif, ori_vids_info) > 0.3:
            rst.append(vif)
    return ori_vids_info + rst


def auto_sql(
        # 种子信息
        uids=None,
        vids=None,
        task_name='no_task_name',
        # 主要控制参数
        epochs=1,  # 迭代次数
        keyword_limit=30,  # 好词的数量上限
        badword_limit=15,  # 坏次的数量上限
        # 第一次查询用的关键词
        do_customize_clear=True,  # 对查询出的文本做清洗
        use_top_tfidf=30,  # 第一次选关键词时选择的词数
        # 用关键词构建sql
        keyword_method='same',  # 关键词分数的计算方式，same\scale\entropy
        keyword_reward=1,  # 同一权重模式下，好词的分数
        keyword_reward_tfidf=False,
        keyword_reward_name=False,      # TODO 目前仅在keyword_reward_tfidf=True时生效
        keyword_reward_name_score=3,
        badword_punish=-1,  # 同一权重模式下，坏词的分数
        keyword_scale=3,  # 缩放权重模式下，好词的分数
        keyword_scale_base=10,  # 缩放权重模式下，作为好词基础分的关键词位置排序（顺序）
        badword_scale=3,  # 缩放权重模式下，坏词的分数
        badword_scale_base=10,  # 缩放权重模式下，作为坏词基础分的关键词位置排序（顺序）
        keyword_entropy=5,  # 熵值权重模式下，好词/坏词的值系数
        keyword_entropy_base=5,  # 熵值权重模式下，好词/坏词的基础分
        # 筛选关键词
        top_tfidf=200,  # 每次迭代时，考虑种子查询结果和本轮查询结果中tfidf靠前词的个数
        min_hit=7,  # 如果被考虑的词在本轮查询结果中出现次数小于min_hit则忽略
        de_similar=False,  # 尚未使用
        # 更新关键词
        update_speed_keyword=5,  # 每一轮迭代更新好词的数量
        update_speed_badword=3,  # 每一轮迭代更新坏词的数量
        # 控制查sql的时间范围
        time_range_seed=30,
        time_range_optimize=10,
        time_range_final=30,
        time_range_date=-1,
        # 控制查sql的结果数量
        rst_limit_seed=2000,
        rst_limit_optimize=2000,
        rst_limit_final=10000,
        # 使用的分词方法和idf词典
        split_method='char',
        idf_method='log',
        multilingual=True,
        idf_list_limit=1000000,  # 仅读取idf词典的前一部分，以节省内存
        all_chinese=True,
        no_space=True,
        no_border_space=True,
        deduplication=False,  # 计算tf 时是否去重
        # 获取idf分的方法
        keyword_rank_score=keyword_rank_score,
        # 打印提示信息
        show_template=False,
        show_sql=True,
        show_detail=True,  # 打印各函数内的提示信息
        send_step_result=True,
        lark_group_id='7216549572061954099',
        folder_token=None,
        lark_sheet_limit=200,  # 输出到飞书表格时输出的行数，过多会报错
        dump_local_file=True,
        # 流程控制
        skip_final=True,
        # 剔除的uid名单
        exclude_uid=None,
        # 上传到tos
        send2tos=True,
        # 是否返回文档的links和种子数据信息
        return_links=True,
        # 使用聚合的sql查找
        sql_with_collect_set=False,
        # 仅选择和vids视频相似的uid的视频
        is_select_uid_video_base_vids=False,
        # idf 词表删除重复的词
        delete_short_in_long=True,
        delete_long_in_short=False,
):
    all_links = {}
    # 将日志存在特定的log中
    sql_log = get_log(task_name[:40] + '.log')
    if show_detail:
        print('getting seed info')
    if vids is None:
        vids = []
    ori_vids = vids
    uid_related_vids = []
    if uids is not None and len(uids) > 0:
        # 直接拉取各用户最近的所有vid
        related_vid_info = sql_uid2video_info(
            uids,
            time_range=time_range_seed,
            time_range_date=time_range_date,
            limit=rst_limit_seed,
            show_template=show_template,
            show_sql=show_sql,
        )
        uid_related_vids = [_['item_id'] for _ in related_vid_info]
        vids = vids + uid_related_vids

    vid_info = sql_vid2video_info(
        vids,
        video_time_range=time_range_seed,
        report_time_range=time_range_seed,
        comment_time_range=time_range_seed,
        time_range_date=time_range_date,
        limit=rst_limit_seed,
        show_template=show_template,
        show_sql=show_sql,
        sql_log=sql_log,
    )

    if is_select_uid_video_base_vids:
        if len(ori_vids) > 0 and len(uid_related_vids) > 0:
            vid_info = select_uid_video_base_vids(vid_info, ori_vids)


    if dump_local_file:
        context = sql_result2list(vid_info)
        dump_excel(context, task_name + '_seed_info')
    link = send_feishu_sheet(
        sql_result2list(vid_info),
        result_title=task_name + '_seed_info',
        folder_token=folder_token,
        lark_group_id=lark_group_id,
        limit=lark_sheet_limit,
        auto_cut=True,
    )
    all_links[task_name + '_seed_info'] = link
    texts, field2text = sql_result2text(vid_info, get_field2text=True)

    if show_detail:
        print('loading idf file')
    # 加载idf词典
    idf_tool = Colloquial(split_method=split_method, idf_method=idf_method, multilingual=multilingual,
                          limit=idf_list_limit)
    idf_dict = idf_tool.get_idf_dict()
    if show_detail:
        print('finish load idf file')

    # 对查询结果里的干扰词做清洗
    if do_customize_clear:
        texts = customize_clear(texts)
    if len(texts) < 2:
        print_red('仅查找到{}个种子。本方法需要至少2条case。请检查输入的case和查询时间间隔。'.format(len(texts)))
        raise ValueError('len of case less than 2')
    if len(texts) < 6:
        print_yellow('仅查找到{}个种子。本方法在种子视频数大于5时效果较好。'.format(len(texts)))
    if show_detail:
        print('ori text sample:')
        print(texts[:3])

    tf_dict_ori, score_tfidf_ori = get_keywords(
        texts,
        idf_dict,
        split_method,
        deduplication,
        keyword_rank_score,
        all_chinese=all_chinese,
        no_space=no_space,
        no_border_space=no_border_space,
        show=True,
        show_detail=show_detail,
        delete_short_in_long=delete_short_in_long,
        delete_long_in_short=delete_long_in_short,
    )
    link = send_feishu_sheet(
        score_tfidf_ori,
        result_title=task_name + '_seed_tfidf',
        folder_token=folder_token,
        lark_group_id=lark_group_id,
        limit=lark_sheet_limit,
        auto_cut=True,
    )
    all_links[task_name + '_seed_tfidf'] = link

    epoch_now = 0
    word2similar_score = None
    similar_score_whole = None
    query_keyword = []
    query_badword = []
    query_rst = []
    while epoch_now < epochs:
        epoch_now += 1
        print('epoch', epoch_now)
        # 获取本轮使用的关键词
        query_keyword, query_badword = select_keyword(
            similar_score_whole,
            word2similar_score,
            query_keyword,
            query_badword,
            tf_dict_ori,
            score_tfidf_ori,
            use_top_tfidf=use_top_tfidf,
            update_speed_keyword=update_speed_keyword,  # 从高于总体分的词里选keyword的数量
            update_speed_badword=update_speed_badword,
            keyword_limit=keyword_limit,
            badword_limit=badword_limit,
            de_similar=de_similar,
        )
        print('query_keyword', query_keyword)
        print('query_badword', query_badword)
        # 获取各个keyword所属字段
        keyword2fields = get_keyword2fields(list(set(query_keyword + query_badword)), field2text)
        # 获取各个keyword对应的分数，未tfidf分除以10
        # TODO 目前迭代的逻辑没有做
        base_tfidf = 10
        keyword2score = {}
        for _k, _tf, _idf, _score in score_tfidf_ori:
            _new_score = 1
            if keyword_reward_name:
                if _k in task_name:
                    _score *= keyword_reward_name_score
            _new_score += (_score - 5) / 20     # tfidf高于5的加分小于5减分
            _new_score += (_idf - 11) / 15      # idf高于11加分
            _new_score += (_tf - 0.3) / 5 if (_tf > 0.5 and _idf > 11) else 0   # idf高于11且tf高于0.5加分

            keyword2score[_k] = round(_new_score, 3)
        # 获取本轮的团伙扩散结果
        if sql_with_collect_set:
            query_rst, query_sql = sql_video_keyword_rank_with_collect_set(
                query_keyword,
                query_badword,
                keyword2fields,
                time_range_date=time_range_date,
                limit=rst_limit_optimize,
                show_template=show_template,
                show_sql=show_sql,
                keyword_reward=keyword_reward,
                badword_punish=badword_punish,
                return_sql=True,
                exclude_uid=exclude_uid,
                keyword_reward_tfidf=keyword_reward_tfidf,
                keyword_reward_tfidf_score=keyword2score,
            )
            # todo 目前还没有适配后续的数据处理流程
        else:
            query_rst, query_sql = sql_video_keyword_rank(
                query_keyword,
                query_badword,
                keyword2fields,
                time_range_date=time_range_date,
                limit=rst_limit_optimize,
                show_template=show_template,
                show_sql=show_sql,
                keyword_reward=keyword_reward,
                badword_punish=badword_punish,
                return_sql=True,
                exclude_uid=exclude_uid,
                keyword_reward_tfidf=keyword_reward_tfidf,
                keyword_reward_tfidf_score=keyword2score,
            )
        if dump_local_file or send2tos:
            context = sql_result2list(query_rst)
            data_path = dump_excel(context, task_name + '_step_{}'.format(epoch_now))
            if send2tos:
                send_file2tos(task_name + '_step_{}'.format(epoch_now) + '.xlsx', data_path)
        if send_step_result:
            link_sql = send_feishu_sheet(
                [query_sql],
                result_title=task_name + '_sql_{}'.format(epoch_now),
                folder_token=folder_token,
                lark_group_id=lark_group_id,
            )
            all_links[task_name + '_sql_{}'.format(epoch_now)] = link_sql
            link_rst = send_feishu_sheet(
                sql_result2list(query_rst),
                result_title=task_name + '_step_{}'.format(epoch_now),
                folder_token=folder_token,
                lark_group_id=lark_group_id,
                limit=lark_sheet_limit,
                # other_info={'sql': [query_sql]},  TODO other_info不成功
                auto_cut=True
            )
            all_links[task_name + '_step_{}'.format(epoch_now)] = link_rst

        # 评估新增的关键词，score越小越好
        # TODO 后续内部应该对待评估的关键词做独立查询，而非使用query_rst
        # TODO 应该拆为两个过程：1、从query_rst中选出N个新的待评估词（和现有词组合起来效果较好），2、查出评估数据集，3、做评估
        if epoch_now < epochs:
            # 在最后一轮迭代时略过关键词优化过程
            similar_score_whole, word2similar_score = analysis_query_rst(
                query_rst,
                tf_dict_ori,
                score_tfidf_ori,
                idf_dict,
                split_method,
                deduplication,
                keyword_rank_score,
                all_chinese=all_chinese,
                no_space=no_space,
                no_border_space=no_border_space,
                top_tfidf=top_tfidf,
                min_hit=min_hit,
                show=False,
                show_detail=False,
                do_customize_clear=do_customize_clear,
                delete_short_in_long=delete_short_in_long,
                delete_long_in_short=delete_long_in_short,
            )
            link = send_feishu_sheet(
                [[_k, _v] for _k, _v in word2similar_score.items()],
                result_title=task_name + '_step_{}_similar'.format(epoch_now),
                folder_token=folder_token,
                lark_group_id=lark_group_id,
                limit=lark_sheet_limit,
                auto_cut=True,
            )
            all_links[task_name + '_step_{}_similar'.format(epoch_now)] = link

    if not skip_final:
        # 最后优化一次关键词并输出结果
        print('final select keyword', epoch_now)
        # 获取本轮使用的关键词
        query_keyword, query_badword = select_keyword(
            similar_score_whole,
            word2similar_score,
            query_keyword,
            query_badword,
            tf_dict_ori,
            score_tfidf_ori,
            use_top_tfidf=use_top_tfidf,
            update_speed_keyword=update_speed_keyword,  # 从高于总体分的词里选keyword的数量
            update_speed_badword=update_speed_badword,
            keyword_limit=keyword_limit,
            badword_limit=badword_limit,
            de_similar=de_similar,
        )
        print('final query_keyword', query_keyword)
        print('final query_badword', query_badword)
        # 获取本轮的团伙扩散结果
        final_query_rst, final_query_sql = sql_video_keyword_rank(
            query_keyword,
            query_badword,
            video_time_range=time_range_final,
            limit=rst_limit_final,
            show_template=show_template,
            show_sql=show_sql,
            keyword_reward=keyword_reward,
            badword_punish=badword_punish,
            return_sql=True,
            exclude_uid=exclude_uid,
        )
        print('len of final_query_rst', len(final_query_rst))
        print(final_query_rst[:3])
        if dump_local_file or send2tos:
            context = sql_result2list(final_query_rst)
            data_path = dump_excel(context, task_name + '_finish')
            if send2tos:
                send_file2tos(task_name + '.xlsx', data_path)
                # log_file_path = get_log_path(task_name + '.log')
                # send_file2tos(task_name + '.log', log_file_path)
        link_sql = send_feishu_sheet(
            [final_query_sql],
            result_title=task_name + '_sql_finish',
            folder_token=folder_token,
            lark_group_id=lark_group_id,
        )
        all_links[task_name + '_sql_finish'] = link_sql
        link = send_feishu_sheet(
            sql_result2list(final_query_rst),
            result_title=task_name + '_finish',
            lark_group_id=lark_group_id,
            folder_token=folder_token,
            limit=lark_sheet_limit,
            # other_info={'sql': [final_query_sql]},
            auto_cut=True
        )
        all_links[task_name + '_finish'] = link
    else:
        final_query_rst = query_rst
    if return_links:
        return final_query_rst, all_links, vid_info
    else:
        return final_query_rst


if __name__ == '__main__':
    # 申请飞书文件夹
    # 在此目录下新建文件夹https://bytedance.feishu.cn/drive/folder/fldcnUnI2gLSddUtGcJtdpWcuch
    # 然后从url里复制出folder_id

    print(get_sentence_idf('三星大作'))
    exit(0)
    # idf_tool = Colloquial()
    # idf_dict = idf_tool.get_idf_dict()
    # kk = ['手机','苹果','原装','支持','国行','比心','可以','正品','内存','全原','无拆修','拆修','二手手机','玫瑰','精品','带走','线下','精品二手手机','保真','河北','价格','数码','抖音','就是','数码科技','只要','微信','引流','虚假','成色','磕碰','通过','你说','作品','视频','低价','苹果手机','原装的','问题','店铺','然后','置换','划痕','过去','喜欢','真的','功能','正常','爱思','客户','实体','安排','标价','诱导','没有','邯郸','手机数码','这个','消费者','产品','诈骗','联系方式','二手','购买','电池','置顶','线下实体','怎么','官方','有的','发布','市场价','支持置换','版的','的手机','欺骗','只能','武汉','套路','官网','通过抖音','实体店铺','咨询','都是','出售','不能','欺骗消费者','保修','双卡','不是','商品','售卖','配件齐全','我要','让你','退款','抖音平台','交易','公开','国航','### score_out_idf ###','验机','全原装','支持验机','可验机','国行正品','店选','可以验机','全原无','张带走','功能正常','无磕碰','全原无拆修','国行原装','互关思','拆无修','无拆无修','远峰','全绿','磕碰划痕','爱思绿','网机','无磕碰划痕','国行全原','标价就是','海蓝色','线下交易','全原装的','原装可验机','暗病','原装无','全原装可验机','双待','远峰蓝','线下实体店铺','公开版','手机价格','官网可查','原装无拆修','公开版的','进网机','是非公开','成色完美','是非公开版的','是非公开版','就是卖价','双卡双待','标价就是卖价','瑶晴','全原可验机','完款','拍照清晰','无暗病','到线下','国行全原装','线上引流','国行全','置顶作品咨询','作品咨询','爱思全绿','全原无拆无修','的都是非','全是假的','版的手机','的全是假的','开票保修','在武汉江岸','爱思沙漏','平台上面','瑶晴数码','国行原装正品','没问题就','武汉江岸','了我微信','无拆修的','在深圳龙岗','说没问题的','搜索置顶','的全是假','卖的都是非','拆修的','三个月没','尊敬的官方','抖音里发','这平台上面','搜索置顶作品','平台上面去','混消','打的全是','版的没有','的都是低于','才跟你说','予冠','价格吸引','音里发的都是','说的是原装','说手机是','市场价的手机','你说这是非','说没问题','这平台上面去']
    # ggg = []
    # for k in kk:
    #     if k in idf_dict:
    #         _idf = idf_dict[k]
    #         ggg.append([k, get_sentence_idf(k, min_g=1, max_g=4, idf_dict=None)])
    #     else:
    #         # TODO min_g=1, max_g=4, idf_dict=None 目前是写死的
    #         _idf = get_sentence_idf(k, min_g=1, max_g=4, idf_dict=None)
    #         ggg.append([k, _idf])
    #     print(k, _idf)
    # ggg.sort(key=lambda _: _[1], reverse=False)
    #
    # print('########')
    # for g in ggg:
    #     print(g[0], g[1])

    _rst = auto_sql(
        # 种子信息
        uids=None,
        vids=[7233763677814541620,7237052313318264102,7238077359402781992,7239176677400530236],
        task_name='DATE_0523',
        folder_token='OsAkffX1ElN1PSd4GE5cJJB7n0b',
        # 主要控制参数
        epochs=1,  # 迭代次数
        keyword_limit=30,  # 好词的数量上限
        badword_limit=15,  # 坏次的数量上限
        # 第一次查询用的关键词
        do_customize_clear=True,  # 对查询出的文本做清洗
        use_top_tfidf=20,  # 第一次选关键词时选择的词数
        # 用关键词构建sql
        keyword_reward=1,  # 好词的分数
        badword_punish=-1,  # 坏词的分数
        # 筛选关键词
        top_tfidf=200,  # 每次迭代时，考虑种子查询结果和本轮查询结果中tfidf靠前的词
        min_hit=7,  # 如果被考虑的词在本轮查询结果中出现次数小鱼min_hit则忽略
        de_similar=False,  # 尚未使用
        # 更新关键词
        update_speed_keyword=5,  # 每一轮迭代更新好词的数量
        update_speed_badword=3,  # 每一轮迭代更新坏词的数量
        # 控制查sql的时间范围
        time_range_seed=30,
        time_range_optimize=10,
        time_range_final=30,
        time_range_date=-1,
        # 控制查sql的结果数量
        rst_limit_seed=2000,
        rst_limit_optimize=2000,
        rst_limit_final=10000,
        # 使用的分词方法和idf词典
        split_method='char',
        idf_method='log',
        multilingual=False,
        idf_list_limit=1000000,  # 仅读取idf词典的前一部分，以节省内存
        all_chinese=True,
        no_space=False,
        no_border_space=True,
        deduplication=False,
        # 获取idf分的方法
        keyword_rank_score=keyword_rank_score,
        # 打印提示信息
        show_template=False,
        show_sql=True,
        show_detail=True,  # 打印各函数内的提示信息
        send_step_result=True,
        lark_group_id='7216549572061954099',
        lark_sheet_limit=300,
        dump_local_file=True,
    )

    # 具体扩展vids
    auto_sql(
        uids=None,
        vids=[7244501201339911456,7244487708184300838,7244486216345750795,7244455744265915648,7244450377268006179,7244443308276108544],
        task_name='微乐麻将赌博外挂欺诈',
        epochs=1,
        skip_final=True,
        rst_limit_seed=2000,
        rst_limit_optimize=10000,
        rst_limit_final=5000,
        send2tos=False,
        time_range_seed=180,
        all_chinese=False,
        no_space=False,
        no_border_space=True,
        deduplication=True,
        sql_with_collect_set=True,
        keyword_reward_tfidf=True,
        keyword_reward_name=True,
    )
