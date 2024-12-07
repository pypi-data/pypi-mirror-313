# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from collections import OrderedDict
import json
import requests
import warnings
import numpy as np
import pandas as pd
from aitool import retry, get_lastday_timestamp, sql_result2list
from random import sample


default_folder_token = "fldcn91o2PXaGKiPEss6aWqXQVh"
APP_ID = "cli_9f637a99323d100c"
APP_SECRET = "y0xWseN7SUnVfbBpzKwTuftWnO4tLEho"
APP_VERIFICATION_TOKEN = "KfLznkHqgb6qsYp1AX1MxfvYIDYaANHC"
GET_TOKEN = "https://skynet.bytedance.com/refresh/token"
LARK_API_ID = "SKY_NET"
LARK_API_SECRET = {"SKY_NET": "vMO4C3Gh44TXUIHY"}


@retry(interval=0.1)
def create_sub_sheet(sheet_token, title, index=0, secret=None):
    url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{}/sheets_batch_update".format(
        sheet_token)
    payload = {
        "requests": [
            {"addSheet": {"properties": {"title": title, "index": index}}}
        ]}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': secret}
    r = requests.post(
        url,
        headers=headers, data=json.dumps(payload), timeout=30)
    resp = r.json()
    if resp["code"] == 0:
        return resp["data"]["replies"][0]["addSheet"]["properties"]["sheetId"]
    elif resp["code"] == 90210:
        raise ValueError("title exist")
    else:
        raise Exception("createSubSheet error: {}".format(r.content))


@retry(interval=0.1)
def insert_sheet(token, sub_token, df, secret=None):
    cols = df.columns.tolist()
    value_list = np.array(df).tolist()
    value_list.insert(0, cols)
    if len(value_list) > 5000:
        value_list = value_list[0:5000]
    url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{}/values_prepend".format(
        token)
    payload = {
        "valueRange": {
            "range": "{}!A1:BZ5000".format(sub_token),
            "values": value_list,
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': secret
    }
    r = requests.post(
        url, headers=headers, data=json.dumps(payload), timeout=30)
    resp = r.json()
    if resp["code"] != 0:
        raise Exception("insertValuesToSheet error: {}, token: {}, body: {}".format(r.text, token, str(payload)))


@retry(interval=0.1)
def create_sheet(title, fold_token, secret):
    url = ("https://open.feishu.cn/open-apis/drive/explorer/v2/file/{}".format(
        fold_token))
    payload = {"title": title, "type": "sheet"}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': secret
    }
    r = requests.post(
        url,
        headers=headers, data=json.dumps(payload), timeout=30)
    resp = r.json()
    if resp["code"] == 0:
        return resp["data"]["token"]
    else:
        raise Exception("createSheet error: {}".format(r.content))


