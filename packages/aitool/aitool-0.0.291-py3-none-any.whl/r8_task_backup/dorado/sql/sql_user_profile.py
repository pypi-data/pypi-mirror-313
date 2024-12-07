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


def sql_user_profile(
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
    ids_str = ','.join(list(map(str, ids)))
    template = """
select
    user_id,
    nickname, --用户昵称
    signature, --用户签名
    avatar_uri, --头像url；按照上游server给的uri口径加工成的url
    status, --用户状态（1:正常 0:封禁）
    is_fake_user, --是否马甲用户，1是，0否
    age_range, -- 用户年龄范围，18-，18-23，24-30，31-40，41-50，50-（实际含义是50+），unknown。年龄字段相关问题请参考https://bytedance.feishu.cn/docs/doccnOtT6chohUPOZ1ypc3CgXNi#
    recommend_age_range, -- 推荐侧抖音年龄模型：0:18- ； 1:18-23； 2: 24-30； 3: 31-40； 4: 41-50； 5: 50+；-1:未知。年龄字段相关问题请参考https://bytedance.feishu.cn/docs/doccnOtT6chohUPOZ1ypc3CgXNi#。⚠️抖音系内部分析建议使用
    fans_num_all, --累计粉丝数，仅含抖音主端(20200620后开始有数)
    ky_only_child_predict, -- 未成年账号预测模型-小孩预测分，默认大于等于0.5为未成年(20201130后开始有数) https://bytedance.feishu.cn/docs/doccn5GAIilmNgxSI6aIyjqxWqg
    is_middle_older, -- 是否中老年账号，1:是，0:否 https://bytedance.feishu.cn/docs/doccnr55tsPRQOjSsMMzKwSjMZb
    is_elder_mode, -- 是否开启长辈模式(1,是；0,否) 数据从20220923开始
    is_default_nickname, --是否默认昵称；1:是；0:否（20211109开始有数据）
    is_default_avatar -- 是否默认头像；1:是；0:否（20211109开始有数据）
from
    aweme.ods_user_profile_info
where
    date=date_format(date_add(NOW(),{}),'yyyyMMdd') and 
    user_id in ({})
limit {}
        """
    parameter = (time_range_date, ids_str, limit)

    if sql_log is not None:
        sql_log.info('sql_user_profile')

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


def sql_user_profile_blue(
        ids,
        time_span=15,
        time_range_date=-1,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql=False,
        sql_log=None,
):
    if ids:
        ids_str = ','.join(list(map(str, ids)))
        template = """
select
    user_id,
    user_create_days,
    `status`,   --- 用户状态（1:正常 0:封禁）
    is_fake_user,  --- 是否马甲用户，1是，0否
    is_canceled, --- 账号是否注销，1是，0否
    os,
    city_resident,   --- 常驻城市
    report_reason_success_rate_30day,  ---30天举报原因成功率（去除恶意举报）
    publish_activeness, ---投稿活跃度 1/2/3/4 代表投稿活跃程度由低到高； -1代表近30天无投稿但有开拍；-2代表近30天无投稿且无开拍；-3代表近30天新注册用户,详见 https://bytedance.feishu.cn/docs/doccnoI8nJRTCi0hdKwMDtIhbnf#(20210823后开始有数)
    vv,  ---日播放次数
    comment_cnt, ---日comment动作数
    like_cnt, ---日like动作数
    follow_cnt, ---日关注动作数
    publish_cnt_30d, ---抖音30天投稿量级
    comment_cnt_30d, ---用户近30天主动评论次数
    dist_device_id_90d, ---近90天设备ID列表
    dist_ip_90d, ---近90天IP列表
    dist_location_90d, ---近90天根据IP解析的省份列表
    login_90d_cnt ---近90天登录次数
from
    ies_lanjun_cn.blue_army_user_di_with_log_info
where
    date=date_format(date_add(NOW(),{}),'yyyyMMdd')
    and user_id in ({})
limit {}
            """
        parameter = (time_range_date, ids_str, limit)
    else:
        template = """
select
    user_id,
    user_create_days,
    `status`,   --- 用户状态（1:正常 0:封禁）
    is_fake_user,  --- 是否马甲用户，1是，0否
    is_canceled, --- 账号是否注销，1是，0否
    os,
    city_resident,   --- 常驻城市
    report_reason_success_rate_30day,  ---30天举报原因成功率（去除恶意举报）
    publish_activeness, ---投稿活跃度 1/2/3/4 代表投稿活跃程度由低到高； -1代表近30天无投稿但有开拍；-2代表近30天无投稿且无开拍；-3代表近30天新注册用户,详见 https://bytedance.feishu.cn/docs/doccnoI8nJRTCi0hdKwMDtIhbnf#(20210823后开始有数)
    vv,  ---日播放次数
    comment_cnt, ---日comment动作数
    like_cnt, ---日like动作数
    follow_cnt, ---日关注动作数
    publish_cnt_30d, ---抖音30天投稿量级
    comment_cnt_30d, ---用户近30天主动评论次数
    dist_device_id_90d, ---近90天设备ID列表
    dist_ip_90d, ---近90天IP列表
    dist_location_90d, ---近90天根据IP解析的省份列表
    login_90d_cnt ---近90天登录次数
from
    ies_lanjun_cn.blue_army_user_di_with_log_info
where
    date=date_format(date_add(NOW(),{}),'yyyyMMdd')
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
        parameter = (time_range_date, time_range_date, time_span, time_range_date, time_span, limit)

    if sql_log is not None:
        sql_log.info('sql_user_profile_blue')

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
    rst = sql_user_profile(uid, limit=10000, show_template=True, show_sql=True)
    print(rst[:1])
    rst = sql_user_profile_blue(uid, limit=10000, show_template=True, show_sql=True)
    print(rst[:1])
