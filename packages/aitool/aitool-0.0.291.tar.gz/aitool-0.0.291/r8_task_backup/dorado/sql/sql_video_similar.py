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
from aitool import sql_controller
import json


def sql_video_similar(
        ids,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql=False,
        sql_log=None,
):
    if len(ids) == 0:
        return []
    ids_str = ','.join(list(map(str, ids)))

    template = """
SELECT
    id,
    product_id,
    app_id,
    attrs,
    create_time,
    modify_time
FROM
    aweme.ods_mysql_ies_item_attr_attr_info_df
WHERE
    date = date_format(date_add(NOW(),{}),'yyyyMMdd')
    and id in ({})
limit {}
        """
    parameter = (time_range_date, ids_str, limit)

    if sql_log is not None:
        sql_log.info('sql_video_similar')

    return sql_controller(
        template,
        parameter,
        show_template=show_template,
        show_sql=show_sql,
        set_template=set_template,
        set_sql=set_sql,
        return_sql=return_sql,
        sql_log=sql_log,
    )


def get_video_similar(
        vids,
        threshold=0,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
):
    # 输出格式[['ori_vid', 'similar_vid', 'score']]
    if len(vids) == 0:
        return []
    data = sql_video_similar(vids, time_range_date=time_range_date, limit=limit, show_template=show_template, show_sql=show_sql,
                             set_template=set_template, set_sql=set_sql)
    rst = []
    for line in data:
        y = json.loads(line[3])
        if 'hotdedup_cdd' not in y:
            continue
        z = json.loads(y['hotdedup_cdd'])
        for _ in z['info']:
            sim_vid = _['pair_id']
            sim_score = _['similarity']
            if sim_score >= threshold:
                rst.append([id, sim_vid, sim_score])
    print('ori_vid', len(vids), 'similar_vid', len(rst)-1)
    return rst


def sql_group_id(
        uids,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql=False,
        sql_log=None,
):
    if len(uids) == 0:
        return []
    uids_str = ','.join(list(map(str, uids)))

    template = """
with 
a as (
    select
    item_id,
    author_id,
    group_id
    from
    aweme.mds_dm_item_id_stats
    where
    app_id=1128 and
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
    author_id in ({})
),
b as (
    select
    distinct item_id, author_id, aweme_id
    from 
    aweme.mds_dm_item_id_stats
    where 
    app_id=1128 and
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
    group_id in (
        select
        distinct group_id
        from 
        a
    )
)
select 
distinct author_id, aweme_id
from
b
where
author_id not in ({})
limit {}
        """
    parameter = (time_range_date, uids_str, time_range_date, uids_str, limit)

    if sql_log is not None:
        sql_log.info('sql_group_id')

    return sql_controller(
        template,
        parameter,
        show_template=show_template,
        show_sql=show_sql,
        set_template=set_template,
        set_sql=set_sql,
        return_sql=return_sql,
        sql_log=sql_log,
    )


if __name__ == '__main__':
    vid = [7205068565576289536, 7204848175662812451,7204762869739638016]
    print(get_video_similar(vid, threshold=0, limit=100))
