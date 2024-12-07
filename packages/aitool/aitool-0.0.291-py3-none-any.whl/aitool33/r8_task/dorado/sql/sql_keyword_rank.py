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


def sql_video_keyword_rank(
        keywords: Union[List[str], Dict[str, float]],
        badwords: Union[List[str], Dict[str, float]],
        keyword2fields: dict = None,
        video_time_range=30,
        report_time_range=10,
        comment_time_range=10,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        keyword_reward=1,
        badword_punish=-1,
        return_sql=False,
        sql_log=None,
        exclude_uid=None,
        keyword_reward_tfidf=False,
        keyword_reward_tfidf_score=None,
):
    keyword2score = {}
    for k in keywords:
        if keyword_reward_tfidf:
            keyword2score[k] = keyword_reward_tfidf_score[k]
        else:
            keyword2score[k] = keyword_reward
    for k in badwords:
        keyword2score[k] = badword_punish

    condition_template_field = """{} regexp '{}'"""
    condition_template_part = """if({}, {}, 0)"""
    all_condition = []
    for k, v in keyword2score.items():
        if k not in keyword2fields:
            print(k, 'not in keyword2fields')
            continue
        condition_fileds = []
        for f in keyword2fields[k]:
            condition_fileds.append(condition_template_field.format(f, k))
        all_condition.append(condition_template_part.format(' or '.join(condition_fileds), v))
    condition_str = '+\n    '.join(all_condition) + '\n    as count_keyword'
    if exclude_uid is None or len(exclude_uid) == 0:
        exclude_str = ''
    else:
        exclude_uid_str = ','.join(map(str, exclude_uid))
        exclude_str = 'and user_id not in ({})'.format(exclude_uid_str)

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
),
m as (
    select
    *,
    {}
    from l
)
select 
*
from m
where m.count_keyword >= 1
{}
order by m.count_keyword desc
limit {}
            """
    parameter = (time_range_date, report_time_range, time_range_date, comment_time_range, time_range_date,
                 comment_time_range, time_range_date, video_time_range, time_range_date, time_range_date,
                 time_range_date, condition_str, exclude_str, limit)

    if sql_log is not None:
        sql_log.info('sql_video_keyword_rank')

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


def sql_video_keyword_rank_with_collect_set(
        keywords: List[str],
        badwords: List[str],
        keyword2fields: dict = None,
        video_time_range=30,
        report_time_range=10,
        comment_time_range=10,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        keyword_reward=1,
        badword_punish=-1,
        return_sql=False,
        sql_log=None,
        exclude_uid=None,
        keyword_reward_tfidf=False,
        keyword_reward_tfidf_score=None,
):
    keyword2score = {}
    for k in keywords:
        if keyword_reward_tfidf:
            keyword2score[k] = keyword_reward_tfidf_score[k]
        else:
            keyword2score[k] = keyword_reward
    for k in badwords:
        keyword2score[k] = badword_punish

    condition_template_field = """{} regexp '{}'"""
    condition_template_part = """if({}, {}, 0)"""
    all_condition = []
    for k, v in keyword2score.items():
        if k not in keyword2fields:
            print(k, 'not in keyword2fields')
            continue
        condition_fileds = []
        for f in keyword2fields[k]:
            condition_fileds.append(condition_template_field.format(f, k))
        all_condition.append(condition_template_part.format(' or '.join(condition_fileds), v))
    condition_str = '+\n    '.join(all_condition) + '\n    as count_keyword'
    if exclude_uid is None or len(exclude_uid) == 0:
        exclude_str = ''
    else:
        exclude_uid_str = ','.join(map(str, exclude_uid))
        exclude_str = 'and user_id not in ({})'.format(exclude_uid_str)

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
),
m as (
    select
    *,
    {}
    from l
),
o as (
    select
    concat_ws(',',slice(collect_list(item_id),1,5)) as item_id,
    concat_ws(',',slice(collect_list(status),1,5)) as status,
    concat_ws(',',slice(collect_list(item_title),1,5)) as item_title,
    concat_ws(',',slice(collect_list(music_title),1,5)) as music_title,
    concat_ws(',',slice(collect_list(asr1),1,5)) as asr1,
    concat_ws(',',slice(collect_list(asr2),1,5)) as asr2,
    concat_ws(',',slice(collect_list(ocr),1,5)) as ocr,
    concat_ws(',',slice(collect_list(province),1,5)) as province,
    concat_ws(',',slice(collect_list(city_name_cn),1,5)) as city_name_cn,
    concat_ws(',',slice(collect_list(device_id),1,5)) as device_id,
    concat_ws(',',slice(collect_list(create_time),1,5)) as create_time,
    user_id,
    concat_ws(',',slice(collect_list(nickname),1,5)) as nickname,
    concat_ws(',',slice(collect_list(signature),1,5)) as signature,
    concat_ws(',',slice(collect_list(user_report),1,5)) as user_report,
    concat_ws(',',slice(collect_list(aweme_id),1,5)) as aweme_id,
    concat_ws(',',slice(collect_list(item_report),1,5)) as item_report,
    concat_ws(',',slice(collect_list(item_comment),1,5)) as item_comment,
    concat_ws(',',slice(collect_list(user_comment),1,5)) as user_comment,
    concat_ws(',',slice(collect_list(poi_name),1,5)) as poi_name,
    concat_ws(',',slice(collect_list(product_id),1,5)) as product_id,
    concat_ws(',',slice(collect_list(product_name),1,5)) as product_name,
    max(count_keyword) as count_keyword,
    size(collect_list(count_keyword)) as size_count_keyword,
    slice(collect_list(count_keyword),1,100) as sample_count_keyword
    from 
    m
    where count_keyword > 0
    group by user_id
)
SELECT
*
from 
o
where count_keyword > 0
{}
order by o.count_keyword desc
limit {}
            """
    parameter = (time_range_date, report_time_range, time_range_date, comment_time_range, time_range_date,
                 comment_time_range, time_range_date, video_time_range, time_range_date, time_range_date,
                 time_range_date, condition_str, exclude_str, limit)
    if sql_log is not None:
        sql_log.info('sql_video_keyword_rank')

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
    from aitool import sql_video_keyword_rank
    rst = sql_video_keyword_rank(
        ['单手模式', '杨过模式', '单手游戏', 'NTR'],    # 好词
        [],                                         # 坏词
        limit=100,
        show_template=True,
        show_sql=True,
        set_template='',
        set_sql='',
    )
    print(rst[:1])


