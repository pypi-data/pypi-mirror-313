# -*- coding: UTF-8 -*-
import euler    # pip install bytedeuler==0.35.2
from euler import base_compat_middleware
import idls.base_thrift as base
from idls.sensitive_feedback_detection_thrift import NLPService
import idls.sensitive_feedback_detection_thrift as NLPService_thrift
import pandas as pd

psm = "sd://ies.efficiency.sensitive_feedback_detection?idc=yg&cluster=default"
client = euler.Client(NLPService, psm, timeout=10)

# 测试
# text1 = NLPService_thrift.InferenceData(text="为什么我没有做任何操作，抖音就突然从我的手机上退出了？这让我感到非常困惑。")
# text2 = NLPService_thrift.InferenceData(text="我刚删除了一个视频，但还是不断收到它的评论和私信，这让我感到很困惑。为什么抖音没有按照我的意愿来保护我的隐私？")
# inference_request = NLPService_thrift.InferenceRequest(data_list = [text1,text2])
# inference_response = client.sensitive_feedback(inference_request)
# print(inference_response.result_list)

from aitool import load_excel, dump_excel
from tqdm import tqdm
from time import sleep
data = load_excel('rst_shengxi_1115.xlsx', to_list=True)
rst = []
for line in tqdm(data):
    text = line[7]
    text1 = NLPService_thrift.InferenceData(text=text)
    inference_request = NLPService_thrift.InferenceRequest(data_list=[text1])
    try:
        inference_response = client.sensitive_feedback(inference_request)
    except Exception as e:
        sleep(3)
        continue
    rsl = inference_response.result_list
    print(rsl)
    lable = rsl[0].label
    score = rsl[0].score
    hit_keywords = rsl[0].hit_keywords
    rst.append(line + [lable, score, hit_keywords])
    if len(rst) % 200 == 0:
        dump_excel(rst, 'rst_shengxi_online_check_1109.xlsx')
dump_excel(rst, 'rst_shengxi_online_check_1109.xlsx')
