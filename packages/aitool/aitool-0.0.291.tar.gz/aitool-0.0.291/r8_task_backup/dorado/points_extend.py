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
from collections import defaultdict
from aitool import get_video_similar, filter_keyword


def get_similar(
        uids=None,
        vids=None,
        keyword=None,
        threshold=0.7,
        time_range=30,
        limit=100000,
        keyword_filter=False,
        keyword_adjust=True,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
):
    # todo 待优化
    # 1、复用get_video_similar
    # 2、复用设备扩展
    # 3、复用视频相似度接口

    # data = sql_video_info(
    #     uids=uids,
    #     vids=vids,
    #     time_range=time_range,
    #     limit=limit,
    #     show_template=show_template,
    #     show_sql=show_sql,
    #     set_template=set_template,
    #     set_sql=set_sql,
    # )
    # print('search vid {}'.format(len(data)))
    # if keyword and keyword_filter:
    #     new_data = []
    #     for info in data:
    #         info_str = '\t'.join(['{}'.format(_) for _ in info])
    #         if filter_keyword(info_str, keyword, min_count=1):
    #             new_data.append(info)
    #     data = new_data
    #     print('after keyword filter vid {}'.format(len(data)))
    # query_vids = [info[0] for info in data]
    # query_rst = get_video_similar(query_vids)
    # print('search similar vid {}'.format(len(query_rst)))
    # similar_vid_set = set()
    # similar_vid2score = defaultdict(float)
    # for ori_vid, similar_vid, score in query_rst:
    #     if score < threshold:
    #         continue
    #     if similar_vid in query_vids:
    #         continue
    #     similar_vid_set.add(similar_vid)
    #     similar_vid2score[similar_vid] = max(similar_vid2score[similar_vid], score)
    # print('chosen similar vid {}'.format(len(similar_vid_set)))
    # if keyword_adjust:
    #     data = sql_video_info(
    #         vids=list(similar_vid_set),
    #         time_range=time_range,
    #         limit=limit,
    #         show_template=show_template,
    #         show_sql=show_sql,
    #         set_template=set_template,
    #         set_sql=set_sql,
    #     )
    #     print('get info for similar vid {}'.format(len(data)))
    #     for info in data:
    #         info_str = '\t'.join(['{}'.format(_) for _ in info])
    #         info_vid = info_str[0]
    #         if filter_keyword(info_str, keyword, min_count=1):
    #             similar_vid2score[info_vid] += 0.2
    # rst = [[k, v] for k, v in similar_vid2score.items()]
    # rst.sort(key=lambda _: _[1], reverse=True)
    rst = []
    return rst


def get_group_id():
    pass
