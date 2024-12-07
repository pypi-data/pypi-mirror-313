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
from aitool import get_file, load_lines, load_excel, split_path, dump_pickle
from typing import Dict, Union, List, Any, NoReturn, Tuple
import time
from time import sleep
from collections import defaultdict
from random import sample
from aitool import case_extension, refactor_auto_sql, send_feishu_sheet, get_log, load_pickle, sql_result2list, \
    get_ngram, get_risk, split_path


def case_extension_eval(
        part_id=0,
        part_all=5,
        day=1,
        size=20,
        use_uid=True,
        use_vid=True,
        choose_method=None,
        out_time=6,
        alive_hour=23,
        out_group='7225142911694831644',
        **kwargs,
):
    # seed的结构：
    # [{
    #     'name': str,        名称
    #     'link': str,  附加信息
    #     'uid': List[Union[str, int]],   种子uid
    #     'vid': List[Union[str, int]],   种子vid
    # }, ...]

    begin_time = time.time()
    begin_data = time.localtime(begin_time).tm_mday

    all_seed = get_risk(day=day)
    len_seed = len(all_seed)
    part_seed = len_seed // part_all
    begin = part_id * part_seed
    end = (part_id + 1) * part_seed

    if choose_method is None:
        choose_method = [
            [1, 1, 1000],
            [1, 3, 300],
        ]
    print('len seed', len(all_seed), 'range', begin, end)
    loger = get_log('extend_seed.log')
    # 受限于接口对数据包大小的限制，各列表只展示最多50个项
    all_rst = [[
        'case名',
        '全部uid',
        '全部uid数量',
        '种子uid',
        '全部vid',
        '种子vid',
        '扩散结果（uid）',
        '扩散结果的最高分',
        '扩展的uid数量',
        '所有扩展的vid的可见率',
        '种子详情文档',
        '过滤分数',
        '必要视频数',
        'TOP_N',
        '选中的详情文档',
        '准确率',
        '召回率',
        '多召case',
        '漏召case',
        '250~300质量分',
        'sample_1_10',
        'sample_41_50',
        'sample_141_150',
        'sample_291_300',
        'scores_1_10',
        'scores_41_50',
        'scores_141_150',
        'scores_291_300',
    ]]
    for sd_idx, sd in enumerate(all_seed[begin: end]):
        try:
            if 'name' in sd and sd['name'] is not None and len(sd['name']) > 0:
                seed_name = sd['name']
            else:
                seed_name = 'no_task_name'
            if 'link' in sd:
                seed_link = sd['link']
            else:
                seed_link = ''
            if 'uid' in sd and sd['uid'] is not None and len(sd['uid']) > 0:
                seed_uid = sd['uid']
                if use_uid:
                    seed_uid_chosen = sample(seed_uid, min(size, len(seed_uid)))
                else:
                    seed_uid_chosen = []
            else:
                seed_uid = []
                seed_uid_chosen = []
            if 'vid' in sd and sd['vid'] is not None and len(sd['vid']) > 0:
                seed_vid = sd['vid']
                if use_vid:
                    seed_vid_chosen = sample(seed_vid, min(size, len(seed_vid)))
                else:
                    seed_vid_chosen = []
            else:
                seed_vid = []
                seed_vid_chosen = []

            rst, uids, vids, task_name, all_links, seed_vid_info = case_extension(
                task_name=seed_name,
                uids=seed_uid_chosen,
                vids=seed_vid_chosen,
                all_chinese=False,
                no_space=False,
                no_border_space=True,
                deduplication=True,
                **kwargs,
            )
            text_seed_vid = sql_result2list(
                seed_vid_info,
                row=['item_title', 'music_title', 'asr1', 'asr2', 'ocr', 'province', 'city_name_cn', 'nickname',
                     'signature', 'user_report', 'item_report', 'item_comment', 'user_comment', 'poi_name',
                     'product_name']
            )
            text_seed_vid = ['。'.join(map(str, text_one)) for text_one in text_seed_vid]

            send_sheet_first_time = True
            the_link = ''
            for min_score, chosen_count, top_n in choose_method:
                rst, chosen_uids, chosen_score, detail_link, text_250_300, quality_scores, simples = refactor_auto_sql(
                    rst,
                    uids,
                    vids,
                    task_name,
                    all_links,
                    min_score=min_score,
                    chosen_count=chosen_count,
                    send_sheet=send_sheet_first_time,
                    **kwargs,
                )
                if send_sheet_first_time:
                    send_sheet_first_time = False
                    the_link = detail_link
                rst = rst[:top_n]
                chosen_uids = chosen_uids[:top_n]
                chosen_score = chosen_score[:top_n]

                # 计算text_seed_vid和text_250_300的3-gram相似度
                from collections import Counter
                str_seed_vid = '。'.join(text_seed_vid)
                str_250_300 = '。'.join(text_250_300)
                str_seed_vid = str_seed_vid.replace('None', '')
                str_250_300 = str_250_300.replace('None', '')
                gram_2_seed_vid = list(get_ngram(str_seed_vid, ngram=2, no_chars='，。,[] '))
                gram_2_250_300 = list(get_ngram(str_250_300, ngram=2, no_chars='，。,[] '))
                len_seed_vid = len(gram_2_seed_vid)
                len_250_300 = len(gram_2_250_300)
                counter_seed_vid = Counter(gram_2_seed_vid)
                counter_250_300 = Counter(gram_2_250_300)
                sim_score = 0
                for k, v in counter_seed_vid.items():
                    if k in counter_250_300:
                        sim_score += (v/len_seed_vid) * (counter_250_300[k]/len_250_300)


                # 计算公开可见率
                rst_state = [_.asDict()['status'] for _ in rst]
                if len(rst_state) > 0:
                    count_open = 0
                    for item_state in rst_state:
                        if item_state == 102 or item_state == '102':
                            count_open += 1
                    rst_open_rate = round(count_open / len(rst_state), 3)
                else:
                    rst_open_rate = ''
                # 计算召回率\准确率\待标（有顺序）\漏召 (仅对uid维度)
                chosen_uids = [str(u) for u in chosen_uids]
                hit = set(chosen_uids) & set(seed_uid)
                if len(chosen_uids) > 0:
                    hit_p = len(hit) / len(chosen_uids)
                else:
                    hit_p = 'None'
                if len(seed_uid) > 0:
                    hit_r = len(hit) / len(seed_uid)
                else:
                    hit_r = 'None'
                hit_more = []
                for _u in chosen_uids:
                    if _u not in seed_uid:
                        hit_more.append(_u)
                hit_less = []
                for _u in seed_uid:
                    if _u not in chosen_uids:
                        hit_less.append(_u)

                # 构建输出格式
                seed_uid_size = len(seed_uid)
                seed_uid_str = ','.join(map(str, seed_uid[:50]))
                seed_uid_chosen_str = ','.join(map(str, seed_uid_chosen[:50]))
                seed_vid_str = ','.join(map(str, seed_vid[:50]))
                seed_vid_chosen_str = ','.join(map(str, seed_vid_chosen[:50]))
                chosen_uid_str = ','.join(map(str, chosen_uids[:50]))
                chosen_score_str = ','.join(map(str, chosen_score[:50]))
                all_rst.append([
                    seed_name,
                    seed_uid_str,
                    seed_uid_size,
                    seed_uid_chosen_str,
                    seed_vid_str,
                    seed_vid_chosen_str,
                    chosen_uid_str,
                    chosen_score_str,
                    len(chosen_uids),
                    rst_open_rate,
                    seed_link,
                    min_score,
                    chosen_count,
                    top_n,
                    the_link,
                    hit_p,
                    hit_r,
                    ','.join(map(str, hit_more[:50])),
                    ','.join(map(str, hit_less[:50])),
                    sim_score,
                    simples['sample_1_10'],
                    simples['sample_41_50'],
                    simples['sample_141_150'],
                    simples['sample_291_300'],
                    quality_scores['scores_1_10'],
                    quality_scores['scores_41_50']/quality_scores['scores_1_10'],
                    quality_scores['scores_141_150']/quality_scores['scores_1_10'],
                    quality_scores['scores_291_300']/quality_scores['scores_1_10'],
                ])
            print('send all_rst')
            folder_token = None if 'folder_token' not in kwargs else kwargs['folder_token']
            send_feishu_sheet(
                all_rst,
                folder_token=folder_token,
                result_title='AUTO_SQL_b{}_e{}_step{}'.format(begin, end, len(all_rst)),
            )

            # 最终输出+终止, 未跑完则在第二天的N点 or 已跑完 or 已运行超过alive_time
            now_time = time.time()
            now_data = time.localtime(now_time).tm_mday
            now_hour = time.localtime(now_time).tm_hour
            run_time = (now_time - begin_time) / (60*60)
            print('begin_data', begin_data)
            print('now_data', now_data)
            print('now_hour', now_hour)
            print('run_time', run_time)
            print('end', (now_data != begin_data and now_hour >= out_time) or (sd_idx == end-begin-1)
                  or (run_time >= alive_hour))
            if (now_data != begin_data and now_hour >= out_time) or (sd_idx == end-begin-1) or (run_time >= alive_hour):
                rst_sfs = send_feishu_sheet(
                    all_rst,
                    folder_token=folder_token,
                    lark_group_id=out_group,
                    result_title='AUTO_SQL_b{}_e{}_step{}'.format(begin, end, len(all_rst)),
                )
                print('End \n{}'.format(rst_sfs))
                break
        except Exception as e:
            print('Error @@@@@@@@@@@@@@@@@@@@@@@')
            print(sd)
            print(e)
            loger.warning(e)


