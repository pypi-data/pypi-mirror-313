"""
更新代码注意要修改输出文件名：10.x-蓝军_one_sql_xxx
"""
from functools import wraps, partial
from pyspark.sql.types import StructType, StructField, StringType, LongType, ArrayType, DoubleType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql import Row
from base_utils.cluster_robot import alert_message_use_df
from base_utils.duplicate_util import HashDup
from pandas import Series
import csv
import get_attr
import weapon_marketing_nlp_model
import weapon_marketing_model_v2
import weapon_marketing_detector
import numpy as np
import pandas as pd
import time
import sys
from pyspark import SparkConf, SparkContext

# import subprocess

# 定义命令和参数
# command = ["zip", "-r", "utils.zip", "/opt/tiger/suicide_comment_decision/src/util/"]

# 执行命令


# spark = SparkSession.builder.config(conf=spark_conf).enableHiveSupport().getOrCreate()
spark = SparkSession.builder.enableHiveSupport().getOrCreate()

sc = spark.sparkContext
imported = False
rs_client = None
try:
    sys.path.append("/opt/tiger/suicide_comment_decision")
    from src.util.redshied_util import rs_client

    imported = True
except Exception as e:
    print("from src.util.redshied_util import rs_client ")
    try:
        import rs_client

        imported = True
    except Exception as e2:
        print("import rs_client failed")
        print(e2)
    print(e)

if not imported:
    import sys
    import importlib

    try:
        # 指定模块文件的绝对路径
        module_path = '/opt/tiger/suicide_comment_decision/src/util/redshied_util.py'

        # 获取模块的名称，通常是文件名去掉.py后缀
        module_name = 'rs_client'

        # 创建一个模块规范
        spec = importlib.util.spec_from_file_location(module_name, module_path)

        # 创建一个新的模块对象
        module = importlib.util.module_from_spec(spec)

        # 将创建的模块添加到sys.modules中，这样在其他地方就可以正常import了
        sys.modules[module_name] = module

        # 执行模块的代码
        spec.loader.exec_module(module)
        # 现在你可以像使用其他模块一样使用这个模块了

        rs_client = module.rs_client
    except Exception as e:
        print(e)

# 注释掉，故意搞失败，测试任务告警监控
import traceback
from base_utils.feishu_util import create_excel_send_alert_msg

sys.path.append("/opt/tiger/algorithm_suicide_decision")
detector = weapon_marketing_detector.WeaponMarketingDetector()

csv.field_size_limit(sys.maxsize)

# broadcast_model = True
# if broadcast_model:
#     sc.addPyFile("porn_words.txt")
#     sc.addPyFile("contact_words.txt")


# sc.addPyFile("/opt/tiger/algorithm_suicide_decision/recall.py")

retries = 3


def retry(func=None, retries=3, sleep=0.1):
    if func is None:
        return partial(retry, retries=retries)

    @wraps(func)
    def wrapper(*args, **kwargs):
        i = 0
        while i < retries:
            i += 1
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("try number: {}".format(i))
                time.sleep(sleep * i)
                if i >= retries:
                    raise e

    return wrapper


def generate_business_time():
    # 这段代码只能在Dorado上运行，本地运行会报错
    # 假设 20220212 15:03执行，date=20220212, hour=11, timestamp=1644642000    ${hour}是业务日期，是当前时间的前一个小时
    global date, hour, date_1h_ago, hour_1h_ago, timestamp, start_time, ts_1h_ago, date_1d_ago, date_2d_ago
    start_time = time.time()  # 这个时间用来计算任务耗时
    # 这样取时间不准，20220217 0点取值 date会是17 hour是0
    # date = '${date}'
    # hour = '${hour-1}'
    timestamp = int('${timestamp}')  # 取当前时间戳往前推1h
    ts_1h_ago = int('${timestamp}') - 3600  # 取当前时间戳往前推2h
    date, hour = get_date_hour(timestamp)
    date_1h_ago, hour_1h_ago = get_date_hour(ts_1h_ago)
    date_1d_ago, _ = get_date_hour(int('${timestamp}') - 3600 * 24)
    date_2d_ago, _ = get_date_hour(int('${timestamp}') - 3600 * 24 * 2)

    print("打印业务时间 date, hour, date_1h_ago, hour_1h_ago, timestamp",
          date, hour, date_1h_ago, hour_1h_ago, timestamp)
    pass


