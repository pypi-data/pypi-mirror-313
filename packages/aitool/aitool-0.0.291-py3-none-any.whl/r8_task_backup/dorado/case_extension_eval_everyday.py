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
from aitool import get_risk, case_extension_eval


if __name__ == '__main__':
    while True:
        part_id = 0
        part_all = 5
        _seed = get_risk(day=1)
        len_seed = len(_seed)
        part_seed = len_seed // part_all
        case_extension_eval(
            day=1,          # 取过去1天的种子
            part_all=5,     # 将种子分为5份
            part_id=0,      # 处理第1份种子
            size=10000,     # 取种子的前10000个视频来挖掘关键词
            use_uid=False,  # 使用种子里的uid信息
            use_vid=True,   # 使用种子里的vid信息
            choose_method=[[1, 3, 300]],        # 输出结果筛选：min_score, chosen_count, top_n
            out_time=6,                         # 每天早上6点输出一次最终结果，并终止循环
            out_group='7225142911694831644',    # 输出最终结果的飞书群
            sql_with_collect_set=True,          # sql聚合格式，提升sql结果浓度（输出到飞书表格有数据大小限制）
            time_range_date=-2,                 # sql查2天前的分区，以免0点后导致无1天前的分区
            folder_token=None,                  # 未指定飞书表格文件夹，使用默认文件夹
            keyword_reward_tfidf=True,          # keyword分数和tfidf相关
            keyword_reward_name=True,           # keyword分数依据case名称加强
            keyword_reward_name_score=10,       # keyword分数依据case名称加强的分数
            delete_short_in_long=True,          # 删除被长keyword包含的短keyword
            delete_long_in_short=False,         # 删除包含了短keyword的长keyword
            keyword_limit=60,                   # sql中使用的keyword数量
            use_top_tfidf=60,                   # 按tfidf排序选前60个keyword
        )
