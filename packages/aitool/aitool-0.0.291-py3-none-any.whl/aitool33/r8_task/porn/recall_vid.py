# -*- coding: UTF-8 -*-
from aitool import sql_controller, random_base64


def sql_recall_porn(
        dir_name=None,
        limit=10000000,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql: bool = False,
        sql_log=None,
):
    if dir_name is None:
        dir_name = random_base64(16)
    template = """
with a as (
    select
    user_id
    from 
    aweme.mds_dm_user_id_stats
    where 
    date=date_format(date_add(NOW(),-1),'yyyyMMdd')
    and is_bluev = 0
    and item_vv_all < 100000
    and recommend_age_range!='0'
),
c as (
    select  
    cast(item_id as BIGINT) item_id,
    gandalf_porn_move_prob
    from
    ies_lanjun_cn.ods_safe_item_change
    where
    date=date_format(from_unixtime(unix_timestamp(NOW())-2*60*60),'yyyyMMdd')
    and hour=date_format(from_unixtime(unix_timestamp(NOW())-2*60*60),'HH')
    and gandalf_porn_move_prob > "0.9"
)
insert overwrite DIRECTORY 'hdfs://haruna/home/byte_faceu_qa/data/yuejiaxiang/{}' row format delimited fields terminated by '\t'
select 
distinct
group_id
from
ies_lanjun_cn.dwd_safe_item_change_h_di
where
date=date_format(from_unixtime(unix_timestamp(NOW())-2*60*60),'yyyyMMdd')
and hour=date_format(from_unixtime(unix_timestamp(NOW())-2*60*60),'HH')
and author_user_id in (select * from a)
and group_id in (select item_id from c)
limit {}
"""
    parameter = (dir_name, limit)

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
    rst = sql_recall_porn()
    print(rst)
