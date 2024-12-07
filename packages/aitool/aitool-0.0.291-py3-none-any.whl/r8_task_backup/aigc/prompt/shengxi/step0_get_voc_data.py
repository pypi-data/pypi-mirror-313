# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
import pandas as pd
import bytedtqs
from pathlib import Path
import pickle
import re
from tqdm import tqdm

# 链接tcc
from bytedtcc import ClientV2

service_name = 'ies.efficiency.sensitive_words'
tcc_client = ClientV2(service_name, 'default')

# 连接lark机器人
from byted_tools.lark_sheet import LarkSDK

lark_client = LarkSDK()

# 连接tos tqs
from byted_tools.tos_util import TosClient

bucket = "ies-qa-turing-nlp"
access_key = "OI4GASTCN6IVPX267OEM"
tos_client = TosClient(bucket, access_key)

# 拉标签表
label_map_fp = Path('/tmp/label_map.pkl')
tos_client.pull_single('maydayfu/voc_label_map/label_map.pkl', label_map_fp)
label_map = pickle.load(open(label_map_fp, 'rb'))

from byted_tools.tqs_tool import TqsClient

app_id = "R74poAg5CaAetWHBxeH3Rbv261l1VbFWIVmbYJWT55b3CjAM"
app_key = "eIYvzsdjtqNsub3x39FKEf9WopLOWWfP6UKTJjnQSvNEUy69"
user_name = "maydayfu.996"
cluster = bytedtqs.Cluster.CN
tqs_client = TqsClient(app_id, app_key, cluster, user_name)

# 连接 voc es
from byted_tools.es_tool import ElasticSearchDao

VOC_PSM = 'byte.es.experience.service.lf'
VOC_INDEX = 'experience-manager-platform'
voc_adapter = ElasticSearchDao(psm=VOC_PSM)

now = datetime.now()
today = now.replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y%m%d')

# %%
import sys;

sys.stderr.flush()
start_dt = datetime.strptime('2023-10-31 08:00:00', '%Y-%m-%d %H:%M:%S')
end_dt = datetime.strptime('2023-10-31 12:00:00', '%Y-%m-%d %H:%M:%S')
start_ms = int(start_dt.timestamp() * 1000)
end_ms = int(end_dt.timestamp() * 1000)

# 查询数据
col_names = [
    'label_ids',
    'label_names',  # 标签名
    'feedback_channel',  # 渠道
    'feedback_id',  # id 会重复
    'eredar_create_timestamp_ms',  # 创建时间
    'content',  # 内容
    'content_full_stage',  # 包含智能阶段的会话数据
    'content_title',  # 摘要
    'sensitive_hit_count',
    'sensitive_hit_keywords',
    'sensitive_max_score',
    'sensitive_label',
    'notes',  # 研判结果、
    'TicketContext',
    'has_aibot',
    'is_transfer_agent'
    # 'customer_content',  # 用户发言
]

qb = {
    "_source": col_names,
    "query": {
        "bool": {
            "must_not": [
                {"term": {"visibility": 0}},
                {"term": {"is_reserve": "true"}},
            ],
            "must": [
                # "term": {"sensitive_label": 'possible'},
                # {"exists": {"field": "label_ids"}},
                # {"terms": {"feedback_channel": ["voip", "ticket_telephone"]}},
                # {"bool": {
                #     "should": [
                #         {"term": {"has_aibot": "true"}},
                #         {"term": {"is_transfer_agent": "false"}}
                #     ]
                # }}
            ],

            # {"terms": {"sensitive_label": ["not_possible_in_first_review"]}}
            # "exists": {"field": 'notes'},

            "filter":
                {
                    "range": {
                        "eredar_create_timestamp_ms": {
                            "gte": start_ms,
                            "lt": end_ms
                        }
                    },

                }
        }
    }
}

res_generator = voc_adapter.my_search_scroll(VOC_INDEX, qb)
all_data = []

