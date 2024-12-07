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
from collections import defaultdict
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import print_yellow, pip_install, print_green


def sql_collect(sql):
    try:
        from pyspark.sql import SparkSession
    except ModuleNotFoundError as e:
        pip_install('pyspark')
        from pyspark.sql import SparkSession
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    ss = spark.sql(sql)
    result = []
    try:
        result = ss.collect()
    except Exception as e:
        print('Error!!!!')
        print('in sql_collect')
        print(e)
    return result


def is_available(table_name, time_span):
    sql = """
        select
        distinct date
        from
        {}
        where
        date=date_format(date_add(NOW(),{}),'yyyyMMdd')
        """.format(table_name, time_span)
    result = sql_collect(sql)
    if len(result) == 0:
        return False
    return True


def sql_line2header(sql_line):
    return list(sql_line.asDict().keys())


def sql_result2list(sql_result, row: List[Union[int, str]] = None, add_header=True) -> List[List]:
    rst = []
    if len(sql_result) == 0:
        print('Warning: sql_result length is 0')
        return rst
    all_header = sql_line2header(sql_result[0])
    chosen_header = []
    if row is None:
        chosen_header = all_header
    else:
        for row_idx in row:
            if isinstance(row_idx, int):
                chosen_header.append(all_header[row_idx])
            elif isinstance(row_idx, str):
                chosen_header.append(row_idx)
    if add_header:
        rst.append(chosen_header)
    for line in sql_result:
        chosen = []
        line_dict = line.asDict()
        for name in chosen_header:
            chosen.append(line_dict[name])
        rst.append(chosen)
    return rst


def sql_result2text(sql_result, all_info=False, separator=' ', get_field2text=False):
    # 将查询结果里每行的信息拼接成字符串输出
    # 默认仅拼接文本内容 all_info=False
    # 可设置为拼接全部内容 all_info=True
    rst = []
    field2text = defaultdict(list)
    for line in sql_result:
        selected_value = []
        for field, value in line.asDict().items():
            if not all_info and not isinstance(value, str):
                continue
            selected_value.append(str(value))
            field2text[field].append(str(value))
            rst.append(separator.join(selected_value))
    if get_field2text:
        return rst, field2text
    else:
        return rst


def get_keyword2fields(keywords, field2text, print_info=True):
    keyword2fields = defaultdict(set)
    for word in keywords:
        for field, texts in field2text.items():
            count_texts = len(texts)
            count_contain = 0
            for text in texts:
                if word in text:
                    count_contain += 1
                    keyword2fields[word].add(field)
            if print_info:
                if count_contain > 0 and count_texts > 0:
                    print('keyword in field', word, field, count_contain, count_texts, count_contain/count_texts)
    return keyword2fields


def sql_controller(
        template,
        parameter,
        show_template=False,
        show_sql=False,
        set_template: str = '',
        set_sql: str = '',
        return_sql: bool = False,
        sql_log=None,
):
    # template里不可以包括set指令，无法正确执行，set的参数需要再dorado里设置
    if 'set ' in template:
        print_yellow('Warning: 不支持set指令，无法正确执行')
    # 用于增强用户对sql的定制化能力
    if set_template:
        template = set_template
    if show_template:
        print_yellow('### SQL模板 ###')
        print_green(template)
        print_yellow('### 模板参数 ###')
        for p in parameter:
            print_green(p)
    sql = template.format(*parameter)
    if set_sql:
        print_yellow("""
        注意: 本方法基于下标处理查询结果。自定义的sql请确保结果的前N列和原本一致，额外字段请添加到尾部。通过show_sql=True可查看原本的sql。
        """)
        sql = set_sql
    if show_sql:
        print_yellow('### SQL ###')
        print_green(sql)
    if sql_log is not None:
        sql_log.info(sql)

    # 执行sql
    result = sql_collect(sql)
    print('result length', len(result))
    if return_sql:
        return result, sql
    else:
        return result


def customize_sentence_clear(text: str):
    text = text.replace('无任何不良导向', '')
    text = text.replace('安全拍摄请勿模仿', '')
    text = text.replace('[捂脸]', '')
    text = text.replace('[赞]', '')
    text = text.replace('[呲牙]', '')
    return text
