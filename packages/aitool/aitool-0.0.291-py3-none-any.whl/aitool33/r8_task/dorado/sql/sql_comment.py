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
ies_lanjun_cn.dwd_user_report_detail_byapp_df
"""
from typing import Dict, Union, List, Any, NoReturn, Tuple

from aitool import sql_controller


def sql_comment(
        ids,
        time_span=15,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql: bool = False,
        text_filter: bool = True,
        text_filter_exp: str = '枪|钱|微信|qq|转账|充电|上门',
        sql_log=None,
):
    text_filter_sentence = ''
    if text_filter:
        text_filter_sentence = """and `text` regexp '{}'""".format(text_filter_exp)
    if ids:
        ids_str = ','.join(list(map(str, ids)))
        template = """
select
    `status`, ---0:DELETE 1:ALL_VISIBLE 2:SELF_VISIBLE 3:FRIEND_VISIBLE 4:PUBLISH 5:STAR 7:UNPROCESSED 8:PARTVISIBLE 详细请参考：https://site.bytedance.net/docs/1715/1946/19960/
    user_id, ---评论用户ID
    group_id, ---在哪篇文章下面, 视频/文章的item_id
    review_status, ---0:未审 1:不通过 2:通过且不限制可热 3:通过且不可热 4:通过且可热 5:通过且置顶 6:通过且置底
    create_time, ---创建时间
    `text`,  ---评论内容
    comment_count,  ---一个评论下面的评论/回复数
    login_digg_count,  ---登录用户点赞数
    login_bury_count  ---登录用户点踩数
from 
    dm_comment.dwd_comment_di_90d 
where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') 
    and app_id=1128
    and `status` in (1,3,8)
    {}
    and create_time >= unix_timestamp(NOW())-{}*24*60*60
    and user_id in ({})
limit {}
            """
        parameter = (time_range_date, text_filter_sentence, time_span, ids_str, limit)
    else:
        template = """
select
    `status`, ---0:DELETE 1:ALL_VISIBLE 2:SELF_VISIBLE 3:FRIEND_VISIBLE 4:PUBLISH 5:STAR 7:UNPROCESSED 8:PARTVISIBLE 详细请参考：https://site.bytedance.net/docs/1715/1946/19960/
    user_id, ---评论用户ID
    group_id, ---在哪篇文章下面, 视频/文章的item_id
    review_status, ---0:未审 1:不通过 2:通过且不限制可热 3:通过且不可热 4:通过且可热 5:通过且置顶 6:通过且置底
    create_time, ---创建时间
    `text`,  ---评论内容
    comment_count,  ---一个评论下面的评论/回复数
    login_digg_count,  ---登录用户点赞数
    login_bury_count  ---登录用户点踩数
from 
    dm_comment.dwd_comment_di_90d 
where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') 
    and app_id=1128
    and `status` in (1,3,8)
    {}
    and create_time >= unix_timestamp(NOW())-{}*24*60*60
    and user_id in (
        select
            distinct reporter_id --- 举报人id
        from
            ies_lanjun_cn.dwd_user_report_detail_byapp_df 
        where
            app_id=1128 and
            date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
            report_create_time >= unix_timestamp(NOW())-{}*24*60*60 and 
            get_json_object(report_extra, '$.report_desc') regexp '引导|黑话|色情|招嫖|低俗|赌|黄|毒|诈骗'
        UNION
        select
            distinct object_owner_id  --- 举报对象所属人uid
        from
            ies_lanjun_cn.dwd_user_report_detail_byapp_df 
        where
            app_id=1128 and
            date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
            report_create_time >= unix_timestamp(NOW())-{}*24*60*60 and
            get_json_object(report_extra, '$.report_desc') regexp '引导|黑话|色情|招嫖|低俗|赌|黄|毒|诈骗'
    )
limit {}
            """
        parameter = (time_range_date, text_filter_sentence, time_span, time_range_date, time_span, time_range_date, time_span, limit)

    if sql_log is not None:
        sql_log.info('sql_comment')

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


def sql_comment_extend(
        ids,
        time_span=15,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql: bool = False,
        sql_log=None,
):
    ids_str = ','.join(list(map(str, ids)))
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
    object_id,
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(get_json_object(report_extra, '$.report_desc'),0,50))),0,500) as report_desc
    from
    ies_lanjun_cn.dwd_user_report_detail_byapp_df 
    where
    app_id=1128 and
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
    report_create_time >= unix_timestamp(NOW())-{}*24*60*60
    group by object_id
),
c as (
    select
    comment_id,
    `status`, ---0:DELETE 1:ALL_VISIBLE 2:SELF_VISIBLE 3:FRIEND_VISIBLE 4:PUBLISH 5:STAR 7:UNPROCESSED 8:PARTVISIBLE 详细请参考：https://site.bytedance.net/docs/1715/1946/19960/
    user_id, ---评论用户ID
    group_id, ---在哪篇文章下面, 视频/文章的item_id
    review_status, ---0:未审 1:不通过 2:通过且不限制可热 3:通过且不可热 4:通过且可热 5:通过且置顶 6:通过且置底
    create_time, ---创建时间
    `text`  ---评论内容
    from 
    dm_comment.dwd_comment_di_90d 
    where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and 
    app_id=1128 and
    create_time >= unix_timestamp(NOW())-{}*24*60*60
),
d as (
    select
    c.*, 
    b.report_desc
    -- ,if(b.report_desc regexp '肉800', '1', 0)+if(b.report_desc regexp '1000多', '1', 0) as count_keyword_r
    from
    c left join b 
    on cast(c.user_id as string)=b.object_id
),
e as (
    select d.*,
    a.nickname,
    a.status as user_status,
    a.signature
    from 
    d left join a
    on d.user_id = a.user_id
),
f as (
    select 
    user_id,
    concat_ws(', ',collect_set(nickname)) as nickname,
    concat_ws(', ',collect_set(signature)) as signature,
    concat_ws(', ',collect_list(text)) as comment,
    concat_ws(', ',collect_set(report_desc)) as report,
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(text,0,50))),0,500) as feature_cmt,
    SUBSTRING(concat_ws(', ',collect_set(SUBSTRING(report_desc,0,50))),0,500) as feature_report
    from
    e
    group by user_id
),
g as (
    select *, 
    concat(feature_cmt, feature_report) as feature
    from f
)
select 
user_id,
nickname,
signature,
comment,
report,
feature
from g
where user_id in ({})
limit {}
    """
    parameter = (time_range_date, time_range_date, time_span, time_range_date, time_span, ids_str, limit)

    if sql_log is not None:
        sql_log.info('sql_comment_extend')

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
    uid = [66533925866, 62451892219, 62079643554]
    rst = sql_comment(uid, time_span=15, limit=10000, show_template=True, show_sql=True)
    print(rst[:1])