tqdm_bar = tqdm(desc='获取数据')
for i in res_generator:
    all_data.append(i['_source'])
    tqdm_bar.update(1)
    # if len(all_data)>=1000:
    #     break
tqdm_bar.close()
df_data = pd.DataFrame(all_data)

print(set(df_data['sensitive_label']))

# 标签映射，标注敏感数据的voc标签业务线
df_map = label_map['df_map']


def get_voc_name(qids):
    if not isinstance(qids, list):
        return None
    try:
        df_tmp = df_map[df_map['feedback_label_id'].isin(qids)].sort_values(by='exp_label_name_path')
        if len(df_tmp) == 0:
            return None
        return df_tmp.iloc[-1]['exp_label_name_path']

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(qids)
        assert 1 == 2


df_data['voc_name'] = [get_voc_name(qids) for qids in tqdm(df_data['label_ids'].values, desc='标签映射')]

# 研判结果打上标签
df = df_data.copy()

# %%

df_choose = df.copy()
mask_see = df_choose.voc_name.map(lambda x: bool(re.search('抖音主端|抖音极速版|新火山', str(x))))
mask_nosee = df_choose.voc_name.map(
    lambda x: bool(re.search('综搜问卷反馈（无原声）|抖音主端$|抖音主端->安全风控|抖音主端->抖音开放平台', str(x))))
# ts_ = datetime.strptime('2023-08-13 09:00:00', '%Y-%m-%d %H:%M:%S').timestamp()*1000
# te_ = datetime.strptime('2023-08-13 21:00:00', '%Y-%m-%d %H:%M:%S').timestamp()*1000
# mask_time =  df_choose.eredar_create_timestamp_ms.map(lambda x:ts_<=x<te_)
df_choose = df[mask_see & ~mask_nosee].reset_index(drop=True).copy()
print(df_choose.shape)


def content_process_func(ser):
    '''
    @ description: 抽出需要检查的文本
    @ return {*}
    '''
    # try:
    content_raw = ser['content']
    if not isinstance(content_raw, str):
        return []
    content = content_raw.replace('"useImagex":true', '"useImagex":True').replace('"useImagex":false',
                                                                                  '"useImagex":False')
    if ser.feedback_channel in ['im']:
        obj = eval(content)
        res = []
        for i in obj:
            if i.get('content'):
                res.append(i['content'])
    elif ser.feedback_channel in ['voip', 'ticket_telephone']:
        content_raw = ser['content_full_stage']
        if not isinstance(content_raw, str):
            return []
        content = content_raw.replace('"useImagex":true', '"useImagex":True').replace('"useImagex":false',
                                                                                      '"useImagex":False')
        obj = eval(content)
        res = []
        for i in obj:
            if i.get('content_type') == 'ivr':
                if i.get('content'):
                    for j in i.get('content'):
                        if j.get('content'):
                            res.append(j.get('content'))
            elif i.get('content_type') == 'agent':
                if i.get('content'):
                    for j in i.get('content'):
                        if j.get('content'):
                            res.append(j.get('content'))
    else:
        res = [content_raw]
    # import ipdb
    # ipdb.set_trace()
    # for i in obj:
    #     if i.get('content_type') == 'ivr':
    #         if i.get('content'):
    #             for j in i.get('content'):
    #                 if j.get('content') and j['from'] == '客户':
    #                     res.append(j.get('content'))
    #     elif i.get('content_type') == 'agent':
    #         if i.get('content'):
    #             for j in i.get('content'):
    #                 if j.get('content'):
    #                     res.append(j.get('content'))
    # if ser.feedback_channel in ['voip','ticket_telephone']:
    # res.append(ser.content_title) # 电话渠道数据加入摘要
    # res.append(ser.TicketContext)

    # except:
    #     # import ipdb
    #     # ipdb.set_trace()
    #     res =  [content_raw]

    return res


text_li = [content_process_func(df_choose.iloc[i]) for i in tqdm(range(len(df_choose)), desc='原声处理')]

# %%
from byted_tools.lark_sheet import LarkSDK

