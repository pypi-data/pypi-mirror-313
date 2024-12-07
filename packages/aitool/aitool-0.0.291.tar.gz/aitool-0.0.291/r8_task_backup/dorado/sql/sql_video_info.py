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


def sql_globle_video_info(
        time_range=30,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql=False,
        sql_log=None,
):
    template = """
with a as(
    select
    user_id,
    nickname,
    status,
    signature
    from 
    aweme.mds_dm_user_id_stats
    where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd')
),
b as(
    select
    object_id,   --- 举报对象id
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(get_json_object(report_extra, '$.report_desc'),0,50))),0,500) as report_desc
    from
    ies_lanjun_cn.dwd_user_report_detail_byapp_df 
    where
    app_id=1128 and
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
    report_create_time >= unix_timestamp(NOW())-15*24*60*60
    group by object_id
),
c as (
    select
    item_id,
    ies_lanjun_cn.dwd_safe_item_change_h_di.status,
    item_title,
    music_title,
    asr1,
    asr2,
    ocr,
    province,
    city_name_cn,
    device_id,
    create_time,
    a.user_id,
    a.nickname,
    a.signature
    from 
    ies_lanjun_cn.dwd_safe_item_change_h_di left join a
    on ies_lanjun_cn.dwd_safe_item_change_h_di.author_user_id=a.user_id
    where   
    date >= date_format(date_add(NOW(),-{}),'yyyyMMdd')
    and date <= date_format(date_add(NOW(),{}),'yyyyMMdd')
)
select
c.*, 
b.report_desc
from
c left join b 
on cast(c.item_id as string)=b.object_id
limit {}
        """
    parameter = (time_range_date, time_range_date, time_range, time_range_date, limit)

    if sql_log is not None:
        sql_log.info('sql_globle_video_info')

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


def sql_vid2video_info(
        vids,
        video_time_range=30,
        report_time_range=10,
        comment_time_range=10,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql=False,
        sql_log=None,
):
    if len(vids) == 0:
        return []
    vids_str = ','.join(list(map(str, vids)))

    template = """
with b as (
    select
    object_id,   --- 举报对象id
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(get_json_object(report_extra, '$.report_desc'),0,50))),0,500) as report_desc
    from
    ies_lanjun_cn.dwd_user_report_detail_byapp_df 
    where
    app_id=1128 and
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
    report_create_time >= unix_timestamp(NOW())-{}*24*60*60
    group by object_id
),
g1 as (
    select
    group_id, -- 频/文章的item_id
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(`text`,0,50))),0,500) as item_comment
    from 
    dm_comment.dwd_comment_di_90d 
    where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and 
    app_id=1128 and
    create_time >= unix_timestamp(NOW())-{}*24*60*60
    group by group_id
),
g2 as (
    select
    user_id, ---评论用户ID
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(`text`,0,50))),0,500) as user_comment
    from 
    dm_comment.dwd_comment_di_90d 
    where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and 
    app_id=1128 and
    create_time >= unix_timestamp(NOW())-{}*24*60*60
    group by user_id
),
a as (
    select
    user_id,
    aweme_id,
    nickname,
    status,
    signature,
    b.report_desc as user_report
    from 
    aweme.mds_dm_user_id_stats left join b
    on cast(user_id as string)=b.object_id
    where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd')
),
c as (
    select
    item_id,
    ies_lanjun_cn.dwd_safe_item_change_h_di.status,
    item_title,
    music_title,
    asr1,
    asr2,
    ocr,
    province,
    city_name_cn,
    device_id,
    create_time,
    a.user_id,
    a.nickname,
    a.signature,
    a.user_report,
    a.aweme_id
    from 
    ies_lanjun_cn.dwd_safe_item_change_h_di left join a
    on ies_lanjun_cn.dwd_safe_item_change_h_di.author_user_id=a.user_id
    where   
    date >= date_format(date_add(NOW(),-{}),'yyyyMMdd')
    and date <= date_format(date_add(NOW(),{}),'yyyyMMdd')
),
d as (
    select
    c.*, 
    b.report_desc as item_report
    from
    c left join b 
    on cast(c.item_id as string)=b.object_id
),
f as (
    select
    d.*, 
    g1.item_comment
    from
    d left join g1
    on d.item_id=g1.group_id
),
h as (
    select
    f.*, 
    g2.user_comment
    from
    f left join g2
    on f.user_id=g2.user_id
),
i as (
    select
    item_id,
    poi_name
    from 
    aweme.mds_dm_item_id_stats
    where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd')
),
j as (
    select
    h.*,
    i.poi_name 
    from
    h left join i
    on h.item_id=i.item_id
),
k as (
    SELECT 
    item_id,        -- 视频id
    SUBSTRING(concat_ws(', ',collect_set(product_id)),0,500) as product_id,        -- 商品id
    SUBSTRING(concat_ws(', ',collect_set(product_name)),0,500) as product_name     -- 商品名
    FROM ies_life.dwd_item_product_info_df 
    WHERE 
    date = date_format(date_add(NOW(),{}),'yyyyMMdd')
    group by item_id
),
l as (
    select
    j.*,
    k.product_id,
    k.product_name 
    from
    j left join k
    on j.item_id=k.item_id
)
select 
*
from l 
where
item_id in ({})
limit {}
        """
    parameter = (time_range_date, report_time_range, time_range_date, comment_time_range, time_range_date,
                 comment_time_range, time_range_date, video_time_range, time_range_date, time_range_date,
                 time_range_date, vids_str, limit)

    if sql_log is not None:
        sql_log.info('sql_vid2video_info')

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


def sql_uid2video_info(
        uids,
        time_range=30,
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
with a as(
    select
    user_id,
    aweme_id,
    nickname,
    status,
    signature
    from 
    aweme.mds_dm_user_id_stats
    where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd')
),
b as(
    select
    object_id,   --- 举报对象id
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(get_json_object(report_extra, '$.report_desc'),0,50))),0,500) as report_desc
    from
    ies_lanjun_cn.dwd_user_report_detail_byapp_df 
    where
    app_id=1128 and
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
    report_create_time >= unix_timestamp(NOW())-15*24*60*60
    group by object_id
),
c as (
select
item_id,
ies_lanjun_cn.dwd_safe_item_change_h_di.status,
item_title,
music_title,
asr1,
asr2,
ocr,
province,
city_name_cn,
device_id,
create_time,
a.user_id,
a.nickname,
a.signature
from 
ies_lanjun_cn.dwd_safe_item_change_h_di left join a
on ies_lanjun_cn.dwd_safe_item_change_h_di.author_user_id=a.user_id
where   
date >= date_format(date_add(NOW(),-{}),'yyyyMMdd')
and date <= date_format(date_add(NOW(),{}),'yyyyMMdd')
)
select
c.*, 
b.report_desc
from
c left join b 
on cast(c.item_id as string)=b.object_id
where c.user_id in ({})
limit {}
        """
    parameter = (time_range_date, time_range_date, time_range, time_range_date, uids_str, limit)

    if sql_log is not None:
        sql_log.info('sql_uid2video_info')

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
    _uids = [1103546788090659, 106102499014, 1896009574661469]
    _a = sql_uid2video_info(_uids, time_range=10, limit=100, show_template=True, show_sql=True)

    _vids = [7230414975263575330, 7230365881350507791, 7229946717989309748, 7230414975263575330]
    _b = sql_vid2video_info(_vids, video_time_range=10, limit=100, show_template=True, show_sql=True)
