from collections import defaultdict, deque
from ast import literal_eval
import hashlib
import time
import json
from multiprocessing import Pool
from aitool import pip_install
import pandas as pd
from tqdm import tqdm


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


class Association_analyzer:
    def __init__(self, user_table, device_table):
        self.user_table = user_table
        self.device_table = device_table
        
    def find_gang(self, 
                  start, 
                  max_degree, 
                  max_member, 
                  max_days_gap, 
                  ban_days, 
                  punish_type=['all', 'douyin_ban_two_level', 'douyin_ban_three_level']
                 ):
        try:
            from bytedhbase.compat import Client
        except ModuleNotFoundError:
            pip_install('bytedhbase')
            from bytedhbase.compat import Client
        frontier = deque()       
        visited_user = set()   
        
        failed_user = set()
        failed_device = set()
        out_of_date_user = set()
        latest_ban_user = set()
        all_ban_user = set()
        
        visited_device = set()
        gang = defaultdict(set)
        came_from = defaultdict(dict)
        
        frontier.append((start, 0))

        hbase_console = "inf.bytetable.nearline_lf.thriftproxy.bytetable_only.service.lf"
        table_client = Client(service_name="sd://{}".format(hbase_console),
                            timeout=10)

        result = {}
        try:
            user_column = table_client.get_row(self.user_table, make_rowkey_pre4(start))[0].columns
            user_column = clean_bytetable_resp(user_column)
            print("user_column: ", user_column)
        except Exception as e:
            print("get_row failed because: {}".format(e))
            print("failed query for uid: {}".format(str(start)))
            failed_user.add(start)
            result['status'] = 1
            return result

        if 'cf:device_id_array' not in user_column:
            failed_user.add(start)
            print("no device_id_array in user_column")
            result['status'] = 1
            return result

        visited_user.add(start)
        came_from[start] = {}
        gang[0].add(start)
        if 'cf:punish_detail' in user_column:
            punish_detail = literal_eval(user_column['cf:punish_detail'].value)
            if is_banned_ever(punish_detail, punish_type):
                all_ban_user.add(start)
            if time.time() - get_last_banned_time(punish_detail, punish_type) <= ban_days * 24 * 3600:
                latest_ban_user.add(start)
        
        while frontier:
            cur_user, cur_degree = frontier.popleft()

            if cur_degree >= max_degree:
                break
            try:
                user_column = table_client.get_row(self.user_table, make_rowkey_pre4(cur_user))[0].columns
                user_column = clean_bytetable_resp(user_column)
            except Exception as e:
                print("get_row failed because: {}".format(e))
                print("failed query for uid: {}".format(str(cur_user)))
                failed_user.add(cur_user)
                visited_user.remove(cur_user)
                gang[cur_degree].remove(cur_user)
                continue

            if 'cf:device_id_array' not in user_column:
                failed_user.add(cur_user)
                visited_user.remove(cur_user)
                print("no device_id_array in user_column")
                gang[cur_degree].remove(cur_user)
                continue
                        
            device_list = literal_eval(user_column['cf:device_id_array'].value)            
            device_last_time_map = user_column['cf:device_last_time_map'].value
            device_login_time_map = get_login_time_map(device_last_time_map)

            for device in device_list:
                if device not in visited_device:
                    try:
                        device_column = table_client.get_row(self.device_table, make_rowkey_pre4(device))[0].columns
                        device_column = clean_bytetable_resp(device_column)
                    except:
                        print("failed to fetch device column")
                        failed_device.add(device)
                        continue
                    if 'cf:user_id_array' not in device_column:
                        failed_device.add(device)
                        print("no user_id_device in device_column")
                        continue
                    visited_device.add(device)
                    user_last_time_map = device_column['cf:user_last_time_map'].value
                    user_login_time_map = get_login_time_map(user_last_time_map)
                    for neighbor in literal_eval(device_column['cf:user_id_array'].value):
                        if neighbor not in visited_user:
                            cur_user_login_time = user_login_time_map[cur_user] if cur_user in user_login_time_map else device_login_time_map[device]
                            if (user_login_time_map[neighbor] and cur_user_login_time) and abs(user_login_time_map[neighbor] - cur_user_login_time) >= max_days_gap * 24 * 3600:
                                out_of_date_user.add(neighbor)
                                continue

                            try:
                                user_column = table_client.get_row(self.user_table, make_rowkey_pre4(neighbor))[0].columns
                                user_column = clean_bytetable_resp(user_column)
                            except:
                                failed_user.add(neighbor)
                                continue
                                
                            if 'cf:device_id_array' not in user_column:
                                failed_user.add(neighbor)
                                print("no device_id_array in user_column")
                                continue
                            
                            if 'cf:punish_detail' in user_column:
                                punish_detail = literal_eval(user_column['cf:punish_detail'].value)
                                if is_banned_ever(punish_detail, punish_type):
                                    all_ban_user.add(neighbor)
                                if time.time() - get_last_banned_time(punish_detail, punish_type) <= ban_days * 24 * 3600:
                                    latest_ban_user.add(neighbor)

                            frontier.append((neighbor, cur_degree+1))
                            visited_user.add(neighbor)
                            gang[cur_degree+1].add(neighbor)
                            came_from[neighbor]['uid'] = cur_user
                            came_from[neighbor]['did'] = device
                            
                            if len(visited_user) >= max_member:
                                result['status'] = 0
                                result['start'] = str(start)
                                result['gang'] = str(dict(gang))
                                result['came_from'] = str(dict(came_from))
                                result['count_sucessed_user'] = len(visited_user)
                                result['count_failed_user'] = len(failed_user)
                                result['count_out_of_date_user'] = len(out_of_date_user)
                                result['user_banned_in_{:d}_days'.format(ban_days)] = sorted(map(int, list(latest_ban_user)))
                                result['count_user_banned_in_{:d}_days'.format(ban_days)] = len(latest_ban_user)
                                result['ratio_of_latest_banned_user'] = round(len(latest_ban_user)  / len(visited_user), 2)
                                result['count_user_banned_ever'] = len(all_ban_user)
                                result['ratio_of_ever_banned_user'] = round(len(all_ban_user)  / len(visited_user), 2)
                                return result

        if len(visited_user) == 0:
            result['status'] = 1
            return result
        
        result['status'] = 0
        result['start'] = str(start)
        result['gang'] = str(dict(gang))

        result['came_from'] = str(dict(came_from))
        result['count_sucessed_user'] = len(visited_user)
        result['count_failed_user'] = len(failed_user)
        result['count_out_of_date_user'] = len(out_of_date_user)
        result['user_banned_in_{:d}_days'.format(ban_days)] = sorted(map(int, list(latest_ban_user)))
        result['count_user_banned_in_{:d}_days'.format(ban_days)] = len(latest_ban_user)
        result['ratio_of_latest_banned_user'] = round(len(latest_ban_user)  / len(visited_user), 2)
        result['count_user_banned_ever'] = len(all_ban_user)
        result['ratio_of_ever_banned_user'] = round(len(all_ban_user)  / len(visited_user), 2)

        return result
    
    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = ['uid:' + str(current)]
        while current != start:
            last = came_from[current]
            path.append('did:' + str(last['did']))
            path.append('uid:' + str(last['uid']))
            current = last['uid']
        path.reverse()
        return path        


