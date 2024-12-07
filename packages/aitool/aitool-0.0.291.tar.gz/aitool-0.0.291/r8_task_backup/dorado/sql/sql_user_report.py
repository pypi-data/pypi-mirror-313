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


def sql_user_report(
        time_span,
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
select
    reporter_id, --- 举报人id
    object_id,   --- 举报对象id
    object_type, --- 举报类型 101:视频；102评论；103:用户；105:音乐；106:私信；121:喜欢页举报；115 :群聊举报等等
    object_owner_id,  --- 举报对象所属人uid
    report_reason,   --- 举报原因；https://bytedance.feishu.cn/sheets/shtcnjarMSs1kn6VObqnmFhOTxc
    get_json_object(report_extra, '$.report_desc') as report_desc,
    report_create_time,
    report_status  --- 1审核中 2举报成功(有处罚)3举报失败（无处罚）0 对齐失败（异常数据）
from
    ies_lanjun_cn.dwd_user_report_detail_byapp_df 
where
    app_id=1128 
    and date=date_format(date_add(NOW(),{}),'yyyyMMdd') 
    and report_create_time >= unix_timestamp(NOW())-{}*24*60*60
    and get_json_object(report_extra, '$.report_desc') regexp '色情|嫖|低俗|赌|黄|毒|骗'
limit {}
        """
    parameter = (time_range_date, time_span, limit)

    if sql_log is not None:
        sql_log.info('sql_user_report')

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


def sql_user_report_comment(
        time_span,
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
select 
    reporter_id, ---举报人id
    comment_user_id, ---评论作者
    report_reason, ---举报原因
    report_reason_desc, ---举报原因描述
    report_create_time, ---举报创建时间
    report_status, ---举报结果；1审核中 2举报成功(有处罚)3举报失败（无处罚）0 对齐失败（异常数据
    get_json_object(report_extra, '$.more_description') as report_desc,
    comment_text, ---评论内容
    get_json_object(comment_extra, '$.create_realtime') as comment_create_realtime,
    get_json_object(comment_extra, '$.location') as comment_location, 
    group_id, ---视频/文章ID
    author_id ---视频/文章作者
from 
    dm_comment.dwd_comment_report_di 
where 
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and
    report_create_time >= cast(unix_timestamp(NOW())-{}*24*60*60 as String)
limit {}
        """
    parameter = (time_range_date, time_span, limit)

    if sql_log is not None:
        sql_log.info('sql_user_report_comment')

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
    rst = sql_user_report(15, limit=10, show_template=True, show_sql=True)
    print(rst[:1])
    rst = sql_user_report_comment(15, limit=10, show_template=True, show_sql=True)
    print(rst[:1])
