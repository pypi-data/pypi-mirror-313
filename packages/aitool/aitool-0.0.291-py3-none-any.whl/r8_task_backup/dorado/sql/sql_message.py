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


def sql_message(
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
    template = """
SELECT
    device_id,  ---发送人device id
    uid, ---发送人ID
    follow_type,  ---0: 无关系 ，1 ：发送者关注接收者, 2 互相关注， 3:接受者关注发送者
    `ip`,
    get_json_object(params, '$.dirty_words_detail[0].word'),
    get_json_object(params, '$.dirty_words_detail[1].word'),
    get_json_object(params, '$.dirty_words_detail[2].word'),
    get_json_object(params, '$.dirty_words_detail[3].word'),
    get_json_object(params, '$.dirty_words_detail[4].word'),
    get_json_object(params, '$.dirty_words_detail[5].word'),
    get_json_object(params, '$.to_id') as to_id,
    get_json_object(params, '$.create_time') as create_time
FROM
    aweme.stg_bhv_private_message_day
WHERE
    date = date_format(date_add(NOW(),{}),'yyyyMMdd') and 
    aid = 1128 and
    get_json_object(params, '$.create_time') >= cast(unix_timestamp(NOW())-{}*24*60*60 as String)
limit {}
        """
    parameter = (time_range_date, time_span, limit)

    if sql_log is not None:
        sql_log.info('sql_message')

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
    rst = sql_message(4, limit=1000, show_template=True, show_sql=True)
    print(rst[:1])