def find_gang(uid):
    user_table = "ies_lanjun:lanjun_fraud_user_portrait"
    device_table = "ies_lanjun:lanjun_fraud_device_portrait"
    analyzer = Association_analyzer(user_table, device_table)
    result = analyzer.find_gang(start=uid, max_degree=3, max_member=50, max_days_gap=180, ban_days=60)
    if result['status'] == 0:
        mark = 1
    else:
        mark = 0
    return mark, result


def filter_by_multi_modal(df_raw):
    df_raw['ratio_of_latest_banned_user'] = df_raw['ratio_of_latest_banned_user'].apply(lambda x: float(x))
    df_raw['ratio_of_ever_banned_user'] = df_raw['ratio_of_ever_banned_user'].apply(lambda x: float(x))
    print(df_raw.head())
    cond1 = df_raw['count_sucessed_user'].astype(float) >= 2
    cond2 = df_raw['ratio_of_latest_banned_user'].astype(float) >= 0
    df_raw['difference_between_banned_ratio'] = df_raw['ratio_of_ever_banned_user'] - df_raw['ratio_of_latest_banned_user']
    df_filter = df_raw.loc[(cond1)&(cond2), :]
    df_sorted = df_filter.sort_values(by='difference_between_banned_ratio', ascending=False)
    print(df_sorted.head())
    print(df_sorted.shape)

    result_df = []
    for _, row in tqdm(df_sorted.iterrows(), total=df_sorted.shape[0], desc="Generating final results..."):
        user_id = row['start']
        print(user_id)

        group = df_sorted.loc[df_sorted['start']==user_id, :].to_dict('records')[0]

        print("-----------------Start to filter gang----------------")
        results = filter_gang_parallel(start=user_id, gang=group['gang'], similar_score_thres=0.8, similar_count_thres=2)
        if results['gang_size'] > 1:
            result_df.append(results)

    result_df = pd.DataFrame(result_df)
    return result_df