# content_list = [json.loads(i.strip())["text"] for i in open("zhibo/content.txt").readlines()]
# content_list = [i.strip() for i in open("zhibo/feedback.txt").readlines()]
# df_content = pandas.DataFrame(content_list, columns=["text"])

lark_client = LarkSDK()
# 必测数据集
text_feishu_url = "https://bytedance.feishu.cn/sheets/ZduJs6ZpXh8IvNt1Gh3cFVv5ndc?sheet=gx3enS"
text_col = "正则内容"

# text_feishu_url = "https://bytedance.feishu.cn/sheets/AGwYsvusShiwDot5rqScbEunnmg"
# text_col = "text"

# text_feishu_url2 = "https://bytedance.feishu.cn/sheets/UH4TsnYF3h8CgLtC7WkccmlZnTh"

# 大模型构造
# text_feishu_url = "https://bytedance.feishu.cn/sheets/OOf6seTTjhGxWqtoIz6cjIgjnBc"
# text_col = "RESULT"

url = text_feishu_url
df_content = lark_client.read_excel(url, sheet="违规内容", header=0)
# df_content.set_axis(["text", "true_label", "notes"], axis=1, inplace=True)
regexes = df_content[[text_col]]


# %%
def regex_recall(text, pattern):
    pattern = re.compile(pattern)
    if re.search(pattern, text):
        return True
    # print(text)
    return False


# pattern = r"(([ABCDXYZabcdxyz].{,2}号)|(.{,2}号[ABCDXYZabcdxyz])).*(([ABCDXYZabcdxyz].{,2}号)|(.{,2}号[ABCDXYZabcdxyz]))"
# pattern = r"我发.{,15}(别人|对方)收到"
# pattern = r"刷赞"

# pattern = r"私密.*(可见|看到|看见|点赞|评论)"

# p1 = r"自动"
# p2 = r"取消"
# p3 = r"关注"
# p4 = r"您"
# p1 = r"(别人|对方|他|她)"
# p2 = r"我"
# p3 = r"发"
# p4 = r"(不一致|不一样)"
# p5 = r"发.*收到|看到|展示"
# p6 = r"另一个"
# p7 = r"看不"
p8 = r"^.{,100}$"
p9 = r"您|先生|女士|咱|小助手"
p10 = r"买过.*提醒"
# p1 and p2 and p3 and (p4 or p5 or p6) and not p7 and p8
# result = []
# count = 0
new_text_li = [["我发的是照片，对方收到的是熊"],
               ["上面是对方截图，下面是我的，我发的是照片，对方收到的是熊，46394864724，凌晨一点十八"],
               ["我给我朋友发照片，他展示的图片跟我给他发的不一样"],
               ["为啥给别人发送的消息，他收到的和我发的不一样啊"]
               ]
# text_li += new_text_li
regexes['count'] = 0
regexes['result'] = 0

for i, row in regexes.iterrows():
    if i > 3:
        break
    result = []
    # pattern = row['正则内容']
    # pattern = "(色情|黄色|漏点|裸体|擦边).*(特效)"
    pattern = r"买过.*提醒"
    count = 0
    if pattern:
        for texts in tqdm(text_li):
            if len(texts) == 0:
                continue
            res = []
            for text in texts:
                # if regex_recall(text, p1) and regex_recall(text, p2) and regex_recall(text, p3) and (regex_recall(text, p4) or regex_recall(text, p5) or regex_recall(text, p6)) and not regex_recall(text, p7) and regex_recall(text, p8):
                # if regex_recall(text, pattern) and regex_recall(text, p8) and not regex_recall(text, p9):
                if regex_recall(text, p10):
                    # if regex_recall(text, p1) and regex_recall(text, p2) and regex_recall(text, p3) and not regex_recall(text, p4):
                    res.append(text)
            count += len(res)
            if len(res) != 0:
                result.append(res)
    regexes.loc[i, 'count'] = count
    regexes.loc[i, 'result'] = str(result)

    print("=======", count)

print(regexes)

# %%