def get_date_hour(timestamp):
    time_local = time.localtime(timestamp)
    # 1645023600 2022-02-16 23:00:00
    dt = time.strftime("%Y%m%d_%H", time_local)
    date = dt.split('_')[0]
    hour = dt.split('_')[1]
    return date, hour


def get_time(start_time):
    ts = time.time()
    return (ts - start_time) / 3600


def get_all_data_by_one_sql():
    one_sql_2 = """
with item as (
    select 
    cast(item_id as string) as item_id,
        collect_set(author_user_id)[0] as author_user_id,
        collect_set(item_title)[0] as item_title,
        collect_set(status)[0] as item_status,
        collect_set(item_media_type)[0] as item_media_type, 
        collect_set(item_is_reviewed)[0] as item_is_reviewed, 
        collect_set(item_create_time_str)[0] as item_create_time_str,
        collect_set(ocr)[0] as ocr_text,
        collect_set(asr1)[0] as asr1_text,
        collect_set(asr2)[0] as asr2_text,
        collect_set(date)[0] as date,
        '' as nickname
    from
        ies_lanjun_cn.dwd_safe_item_change_h_di

    where
        date = '{}' and hour = '{}'
        and app_id in ('1128', '2329') -- 1128-抖音 2329-抖音极速版
        and status in ('102', '143')
        and item_create_time >= {} --hour 的时间戳，10位数，以秒为单位
    group by item_id
),

user_t as (
    select
        collect_set(user_id)[0] as user_id,
        collect_set(punish_detail)[0] as punish_detail,
        collect_set(signature)[0] as signature,
        collect_set(avatar_uri)[0] as avatar_uri,
        collect_set(cover_uri)[0] as cover_uri,
        collect_set(device_id_array)[0] as device_id_array, 
        collect_set(device_cnt)[0] as device_cnt, 
        collect_set(province)[0] as province,
        collect_set(city)[0] as city,
        collect_set(city_label)[0] as city_label,
        collect_set(district)[0] as district,
        collect_set(im_msg_cnt_7d)[0] as im_msg_cnt_7d,
        collect_set(im_user_cnt_7d)[0] as im_user_cnt_7d,
        collect_set(im_user_no_relation_cnt_7d)[0] as im_user_no_relation_cnt_7d
    from
        ies_lanjun_cn.blue_army_gun_user
    where
        date = '{}'
    group by user_id
),

total as (
    select 
        item_id,
        author_user_id,
        nickname,
        user_t.signature,
        item_title,
        item_status,
        item_media_type,
        item_is_reviewed,
        item_create_time_str, 
        ocr_text,
        asr1_text, 
        asr2_text, 
        user_t.avatar_uri,
        user_t.cover_uri,
        user_t.device_id_array,
        user_t.device_cnt,
        user_t.im_msg_cnt_7d,
        user_t.im_user_cnt_7d,
        user_t.im_user_no_relation_cnt_7d,
        date
    from item left join user_t
        on item.author_user_id = user_t.user_id
)


select
* 
from total limit 6000;
    """

    global count
    one_sql_2 = one_sql_2.format(
        date, hour_1h_ago, str(ts_1h_ago), str(date_2d_ago))
    print("one_sql_2 ")
    print(one_sql_2)
    df_all = spark.sql(one_sql_2)
    count = df_all.count()
    # print('#!# df_all count:  ',count)

    return df_all


def get_rdd_extra_schema():
    rdd_schema = StructType([
        StructField("item_id", StringType(), True),
        StructField("author_user_id", StringType(), True),
        StructField("nickname", StringType(), True),
        StructField("signature", StringType(), True),
        StructField("item_title", StringType(), True),
        StructField("item_status", StringType(), True),
        StructField("item_media_type", StringType(), True),
        StructField("item_is_reviewed", StringType(), True),
        StructField("item_create_time_str", StringType(), True),
        StructField("ocr_text", StringType(), True),
        StructField("asr1_text", StringType(), True),
        StructField("asr2_text", StringType(), True),
        StructField("avatar_uri", StringType(), True),
        StructField("cover_uri", StringType(), True),
        StructField("device_id_array", ArrayType(LongType(), True), True),
        StructField("device_cnt", LongType(), True),
        StructField("im_msg_cnt_7d", LongType(), True),
        StructField("im_user_cnt_7d", LongType(), True),
        StructField("im_user_no_relation_cnt_7d", LongType(), True),
        StructField("date", StringType(), True),
        StructField("tag_name", StringType(), True),
        StructField("hit_model_names", ArrayType(StringType(), True), True),
        StructField("hit_table_ids", ArrayType(LongType(), True), True)
    ])
    return rdd_schema