if __name__ == '__main__':
    # 批量测试
    part_id = 0
    part_all = 4
    _seed = load_pickle('./offline_eval_data_1686585600.pkl')
    len_seed = len(_seed)
    part_seed = len_seed // part_all
    case_extension_eval(_seed, begin=part_id*part_seed, end=(part_id+1)*part_seed, sql_with_collect_set=True,
                        time_range_date=-2, size=10000, use_uid=False)


    # 在线测试 - 仅用核心视频
    from aitool import get_risk, case_extension_eval


    def extend_seed(seed):
        new_seed = []
        for s in seed:
            new_seed.append(s)
            vidp = s['name'].split('7', 1)[1]
            vidp = '7'+vidp
            vidp = vidp.replace('，', ',')
            vidp = vidp.split(',')
            new_seed.append({
                'name': 'short_' + s['name'],
                'link': s['link'],
                'uid': None,
                'vid': vidp,
            })
        return new_seed

    part_id = 1
    part_all = 2
    _seed = get_risk(day=3)
    _seed = extend_seed(_seed)
    len_seed = len(_seed)
    part_seed = len_seed // part_all
    case_extension_eval(
        _seed,
        begin=part_id * part_seed,
        end=(part_id + 1) * part_seed,
        sql_with_collect_set=True,
        time_range_date=-2,
        size=10000,
        use_uid=False,
        folder_token='WIc8fIMiflERsTdxJwhcTsS2nQf',
        choose_method=[[1, 3, 300]],
        keyword_reward_tfidf=True,
        keyword_reward_name=True,
        keyword_reward_name_score=10,
        delete_short_in_long=True,
        delete_long_in_short=False,
        keyword_limit=30,
        use_top_tfidf=30,
    )

    # 在线测试 - 仅用核心视频
    from aitool import get_risk, case_extension_eval

    part_id = 1
    part_all = 5
    _seed = get_risk(day=1)
    len_seed = len(_seed)
    part_seed = len_seed // part_all
    case_extension_eval(
        _seed,
        begin=part_id * part_seed,
        end=(part_id + 1) * part_seed,
        sql_with_collect_set=True,
        time_range_date=-2,
        size=10000,
        use_uid=False,
        folder_token='WIc8fIMiflERsTdxJwhcTsS2nQf',
        choose_method=[[1, 3, 300]],
        keyword_reward_tfidf=True,
        keyword_reward_name=True,
        keyword_reward_name_score=10,
        delete_short_in_long=True,
        delete_long_in_short=True,
        keyword_limit=40,
        use_top_tfidf=40,
    )

    from aitool import case_extension_eval

    # 单个case
    _seed = [{
        'name': '通天代',  # 名称
        'link': '',  # 附加信息
        'uid': [92709099898, 1042812094919267, 706308113443140, 673379112987015, 917430653435340, 180758507435216,
                57652283180539, 87884677276, 831708785814493, 3628868086544264, 583184630955791, 3879495212993048,
                3620031982738080, 94874657057, 4420514408043044, 1394631870265768, 1744264650038078, 1684912418601279,
                1825619763277645, 3943268426977357, 840477649673684, 3943292222324184, 3470480163482974,
                3404542327926893, 2397413345349752, 64797453606, 72564328690],  # 种子uid
        'vid': [],  # 种子vid
    }]
    case_extension_eval(
        _seed,
        folder_token='SIvjfyFhglJ63tdKhRDcPWSGnjc',
        begin=0,
        end=100,
        sql_with_collect_set=True,
        time_range_date=-2,
        size=10000,
        use_uid=True,
        choose_method=[[1, 3, 300]],
        keyword_reward_tfidf=True,
        keyword_reward_name=True,
        keyword_reward_name_score=10,
        delete_short_in_long=True,
        delete_long_in_short=False,
        keyword_limit=60,
        use_top_tfidf=60,
    )