def clean_row_output(results):
    for i in results:
        if i == 'gang_user_info':
            results[i] = json.dumps(results[i])
        else:
            results[i] = str(results[i])
    return results


def row_filter_by_multi_modal(row_dict):
    results = {}
    results['start_uid'] = "start"
    results['gang_size'] = "len(gang_uids)"
    results['gang_uids'] = "gang_uids"
    results['similar_items'] = "all_similar_items"
    results['gang_user_info'] = "gang_user_info_list"

    row_dict['ratio_of_latest_banned_user'] = float(row_dict['ratio_of_latest_banned_user'])
    row_dict['ratio_of_ever_banned_user'] = float(row_dict['ratio_of_ever_banned_user'])
    cond1 = 1 if float(row_dict['count_sucessed_user']) >= 2 else 0
    cond2 = 1 if float(row_dict['ratio_of_latest_banned_user']) >= 0 else 0
    row_dict['difference_between_banned_ratio'] = row_dict['ratio_of_ever_banned_user'] - row_dict['ratio_of_latest_banned_user']
    if not(cond1 and cond2):
        return 0, results
    user_id = row_dict['start']
    results = filter_gang_parallel(start=user_id, gang=row_dict['gang'], similar_score_thres=0.8, similar_count_thres=2)
    results = clean_row_output(results)
    if float(results['gang_size']) > 1:
        return 1, results
    return 0, results


def get_video_similarity(item_id_1, item_id_2, media_type=4):
    # media_type 图集 = 2  视频 = 4
    item_id_1 = str(item_id_1)
    item_id_2 = str(item_id_2)
    try:
        from euler import base_compat_middleware, Client as EClient
        import aitool.r8_task.idls.cv_project_template_thrift as similarity_thrift
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
    except ModuleNotFoundError:
        pip_install('bytedeuler==0.41.1  --index-url=https://bytedpypi.byted.org/simple/')
        from euler import base_compat_middleware, Client as EClient
        import aitool.r8_task.idls.cv_project_template_thrift as similarity_thrift
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
    similarity_client = EClient(similarity_thrift.Service, 'sd://ies.efficiency.landun_service_teenager?idc=lf&cluster=similarity', timeout=10, reuse_connection=True)
    similarity_client.use(base_compat_middleware.client_middleware)

    req = similarity_thrift.VideoMultiModalSimilarityRequest(item_id_1=item_id_1,
                                                            item_id_2=item_id_2,
                                                            media_type=media_type)

    try:
        resp = similarity_client.video_multimodal_similarity(req)
    except Exception:
        print("failed calculation! {} vs {}".format(str(item_id_1), str(item_id_2)))
        return -2
    if resp.prob >= 0:
        return resp.prob
    return -1


def get_items_by_uid(client, uid, latest_k):
    try:
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
    except ModuleNotFoundError:
        pip_install('bytedeuler==0.41.1  --index-url=https://bytedpypi.byted.org/simple/')
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
    extra = {"kani": "{\"redshield_god\":[\"all\"]}"}
    base = item_list_thrift.base.Base(Extra=extra)
    req = item_list_thrift.GetUserPublishItemIDMediaTypeListRequest(AuthorID=int(uid), PageSize=latest_k, Base=base)
    try:
        res = client.GetUserPublishItemIDMediaTypeList(req)
    except:
        import pdb
        pdb.set_trace()
        print("Fail to get item list! uid: {}".format(str(uid)))
        return []

    return res.ItemIDAndMediaTypes