def get_extra_info(df_all):
    rdd_info = df_all.rdd.mapPartitions(lambda rows: get_extra_info_rows(rows))

    print("df_info schema[指定之前]: ")
    try:
        df_ori = spark.createDataFrame(rdd_info)
        df_ori.printSchema()
    except:
        print("df_info schema打印失败，捕获抛出的异常: ")
        traceback.print_exc()

    # 首先通过指定schema来生成df，如果抛出异常，自动由spark自动推断生成df
    try:
        rdd_info_schema = get_rdd_extra_schema()
        df_info = spark.createDataFrame(rdd_info, schema=rdd_info_schema)
        # df_info = df_info.toPandas()
    except:
        print("df_info指定schema失败，捕获抛出的异常：")
        traceback.print_exc()
        # 如果还失败，中断程序
        df_info = spark.createDataFrame(rdd_info)
        print("df_info schema: ")
        df_info.printSchema()
        # df_info = df_info.toPandas()

    return df_info


def get_extra_info_rows(rows):
    new_rows = []
    for row in rows:
        row_dict = row.asDict()
        is_recall, tag_row_dict = get_attr.get_attr_value(row_dict)
        new_rows.append(Row(**tag_row_dict))
    return new_rows
    pass


def get_rdd_recall_schema():
    rdd_risk_schema = StructType([
        StructField("item_id", StringType(), True),
        StructField("author_user_id", StringType(), True),
        StructField("nickname", StringType(), True),
        StructField("signature", StringType(), True),
        StructField("item_title", StringType(), True),
        StructField("item_status", StringType(), True),
        StructField("item_media_type", StringType(), True),
        StructField("item_is_reviewed", StringType(), True),
        StructField("item_create_time_str", StringType(), True),
        StructField("ocr_text", StringType(), True),
        StructField("asr1_text", StringType(), True),
        StructField("asr2_text", StringType(), True),
        StructField("avatar_uri", StringType(), True),
        StructField("cover_uri", StringType(), True),
        StructField("device_id_array", ArrayType(LongType(), True), True),
        StructField("device_cnt", LongType(), True),
        StructField("im_msg_cnt_7d", LongType(), True),
        StructField("im_user_cnt_7d", LongType(), True),
        StructField("im_user_no_relation_cnt_7d", LongType(), True),
        StructField("date", StringType(), True),
        StructField("tag_name", StringType(), True),
        StructField("hit_model_names", ArrayType(StringType(), True), True),
        StructField("hit_table_ids", ArrayType(LongType(), True), True),
        StructField("title_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("ocr_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("asr1_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("asr2_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("nickname_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("signature_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("title_tag", ArrayType(StringType(), True), True),
        StructField("ocr_tag", ArrayType(StringType(), True), True),
        StructField("asr1_tag", ArrayType(StringType(), True), True),
        StructField("asr2_tag", ArrayType(StringType(), True), True),
        StructField("nickname_tag", ArrayType(StringType(), True), True),
        StructField("signature_tag", ArrayType(StringType(), True), True),
        StructField("is_weapon", IntegerType(), True),
        StructField("is_contact", IntegerType(), True),
        StructField("is_contact_num", IntegerType(), True),
        StructField("total_matched_word_len", IntegerType(), True),
        StructField("total_matched_len", IntegerType(), True),
    ])
    return rdd_risk_schema


def get_recall_result(df_info):
    rdd_recall = df_info.rdd.mapPartitions(
        lambda rows: get_recall_result_rows(rows))

    # print("df_recall schema[指定之前]: ")
    # try:
    #     df_ori = spark.createDataFrame(rdd_recall)
    #     df_ori.printSchema()
    # except:
    #     print("df_recall schema打印失败，捕获抛出的异常: ")
    #     traceback.print_exc()

    # 首先通过指定schema来生成df，如果抛出异常，自动由spark自动推断生成df
    try:
        rdd_recall_schema = get_rdd_recall_schema()
        df_recall = spark.createDataFrame(rdd_recall, schema=rdd_recall_schema)
        # df_recall = df_recall.toPandas()
    except Exception as e:
        print(e)
        print("df_recall指定schema失败，捕获抛出的异常: ")
        traceback.print_exc()
        # 如果还失败，中断程序
        df_recall = spark.createDataFrame(rdd_recall)
        print("df_recall schema: ")
        df_recall.printSchema()
        # df_recall = df_recall.toPandas()
    print("df_recall done")
    return df_recall


def get_recall_result_rows(rows):
    new_rows = []
    for row in rows:
        row_dict = row.asDict()
        is_recall, nlp_row_dict = detector.do_nlp_recall(row_dict)
        if is_recall:
            new_rows.append(Row(**nlp_row_dict))
    return new_rows
    pass


def get_rdd_model_schema():
    rdd_risk_schema = StructType([
        StructField("item_id", StringType(), True),
        StructField("author_user_id", StringType(), True),
        StructField("nickname", StringType(), True),
        StructField("signature", StringType(), True),
        StructField("item_title", StringType(), True),
        StructField("item_status", StringType(), True),
        StructField("item_media_type", StringType(), True),
        StructField("item_is_reviewed", StringType(), True),
        StructField("item_create_time_str", StringType(), True),
        StructField("ocr_text", StringType(), True),
        StructField("asr1_text", StringType(), True),
        StructField("asr2_text", StringType(), True),
        StructField("avatar_uri", StringType(), True),
        StructField("cover_uri", StringType(), True),
        StructField("device_id_array", ArrayType(LongType(), True), True),
        StructField("device_cnt", LongType(), True),
        StructField("im_msg_cnt_7d", LongType(), True),
        StructField("im_user_cnt_7d", LongType(), True),
        StructField("im_user_no_relation_cnt_7d", LongType(), True),
        StructField("date", StringType(), True),
        StructField("tag_name", StringType(), True),
        StructField("hit_model_names", ArrayType(StringType(), True), True),
        StructField("hit_table_ids", ArrayType(LongType(), True), True),
        StructField("title_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("ocr_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("asr1_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("asr2_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("nickname_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("signature_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("title_tag", ArrayType(StringType(), True), True),
        StructField("ocr_tag", ArrayType(StringType(), True), True),
        StructField("asr1_tag", ArrayType(StringType(), True), True),
        StructField("asr2_tag", ArrayType(StringType(), True), True),
        StructField("nickname_tag", ArrayType(StringType(), True), True),
        StructField("signature_tag", ArrayType(StringType(), True), True),
        StructField("is_weapon", IntegerType(), True),
        StructField("is_contact", IntegerType(), True),
        StructField("is_contact_num", IntegerType(), True),
        StructField("total_matched_word_len", IntegerType(), True),
        StructField("total_matched_len", IntegerType(), True),
        StructField("background_weapon_score", DoubleType(), True),
        StructField("avatar_weapon_score", DoubleType(), True),
        StructField("video_weapon_score", DoubleType(), True)
    ])
    return rdd_risk_schema


def get_model_result(df_recall):
    rdd_model = df_recall.rdd.mapPartitions(
        lambda rows: get_model_result_rows(rows))

    print("df_recall schema[指定之前]: ")
    # try:
    #     df_ori = spark.createDataFrame(rdd_model)
    #     df_ori.printSchema()
    # except:
    #     print("df_recall schema打印失败，捕获抛出的异常: ")
    #     traceback.print_exc()

    # 首先通过指定schema来生成df，如果抛出异常，自动由spark自动推断生成df
    try:
        rdd_model_schema = get_rdd_model_schema()
        print("rdd_model.head()")
        print(rdd_model.top(3))
        print("rdd_model_schema ")

        print(rdd_model_schema)
        df_model = spark.createDataFrame(rdd_model, schema=rdd_model_schema)
        # df_recall = df_recall.toPandas()
    except Exception as e:
        print(e)
        print("df_recall指定schema失败，捕获抛出的异常: ")
        traceback.print_exc()
        # 如果还失败，中断程序
        df_model = spark.createDataFrame(rdd_model)
        print("df_recall schema: ")
        df_model.printSchema()
        # df_recall = df_recall.toPandas()
    print("df_model return done")
    return df_model


def get_model_result_rows(rows):
    new_rows = []
    for row in rows:
        row_dict = row.asDict()
        cv_row_dict = weapon_marketing_model_v2.do_cv_model(row_dict)
        new_rows.append(Row(**cv_row_dict))
    return new_rows
    pass


def get_rdd_nlp_model_schema():
    rdd_risk_schema = StructType([
        StructField("item_id", StringType(), True),
        StructField("author_user_id", StringType(), True),
        StructField("nickname", StringType(), True),
        StructField("signature", StringType(), True),
        StructField("item_title", StringType(), True),
        StructField("item_status", StringType(), True),
        StructField("item_media_type", StringType(), True),
        StructField("item_is_reviewed", StringType(), True),
        StructField("item_create_time_str", StringType(), True),
        StructField("ocr_text", StringType(), True),
        StructField("asr1_text", StringType(), True),
        StructField("asr2_text", StringType(), True),
        StructField("avatar_uri", StringType(), True),
        StructField("cover_uri", StringType(), True),
        StructField("device_id_array", ArrayType(LongType(), True), True),
        StructField("device_cnt", LongType(), True),
        StructField("im_msg_cnt_7d", LongType(), True),
        StructField("im_user_cnt_7d", LongType(), True),
        StructField("im_user_no_relation_cnt_7d", LongType(), True),
        StructField("date", StringType(), True),
        StructField("tag_name", StringType(), True),
        StructField("hit_model_names", ArrayType(StringType(), True), True),
        StructField("hit_table_ids", ArrayType(LongType(), True), True),
        StructField("title_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("ocr_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("asr1_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("asr2_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("nickname_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("signature_matched_words", ArrayType(
            ArrayType(StringType(), True), True), True),
        StructField("title_tag", ArrayType(StringType(), True), True),
        StructField("ocr_tag", ArrayType(StringType(), True), True),
        StructField("asr1_tag", ArrayType(StringType(), True), True),
        StructField("asr2_tag", ArrayType(StringType(), True), True),
        StructField("nickname_tag", ArrayType(StringType(), True), True),
        StructField("signature_tag", ArrayType(StringType(), True), True),
        StructField("is_weapon", IntegerType(), True),
        StructField("is_contact", IntegerType(), True),
        StructField("is_contact_num", IntegerType(), True),
        StructField("total_matched_word_len", IntegerType(), True),
        StructField("total_matched_len", IntegerType(), True),
        StructField("background_weapon_score", DoubleType(), True),
        StructField("avatar_weapon_score", DoubleType(), True),
        StructField("video_weapon_score", DoubleType(), True),
        StructField("weapon_nlp_score", DoubleType(), True)

    ])
    return rdd_risk_schema


def get_nlp_model_result(df_recall):
    rdd_model = df_recall.rdd.mapPartitions(
        lambda rows: get_nlp_model_result_rows(rows))

    print("df_recall schema[指定之前]: ")
    try:
        df_ori = spark.createDataFrame(rdd_model)
        df_ori.printSchema()
    except:
        print("df_recall schema打印失败，捕获抛出的异常: ")
        traceback.print_exc()

    # 首先通过指定schema来生成df，如果抛出异常，自动由spark自动推断生成df
    try:
        rdd_model_schema = get_rdd_nlp_model_schema()
        df_model = spark.createDataFrame(rdd_model, schema=rdd_model_schema)
        # df_recall = df_recall.toPandas()
    except:
        print("df_recall指定schema失败，捕获抛出的异常: ")
        traceback.print_exc()
        # 如果还失败，中断程序
        df_model = spark.createDataFrame(rdd_model)
        print("df_recall schema: ")
        df_model.printSchema()
        # df_recall = df_recall.toPandas()

    return df_model


def get_nlp_model_result_rows(rows):
    new_rows = []
    for row in rows:
        row_dict = row.asDict()
        nlp_row_dict = weapon_marketing_nlp_model.do_nlp_model(row_dict)
        new_rows.append(Row(**nlp_row_dict))
    return new_rows
    pass


def get_final_result(df_final):
    print("生成pandas:")
    final_result = df_final.toPandas()

    final_result["item_id"] = final_result["item_id"].astype(np.str)

    final_result = final_result.fillna(value="/")

    # final_result = final_result[final_result["is_contact_num"] == 1]
    # final_result = final_result[(final_result["tag_name"].str.len() == 0)|(final_result["tag_name"].str.contains("随拍|猎奇好物|武器装备|玩具"))]
    # final_result = final_result[(final_result["nickname_tag"].str.contains("联系方式"))|(final_result["signature_tag"].str.contains("联系方式"))]
    final_result = final_result[~final_result["ocr_text"].str.contains(
        "烟花|爆竹|炮仗|鞭炮|礼花|春节|浏阳市|防身|仙女棒|年味|过年")]
    final_result = final_result[~final_result["item_title"].str.contains(
        "烟花|爆竹|炮仗|鞭炮|礼花|春节|浏阳市|防身|仙女棒|年味|过年")]
    final_result = final_result[~final_result["tag_name"].str.contains(
        "游戏|新闻")]
    final_result = final_result[
        (final_result["tag_name"].str.contains("猎奇好物|武器装备|玩具")) | (final_result["hit_table_ids"].str.len(
        ) > 0) | (final_result["is_weapon"] == 1) | (final_result["hit_model_names"].str.contains("weapon"))]
    final_result["nickname_risk"] = np.where(
        final_result["nickname"].str.contains("户外|兔|鹰|pcp|模型|模具|玩具|PCP|Pcp"), 1, 0)

    final_result["background_weapon_risk"] = np.where(
        final_result["background_weapon_score"] >= 0.8, 1, 0)
    final_result["avatar_weapon_risk"] = np.where(
        final_result["avatar_weapon_score"] >= 0.8, 1, 0)
    final_result["weapon_nlp_risk"] = np.where(
        final_result["weapon_nlp_score"] >= 0.8, 1, 0)
    final_result["video_weapon_risk"] = np.where(
        final_result["video_weapon_score"] >= 0.6, 1, 0)

    final_result["decision_score"] = final_result["total_matched_len"] \
                                     + final_result["nickname_risk"] * 100 \
                                     + final_result["background_weapon_risk"] * 20 \
                                     + final_result["avatar_weapon_risk"] * 20 \
                                     + final_result["weapon_nlp_risk"] * 20 \
                                     + final_result["video_weapon_risk"] * 20
    final_result["decision_result"] = np.where(
        final_result["decision_score"] >= 100, True, False)

    # final_result = final_result.apply(make_decision, axis=1)  # 联合决策新方法

    # final_result["score"] = final_result.apply(lambda x: get_score(x), axis=1)  # 计算排序得分
    # 根据新决策分数降序排序

    final_result.sort_values(by=["decision_score"], ascending=[
        False], inplace=True)

    # #取top200
    # final_result = final_result.head(200)

    final_result_filtered = final_result[[
        "item_id",
        "author_user_id",
        "decision_result",
        "decision_score",
        "weapon_nlp_score",
        "cover_uri",
        "background_weapon_score",
        "avatar_uri",
        "avatar_weapon_score",
        "video_weapon_score",
        "item_is_reviewed",
        "nickname",
        "nickname_risk",
        "signature",
        "title_matched_words",
        "ocr_matched_words",
        "is_weapon",
        "is_contact",
        "is_contact_num",
        "hit_model_names",
        "hit_table_ids",
        "tag_name",
    ]]

    # final_result =  final_result.head(1910)
    # 返回两个final_result, 第一个是原始的，第二个是经过字段过滤的。
    return final_result, final_result_filtered


def duplicate(final_result):
    global dup
    print("联合决策后去重")
    print("final_result.shape : 去重前" + str(final_result.shape))
    print("final_result.shape : 去重前 计算时间 : {}".format(get_time(start_time)))
    dup = HashDup()
    final_result = final_result.apply(check_dup, axis=1)  # 打上去重标签
    final_result = final_result[final_result['dup'] == 0]  # 去重
    print("final_result.shape : 去重后" + str(final_result.shape))
    print("final_result.shape : 去重后 计算时间 : {}".format(get_time(start_time)))
    return final_result


# 去重
def check_dup(row):
    dict = row.to_dict()
    if dict['decision_result']:
        mark = dup.check_dup_insert(dict)  # mark 0-表示历史无重复 , mark 1-表示历史有重复
    else:
        mark = 0
    dict['dup'] = mark
    return Series(dict)


def get_excel_name():
    return "枪爆导流-词_{}_{}".format(date, hour)


def get_message(final_result):
    return "{}/{} 枪爆导流- NLP CV 模型,召回条数: {}, 风险条数: {}, ".format(date, hour, str(count),
                                                                             str(final_result.shape[0]))


def make_decision(row):
    dict = row.to_dict()
    res = recall.get_decision_result_score(dict)
    new_row = Series(res)
    return new_row
    pass


def send_alert_msg(final_result):
    # LARK_GROUP_ID = "7101233672254275587"  # 蓝军红线导流视频监控群
    LARK_GROUP_ID = "7296702892593004572"  # 枪暴风险挖掘 20231102

    # chat_id是一个群聊的唯一标识。当创建一个群聊的时候，系统会自动生成该ID。
    CHAT_ID = "oc_4ee52beb531b4b47671361fbe442f779"
    # LARK_TEST_GROUP_ID = "7101233672254275587"  # 蓝军告警测试群
    LARK_TEST_GROUP_ID = "7296702892593004572"  # 蓝军告警测试群
    # 枪暴风险挖掘 20231102
    # FOLDER_TOKEN = "fldcn3IROX1Tc1OccuWYRkjM3Xf"  # 抖音举报报警
    FOLDER_TOKEN = "ZCiJfuGPxlJuhtdRZSyckesEnwd"  # 我的目录fang_foler
    # https://bytedance.feishu.cn/drive/folder/ZCiJfuGPxlJuhtdRZSyckesEnwd

    # final_result["ocr_text"] = final_result["ocr_text"].apply(lambda x: x[:50])
    # final_result["asr1_text"] = final_result["asr1_text"].apply(lambda x: x[:100])
    # final_result["asr2_text"] = final_result["asr2_text"].apply(lambda x: x[:100])
    # final_result["item_title"] = final_result["item_title"].apply(lambda x: x[:50])
    # final_result["nickname"] = final_result["nickname"].apply(lambda x: x[:100])
    # final_result["signature"] = final_result["signature"].apply(lambda x: x[:100])

    total_cnt = final_result.shape[0]
    display_cnt = 5000
    # risk_cnt = final_result[final_result["decision_result"]].shape[0]

    print("开始 发送告警:")
    df_dict = {"weapon_marketing_{}_{}点".format(
        date, hour): final_result.head(display_cnt)}
    alert_message_use_df(
        "{}/{}点/ 枪爆导流 - NLP CV 模型,召回条数: {}, 召回条数: {}, 展示条数: {}, 风险条数: {}".format(
            date, hour, count, total_cnt, display_cnt, total_cnt),
        df_dict,
        most_num=1,
        group_id=LARK_GROUP_ID,
        # chat_id=CHAT_ID,
        fold_token=FOLDER_TOKEN)
    print("完成 发送告警 计算时间 : {}".format(get_time(start_time)))


def dump_to_hive(df_all, final_result):
    set_sql = '''
    set hive.exec.dynamic.partition.mode=nonstrict;
    set hive.exec.dynamic.partition=true;
    '''
    spark.sql(set_sql)

    # # dump sql取数结果 to hive
    # # 对于Hive分区表的写入，insertInto要待参数覆盖为True，这样每次会覆盖分区。注意不要使用saveAsTable！，会将全表覆盖，
    # after_sql_hive_tab = 'db_skynet.porn_marketing_result'
    # print('打印 df_all - dump to after_sql hive schema信息')
    # df_all.printSchema()
    # df_all.write.format("hive").insertInto(after_sql_hive_tab, True)
    # print("完成 dump sql取数结果 to hive 计算时间 : {}".format(get_time(start_time)))

    # dump 最终结果写 to hive
    final_result_hive_tab = 'db_skynet.porn_marketing_result'
    # final_result.drop('keyword', axis=1, inplace=True)  # pandas 的 df 删除某列
    # final_result.drop('river_score', axis=1, inplace=True)
    # final_result.drop('gas_score', axis=1, inplace=True)
    # final_result.drop('get_rule_str', axis=1, inplace=True)
    # final_result.drop('tag_name', axis=1, inplace=True)
    # final_result.info()
    spark_df = spark.createDataFrame(final_result)
    print('打印 spark_df - dump to final_result hive schema信息')
    spark_df.printSchema()
    spark_df.write.format("hive").insertInto(final_result_hive_tab, True)
    print("完成 dump 最终结果 to hive 计算时间 : {}".format(get_time(start_time)))


def main():
    # 正常任务

    generate_business_time()  # 生成业务时间

    df_all = get_all_data_by_one_sql()  # spark sql 取数
    print("get_all_data_by_one_sql(df_info) ")
    df_info = get_extra_info(df_all)  # 获取attr信息
    print("get_extra_info(df_info) ")

    df_recall = get_recall_result(df_info)  # 召回
    print("get_recall_result df_info  ")

    # df_nlp_model = get_model_result(df_recall)  # 重置并发度，模型

    df_model = get_model_result(df_recall)  # 重置并发度，模型

    df_model = get_nlp_model_result(df_model)  # 重置并发度，模型
    print("df_model.head(50)")

    print(df_model.head(50))

    final_result, final_result_filtered = get_final_result(
        df_model)  # 生成pandas
    print(final_result_filtered.head(10))
    # send_alert_msg(final_result_filtered)  # 发送告警
    create_excel_send_alert_msg(final_result_filtered, "7296702892593004572", "ZCiJfuGPxlJuhtdRZSyckesEnwd",
                                get_excel_name(),
                                get_message(final_result))
    limit = 30
    sent_count = 0

    try:
        uid_set = set()
        for idx, row in final_result_filtered.iterrows():
            # uid = 3210221143468382
            print("row:")
            print(row)
            uid = row.get('author_user_id', '')

            if uid in uid_set:
                continue
            else:
                uid_set.add(uid)

            if len(str(uid)) < 3:
                continue
            ocr_matched_words_str = row.get('ocr_matched_words', '')
            object_dict = {'title': '枪-智能服务',
                           'uid': str(uid), "reason": '{}#枪v040515'.format(ocr_matched_words_str)}

            # 推送队列
            # 7341467406390395392 枪

            task_id = rs_client.push_tcs_risk_comment(project_id='7341467406390395392', object_id=str(uid),
                                                      object_dict=object_dict)

            print(task_id)
            print(object_dict)

            sent_count += 1
            if sent_count > limit:
                break

    except Exception as e:
        print(e)

    print("sent_count {}".format(sent_count))

    try:
        import bytedtos
        import os
        bucket_name = "ies-turing-pornmarketing"
        access_key = "VSHS8IU4P9O1Q45F056W"

        file_name = '{}_{}.csv'.format(date, hour)

        print(file_name)
        obj_key = 'life_safety/qiang_risk/{}'.format(file_name)
        final_result_filtered.to_csv(file_name)

        total_size = os.path.getsize(file_name)
        print(total_size)
        client = bytedtos.Client(bucket_name, access_key)

        # res = client.put(obj_key, open(file_name, 'rb'))
        # print(res)
        client.put_object(obj_key, open(file_name, 'rb'))
        print("put_object success")
        ret = client.head_object(obj_key)
        print('tos head_object 返回值')
        print(ret)
    except Exception as e:
        print(e)

    # dump_to_hive(df_all, final_result)  # 写入hive
    # print("完成 计算时间 : {}".format(get_time(start_time)))

    # dump_to_hive(df_all, final_result):


def a():
    global send_landun_num
    send_landun_num = 1
    pass


def test_main():
    # a()
    global send_landun_num
    send_landun_num = 1
    send_to_landun_platform(None, test=True)
    # test_set_schema()
    # test_make_141_False()
    pass


def test_make_141_False():
    dict1 = {}
    dict1['decision_result'] = True
    dict1['item_status'] = 140
    decision_result = dict1['decision_result']
    item_status = dict1['item_status']
    if item_status == 141:
        decision_result = False
    dict1['decision_result'] = decision_result
    print(dict1)


if __name__ == "__main__":
    # test_main()

    main()

    sc.stop()