# 下面的三个函数用来发送信息
def get_app_access_token():
    """访问apptoken"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + APP_VERIFICATION_TOKEN
    }
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    resp = r.json()
    access_token = resp.get("tenant_access_token")
    return access_token


def get_group_id(access_token):
    # TODO 这个函数有问题
    """得到群ID, 由于机器人只加了一个群, 所以代码实现较简单"""
    url = "https://open.feishu.cn/open-apis/chat/v4/list"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    r = requests.post(url, headers=headers)
    resp = r.json()
    return resp.get("data").get("groups")[0].get("chat_id")


def send_message(msg, link, access_token, group_id=None):
    if not group_id:
        group_id = get_group_id(access_token)
        print(group_id)

    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token
    }
    payload = {
        "chat_id": group_id,
        "msg_type": "text",
        "content": {
            "text": "{msg}\n case链接: {link}".format(msg=msg, link=link)
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    resp = r.json()


def alert_message_use_df(
        msg,
        sheet_dict,
        most_num=10,
        group_id=None,
        chat_id=None,
        file_name="default_lanjun_alert_file",
        fold_token=default_folder_token
):
    secret ="Bearer " + get_app_access_token()
    print("secret = ", secret)
    sheet_token = create_sheet(file_name, fold_token, secret)
    print("sheet_token = ", sheet_token)

    # 对sheet写数据
    cnt = 0
    for sub_name, df in sheet_dict.items():
        df = df.applymap(str)
        sub_sheet_token = create_sub_sheet(sheet_token, sub_name, 0, secret)
        insert_sheet(sheet_token, sub_sheet_token, df, secret)
        cnt += 1
        if cnt >= most_num:
            print("WARNING: PUSH ONLY {}/{} SHEETS.".format(cnt, len(sheet_dict)))
            break
    link = "https://bytedance.feishu.cn/sheets/{}".format(sheet_token)
    app_access_token = "Bearer " + get_app_access_token()
    send_message(msg, link, app_access_token, group_id=group_id)
    print("app_access_token = ", app_access_token)
    # 不需要给文件开放权限了，在界面上操作，直接把整个文件夹的权限开放给飞书群即可。
    # 已过时 add_chat_edit(app_access_token, sheet_token, chat_id)
    return link


def send_feishu_msg(msg, access_token=None, group_id='7216549572061954099'):
    if access_token is None:
        access_token = "Bearer " + get_app_access_token()
    if group_id is None:
        group_id = get_group_id(access_token)

    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token
    }
    payload = {
        "chat_id": group_id,
        "msg_type": "text",
        "content": {
            "text": "{}".format(msg)
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    return r.json()


def send_feishu_sheet(
        result: List,
        result_title: str = 'TaskName',
        other_info: Dict[str, List] = None,
        lark_group_id: str = '7216549572061954099',   # 获取group_id：https://open.feishu.cn/tool/token
        folder_token: str = None,      # 我的目录fang_foler
        limit: int = 1000000,       # 总的最多输出行数
        page_limit: int = 10000,    # 单个文件最多输出行数
        auto_cut=False,             # 自动缩小传输的文本量, 会导致全表变为字符串类型
        auto_cut_line=500,          # 表格的行数上限
        auto_cut_text=1000,          # 每个单元格的截断长度
):
    # 如果生成文件数量多，需要单独建个folder_token，以免文件过多导致失败
    if folder_token is None:
        all_token = [
            'EzjPfS2rOl7kATd0ElBcAUqXn7c',
            'H9XwfGvaslbji1dQi6OcH75jnUg',
            'VC0IfX2e5lyFUpdfFjPcjNsOnWe',
            'IyJ2fj9UglcUVLdt6jKcIY5Enwg',
            'EiU3fOLCqlwRl5dnbShctUcanhe',
            'RsItfm08hl18iAd2SGbc20vInBe',
            'W4BrfeRRMlEEkLdoJRfcRzn6nZc',
            'O9jTfFCLllEOmqd8QrncrgrmnRR',
            'CG5ufqmJwlcoXqdEMzncYDT7ndd',
            'QjpEffD1SlQtPNdwON1cqVl7nAc',
            'V1tOfoQb6lndKKdr2lPcyTWVnFb',
            'Vwosf4p2sldfMIdZbBFcsJXTnDi',
            'OKz9fW4bilnwundfFG3cCkBQnPb',
            'GQ3qfWUJulhNnWdxCtXc5LEcnXb',
            'IcXafNfjzlCNGbdUIz5cL9SEnrc',
            'AkTIfRDXhl8C0Td1OfacdNr1nNh',
            'KfI0fTOyclnX6pdR1gncDl0GnVd',
            'FH3qftGChlHH9Udqsmdc3WvFnvg',
            'FdIdfmvZIlvkxWdpXK9c88LbnRe',
            'BsUNfS65UlnfH0dwNNlceTt2nof',
        ]
        folder_token = sample(all_token, 1)[0]
        print('Warning folder_token is default。'
              '此文件路径定期清空，不要留重要资料在这个目录下。'
              '如果需要长期保留，请输入参数folder_token')
    if auto_cut:
        # TODO 这条链路不支持pd数据格式
        result_new = []
        for line in result:
            line_new = []
            for item in line:
                line_new.append('{}'.format(item)[:auto_cut_text])
            result_new.append(line_new)
            if len(result_new) >= auto_cut_line:
                break
        result = result_new

    all_main_result = []
    output_len = len(result[:limit])
    page_begin = 0
    while page_begin < output_len:
        main_result_part = result[page_begin:page_begin+page_limit]
        page_begin = page_begin + page_limit
        all_main_result.append(pd.DataFrame(main_result_part))
    other_result = {}
    if other_info:
        for k, v in other_info.items():
            other_result[k] = pd.DataFrame(v)

    result_title = result_title + '_{}'.format(get_lastday_timestamp())

    doc_links = []
    for idx, main_result in enumerate(all_main_result):
        if len(all_main_result) > 1:
            result_title_part = result_title + '_part_{}'.format(idx)
        else:
            result_title_part = result_title
        sheet_dict = OrderedDict()
        sheet_dict[result_title_part] = main_result.head(page_limit)
        if idx == 0:
            # 如果多表输出，那么other_info只在第一张表输出
            for _name, _df in other_result.items():
                sheet_dict[_name] = _df.head(page_limit)

        print('开始发送 {}'.format(result_title_part))
        link = alert_message_use_df(result_title_part,
                             sheet_dict,
                             file_name=result_title_part,
                             most_num=1,
                             group_id=lark_group_id,
                             fold_token=folder_token,
                             )
        doc_links.append(link)
    if len(doc_links) == 1:
        return doc_links[0]
    return doc_links


def send_alert_msg(*args, **kwargs):
    warnings.warn("请改用函数send_feishu_sheet，完全兼容", DeprecationWarning)
    send_feishu_sheet(*args, **kwargs)


if __name__ == '__main__':
    send_feishu_sheet([[1, 2, 3], [1, 2, 3]])

    import pandas as pd
    data = {'course': ['数学', '英语', '历史', '科学', '物理'],
            'instructor': ['约翰·史密斯', '萨拉·约翰逊', '迈克·布朗', '卡伦·李', '戴维·金'],
            'batch_size': [43, 25, 19, 51, 48]}
    _df = pd.DataFrame(data)
    send_feishu_sheet(_df)