def check_similar_user(refer_items, query_id, similar_score_thres, similar_count_thres):
    try:
        from euler import base_compat_middleware, Client as EClient
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
    except ModuleNotFoundError:
        pip_install('bytedeuler==0.41.1  --index-url=https://bytedpypi.byted.org/simple/')
        from euler import base_compat_middleware, Client as EClient
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift

    item_list_client = EClient(item_list_thrift.GetUserPublishItemListService, 'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10, reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    item_list_client.use(base_compat_middleware.client_middleware)

    query_items = get_items_by_uid(item_list_client, query_id, 5)
    print(query_id, query_items)
    found = False
    print("this loop")
    similar_count = 0
    cal_count = 0
    similar_items = []
    for q in query_items:
        if found:
            break
        for r in refer_items:
            if found:
                break
            cal_count += 1
            mt1, mt2 = q.MediaType, r.MediaType
            item_id_1, item_id_2 = q.ItemID, r.ItemID
            if mt1 == mt2 == 2:
                score = get_video_similarity(item_id_1, item_id_2, media_type=2)
            elif mt1 == mt2 == 4:
                score = get_video_similarity(item_id_1, item_id_2, media_type=4)
            else:
                score = -1
            print(query_id, score)
            if score < 0:
                continue
            elif score > similar_score_thres:
                similar_items.append((item_id_1, item_id_2))
                similar_count += 1
            if similar_count >= similar_count_thres:
                found = True
    print("{:d} visited, similar count: {:d}, similar items: {}".format(query_id, similar_count, ' '.join(map(str, similar_items))))
    print(query_id, similar_items)
    return query_id, found, similar_items, query_items, cal_count


def filter_gang_parallel(start, gang, similar_score_thres, similar_count_thres):
    try:
        from euler import base_compat_middleware, Client as EClient
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
    except ModuleNotFoundError:
        pip_install('bytedeuler==0.41.1  --index-url=https://bytedpypi.byted.org/simple/')
        from euler import base_compat_middleware, Client as EClient
        import aitool.r8_task.idls.get_item_list_with_mediatype_thrift as item_list_thrift
    item_list_client = EClient(item_list_thrift.GetUserPublishItemListService, 'sd://ies.efficiency.redshied_ms_task?cluster=default', timeout=10, reuse_connection=True)  # 如果reuse_connection=False可能回报cannot connect to 某个ip的错误
    item_list_client.use(base_compat_middleware.client_middleware)

    refer_items = get_items_by_uid(item_list_client, start, 5)
    print(refer_items)
    gang_uids = [int(start)]
    all_similar_items = {}
    all_res = []
    uid_list = []
    gang_user_info_list = [
        {
            "UserID": int(start),
            "VideoItemIDList": [i.ItemID for i in refer_items],
            "CommentIDList": [],
            "Remark": ""
            }
    ]

    if not isinstance(gang, dict):
        try:
            gang = literal_eval(gang)
        except Exception as e:
            print("gang must be a dictionary!")
            raise(e)

    with Pool(10) as pool:       
        for k, v in gang.items():
            if k == 0:
                continue
            for uid in v:
                print(uid)
                res = pool.apply_async(check_similar_user, args=(refer_items, uid, similar_score_thres, similar_count_thres))
                all_res.append(res)
                uid_list.append(uid)

        pool.close()
        pool.join()

    for u, res in zip(uid_list, all_res):
        if res.ready():
            print('ready!')
            if res.successful():
                print('successful!')
                uid, found, items, query_items, cal_count = res.get()
                print(uid, cal_count)
                if found:
                    gang_uids.append(uid)
                    all_similar_items[uid] = items
                    gang_member = {
                        "UserID": uid,
                        "VideoItemIDList": [i.ItemID for i in query_items],
                        "CommentIDList": [],
                        "Remark": ""
                    }
                    gang_user_info_list.append(gang_member)
                
            else:
                print("unsuccessful!~~~~~~~~~~~~~~~~")
                try:
                    a, b, c, d = res.get()
                except Exception as e:
                    print(e)
                    print("unsuccessful id: {}".format(str(u)))
        else:
            print('not ready!')
        
    results = {}
    results['start_uid'] = start
    results['gang_size'] = len(gang_uids) 
    results['gang_uids'] = gang_uids
    results['similar_items'] = all_similar_items  
    results['gang_user_info'] = gang_user_info_list      
    return results


if __name__ == "__main__":
    print(get_video_similarity(7223603415933308220, 7223584221137325349))
    print(find_gang(2414970203285024))
