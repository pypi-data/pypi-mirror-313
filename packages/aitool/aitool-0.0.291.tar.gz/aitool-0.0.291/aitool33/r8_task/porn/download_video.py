# -*- coding: UTF-8 -*-
import hashlib
import euler
from euler import base_compat_middleware
import aitool.r8_task.idls.redshied_ms_task_thrift as redshied_ms_task_thrift
import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
import pandas as pd
import time
import threading, urllib.request
import os


def vid2url(vid_str):
    get_item_list_client = euler.Client(redshied_ms_task_thrift.TaskService,
                                        'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                        reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    get_item_list_client.use(base_compat_middleware.client_middleware)

    item_list_client = euler.Client(item_list_thrift.GetUserPublishItemListService,
                                    'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                    reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    item_list_client.use(base_compat_middleware.client_middleware)

    refer_items2 = get_item_infos_by_item_id(get_item_list_client, vids=[int(vid_str)])
    # print(refer_items2)
    vids = []

    if isinstance(refer_items2, list) or refer_items2 is [] or refer_items2 == []:
        return
    if refer_items2.VideoInfos is None:
        return

    for v_item in refer_items2.VideoInfos:
        return v_item.URL


def download_url(x, y, woker_idx):
    # 下载 url 并保存到 output_directory 文件夹中
    retry_count = 3
    global out_folder
    opener = urllib.request.build_opener()
    # opener.addheaders = [('cookie', 'Aweme-Internal-Identity=chenzhanwang.johnny@bytedance.com')]
    opener.addheaders = [('cookie', 'Aweme-Internal-Identity=yangjing.yl@bytedance.com')]

    urllib.request.install_opener(opener)
    while True:
        vidstr = None
        try:
            vidstr = vid.pop()

        except Exception as e:
            print(e)
            retry_count -= 1
            print("retry_count ", retry_count)
            time.sleep(3)
            if retry_count < 0:
                print("worker done. ", woker_idx)

                break

        out = '{}.mp4'.format(vidstr)
        out = os.path.join(out_folder, out)
        if os.path.isfile(out):
            print(vidstr, "skip")
            continue

        try:
            url = vid2url(vidstr)
        except Exception as e:
            print(e)
            continue

        try:
            # headers = {'cookie': 'Aweme-Internal-Identity=yangjing.yl@bytedance.com'}
            urllib.request.urlretrieve(url, out)
        except Exception as e:
            print(vidstr, " urlretrieve Exception!")
            print(e)
            continue
        print(vidstr, " downloaded!")


def download_vid(vid, out_dir, skip_exit=True):
    opener = urllib.request.build_opener()
    opener.addheaders = [('cookie', 'Aweme-Internal-Identity=yangjing.yl@bytedance.com')]
    urllib.request.install_opener(opener)
    vidstr = str(vid)
    out = '{}.mp4'.format(vidstr)
    out = os.path.join(out_dir, out)
    if os.path.isfile(out):
        if skip_exit:
            return None
        else:
            return out
    try:
        url = vid2url(vidstr)
    except Exception as e:
        print(e)
        return None
    try:
        urllib.request.urlretrieve(url, out)
    except Exception as e:
        print(vidstr, " urlretrieve Exception!")
        print(e)
        return None
    return out


import byteddps

gdpr_token = byteddps.get_token()
print(gdpr_token)

extra = {"kani": "{\"redshield_god\":[\"all\"], \"data_query_l5\":[\"secret_item\"]}", 'gdpr-token': gdpr_token,
         "email": "yangjing.yl@bytedance.com"}


def md5Pre4(uid):
    md_temp = hashlib.md5(uid.encode("utf-8")).hexdigest()[:4]
    hash = str(int(md_temp, 16))
    return hash.zfill(5)


def make_rowkey_pre4(i):
    return md5Pre4(str(i)) + "_" + str(i)


def get_login_time_map(device_last_time_map):
    login_time_map = {}
    raw_list = device_last_time_map.split(',')
    for item in raw_list:
        if ':' in item:
            device, time = map(int, item.split(':'))
            login_time_map[device] = time
        else:
            login_time_map[int(item)] = None
    return login_time_map


def get_last_banned_time(punish_detail, punish_type):
    last_ban_time = 0
    for k, v in punish_detail.items():
        if k in punish_type and 'startTime' in v:
            last_ban_time = max(last_ban_time, int(v['startTime']))
    return last_ban_time


def is_banned_ever(punish_detail, punish_type):
    is_banned = False
    for k, v in punish_detail.items():
        if k in punish_type:
            is_banned = True
    return is_banned


def clean_bytetable_resp(col):
    if not isinstance(col, dict):
        raise ValueError("bytetable response should be a dict, but {} received!".format(type(col)))
    new_col = {}
    for key, cell in col.items():
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        value = cell.value
        if isinstance(value, bytes):
            new_value = value.decode('utf-8')
            cell.value = new_value
        new_col[key] = cell
    return new_col


def get_items_by_uid(client, uid, latest_k):
    # extra = {"kani": "{\"redshield_god\":[\"all\"]}"}
    base = item_list_thrift.base.Base(Extra=extra)
    req = item_list_thrift.GetUserPublishItemIDMediaTypeListRequest(AuthorID=int(uid), PageSize=latest_k, Base=base)
    try:
        res = client.GetUserPublishItemIDMediaTypeList(req)
    except:
        import pdb
        pdb.set_trace()
        print("Fail to get item list! uid: {}".format(str(uid)))
        return []
    # if 'f1:item_list' not in columns:
    #     return []
    # return sorted(literal_eval(columns['f1:item_list'].value), reverse=True)[:latest_k]
    return res.ItemIDAndMediaTypes


def get_items_by_uidv2(client, uid_list):
    # extra = {"kani": "{\"redshield_god\":[\"all\"]}"}
    base = redshied_ms_task_thrift.base.Base(Extra=extra)
    req = redshied_ms_task_thrift.ListAuthorInfoRequest(uid_list, Base=base)
    try:
        res = client.ListAuthorInfo(req)
    except:
        # import pdb
        # pdb.set_trace()
        print("Fail to get item list! uid: {}".format(str(uid_list)))
        return []
    # columns = client.get_row(user_item_map_table, make_rowkey(uid))[0].columns
    # if 'f1:item_list' not in columns:
    #     return []
    # return sorted(literal_eval(columns['f1:item_list'].value), reverse=True)[:latest_k]
    return res


def get_item_infos_by_item_id(client, vids):
    # extra = {"kani": "{\"redshield_god\":[\"all\"]}"}
    base = redshied_ms_task_thrift.base.Base(Extra=extra)
    # ListVideoInfoResponse ListVideoInfo(1: ListVideoInfoRequest req)
    base.Caller = 'ies.efficiency.turing_open_service_nlp_porn_marketing'
    req = redshied_ms_task_thrift.ListVideoInfoRequest(ItemIDs=vids, Base=base)
    try:
        res = client.ListVideoInfo(req)
    except Exception as e:
        print(e)
        # import pdb
        # pdb.set_trace()
        print("Fail to get item list! item ids: {}".format(str(vids)))
        return []
    # columns = client.get_row(user_item_map_table, make_rowkey(uid))[0].columns
    # if 'f1:item_list' not in columns:
    #     return []
    # return sorted(literal_eval(columns['f1:item_list'].value), reverse=True)[:latest_k]
    print(res)
    return res


def test_items_info():
    print("running test_items_info...")
    get_item_list_client = euler.Client(redshied_ms_task_thrift.TaskService,
                                        'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                        reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    get_item_list_client.use(base_compat_middleware.client_middleware)

    item_list_client = euler.Client(item_list_thrift.GetUserPublishItemListService,
                                    'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                    reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    item_list_client.use(base_compat_middleware.client_middleware)

    # hbase_console = "inf.bytetable.nearline_lf.thriftproxy.bytetable_only.service.lf"
    # table_client = Client(service_name="sd://{}".format(hbase_console),
    #                     timeout=20000,
    #                     reuse_connection=True)

    df = pd.read_csv("/mnt/bn/mlxlabzw/code/jupyter_notebooks/data/不公开视频/p_users.txt")

    ocr2item_id = {}
    ocr2authorid = {}
    # import pdb
    # pdb.set_trace()

    for idx, row in df.iterrows():
        # if idx>10:
        #     break

        # import pdb
        # pdb.set_trace()
        refer_items = get_items_by_uid(item_list_client, row["object_id"], latest_k=50)

        if refer_items is None:
            continue

        try:
            vids = [i.ItemID for i in refer_items]
        except Exception as e:
            print(e)
            continue

        if len(vids) < 1:
            continue
        refer_items2 = get_item_infos_by_item_id(get_item_list_client, vids=vids)
        print(refer_items2)
        vids = []

        # import pdb
        # pdb.set_trace()
        if refer_items2.VideoInfos is None:
            continue

        for v_item in refer_items2.VideoInfos:
            ocr = v_item.OcrText
            if ocr is None:
                ocr = v_item.AsrHumanText
                if ocr is None or ocr.strip() == "":
                    continue
            ocr = ocr.strip()

            ocr = ocr.replace(" ", "")
            ocr = ocr.lower()
            res = []
            for i in ocr:
                if not i.isdigit():
                    res.append(i)
                else:
                    res.append("1")

            ocr = ''.join(res)

            # v_item.OcrText

            # .AuthorID
            if ocr2item_id.get(ocr) and v_item.ItemID not in ocr2item_id[ocr]:
                ocr2item_id[ocr].append(v_item.ItemID)
            else:
                ocr2item_id[ocr] = [v_item.ItemID]

            if ocr2authorid.get(ocr) and v_item.AuthorID not in ocr2authorid[ocr]:
                ocr2authorid[ocr].append(v_item.AuthorID)
            else:
                ocr2authorid[ocr] = [v_item.AuthorID]
    df_ocr_vid = pd.DataFrame(ocr2item_id.items(), columns=['ocr', 'vid'])

    print(df_ocr_vid.head(10))
    df_ocr_vid["vid_len"] = df_ocr_vid["vid"].apply(lambda x: len(x))

    df_ocr_vid.sort_values(by='vid_len', ascending=False).head(2000).to_csv("../csv_out/porn_df_ocr_vid_top0104.csv")

    ###
    df_ocr_aid = pd.DataFrame(ocr2authorid.items(), columns=['ocr', 'aid'])

    print(df_ocr_aid.head(10))
    df_ocr_aid["aid_len"] = df_ocr_aid["aid"].apply(lambda x: len(x))

    df_ocr_aid.sort_values(by='aid_len', ascending=False).head(2000).to_csv("../csv_out/porn_df_ocr_aid_top0104.csv")

    ###


def get_items_info():
    print("running get_items_info...")
    get_item_list_client = euler.Client(redshied_ms_task_thrift.TaskService,
                                        'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                        reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    get_item_list_client.use(base_compat_middleware.client_middleware)

    item_list_client = euler.Client(item_list_thrift.GetUserPublishItemListService,
                                    'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                    reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    item_list_client.use(base_compat_middleware.client_middleware)

    # hbase_console = "inf.bytetable.nearline_lf.thriftproxy.bytetable_only.service.lf"
    # table_client = Client(service_name="sd://{}".format(hbase_console),
    #                     timeout=20000,
    #                     reuse_connection=True)

    # df = pd.read_csv("/mnt/bn/mlxlabzw/code/jupyter_notebooks/data/不公开视频/p_video.txt")
    # item_id_path = "/mnt/bn/mlxlabzw/code/jupyter_notebooks/porn/tmpdata/红军召回.csv"
    item_id_path = "/mnt/bn/mlxlabzw/code/jupyter_notebooks/porn/tmpdata/281475006479063-temp_page-真人色情正例-查询12.csv"

    # df = pd.read_csv(item_id_path, names=['object_id'])
    df = pd.read_csv(item_id_path)

    urls = {}
    for idx, row in df.iterrows():

        refer_items2 = get_item_infos_by_item_id(get_item_list_client, vids=[row["object_id"]])
        # print(refer_items2)
        vids = []

        if isinstance(refer_items2, list) or refer_items2 is [] or refer_items2 == []:
            continue
        if refer_items2.VideoInfos is None:
            continue

        for v_item in refer_items2.VideoInfos:
            ocr = v_item.OcrText
            if ocr is None:
                ocr = v_item.AsrHumanText
                if ocr is None or ocr.strip() == "":
                    continue
            ocr = ocr.strip()

            urls[row["object_id"]] = v_item.URL

            ocr = ocr.replace(" ", "")
            ocr = ocr.lower()
            res = []
            for i in ocr:
                if not i.isdigit():
                    res.append(i)
                else:
                    res.append("1")

            ocr = ''.join(res)
    out_path = item_id_path + "_urlv3.csv"
    with open(out_path, "w") as fout:
        for k, v in urls.items():
            fout.write("{}\n{}\n".format(k, v))

            # v_item.OcrText


# PlayVVCount
def static_vv():
    get_item_list_client = euler.Client(redshied_ms_task_thrift.TaskService,
                                        'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                        reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    get_item_list_client.use(base_compat_middleware.client_middleware)

    item_list_client = euler.Client(item_list_thrift.GetUserPublishItemListService,
                                    'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10,
                                    reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    item_list_client.use(base_compat_middleware.client_middleware)

    # hbase_console = "inf.bytetable.nearline_lf.thriftproxy.bytetable_only.service.lf"
    # table_client = Client(service_name="sd://{}".format(hbase_console),
    #                     timeout=20000,
    #                     reuse_connection=True)

    vids = []
    vv_sum = 0
    import pdb
    pdb.set_trace()
    with open("../uids/xinguan.txt") as fin:
        line = None
        for line in fin:
            try:
                line = int(line)
            except:
                continue
            print(line)
            vids.append(line)
            if len(vids) < 5:
                continue
            refer_items2 = get_item_infos_by_item_id(get_item_list_client, vids=vids)

            print(refer_items2)
            vids = []
            # import pdb
            # pdb.set_trace()
            # if refer_items2.VideoInfos is None:
            #     continue
            if refer_items2 is None:
                continue

            for v_item in refer_items2.VideoInfos:
                vv = v_item.PlayVVCount
                if vv is None:
                    continue
                vv_sum += int(vv)
    print("vv_sum {}".format(vv_sum))


def download_video():
    # os.system("find /mnt/bn/mlxlabzw/code/jupyter_notebooks/porn/tmpdata/mid_porn/ -type f -empty -print -delete")
    # 创建多个线程来下载url
    threads = []

    global vid
    count = 0
    df1 = pd.read_csv('/mnt/bn/mlxlabzw/xiangyuejia/porn/281475007801283-temp_page-色情机审漏放召回-查询5.csv',
                      converters={'item_id': str})
    df = df1[['item_id']].rename(columns={'item_id': 'vid'})
    df = df.drop_duplicates()
    for idx, row in df.iterrows():
        line = row['vid']
        line = str(line)
        print(line)
        line = line.strip()
        # print(line)
        # if "https" not in line:
        #     continue
        vid_str = line
        try:
            int(vid_str)
        except Exception as e:
            print(e)
            continue

        vid.append(vid_str)

        count += 1

    print("vid len ", len(vid))
    # import pdb
    # pdb.set_trace()
    # sys.exit(0)
    for i in range(100):
        thread = threading.Thread(target=download_url, args=(0, 1, i))
        threads.append(thread)
        thread.start()

    # 等待所有线程结束
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    download_vid('7279998796111678780', './')
