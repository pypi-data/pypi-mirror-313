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
from tqdm import tqdm
from collections import defaultdict
from aitool import User, Obj, Report, Comment, Message, Device, Ip
from aitool import sql_user_report, sql_user_profile_blue, sql_comment, sql_message, send_alert_msg


def load_data(time_span=15, limit=100000):
    # node
    user = {}
    obj = {}
    comment = {}    # 按hash做聚类
    message = []
    device = {}
    ip = {}

    # relation
    report = []

    # 1.举报-关系
    # "reporter_id","object_id","object_type","object_owner_id","report_reason",
    # "report_desc","report_create_time","report_status"
    # "2616489297320168","7160348399122894087","101","75780639264","101","底裤都漏出来了，这种低俗演绎还是直接封号吧，学生也用手机，看到不学习了天天看这个，请求直接封号拉到了，成年人怎么都行，青少年还是得注意，支持还平台绿色环境","1667232017","1"
    print('begin sql_user_report')
    data = sql_user_report(time_span, limit=limit)
    print('end sql_user_report')
    print(data[:1])
    stt_status = defaultdict(int)
    related_uid = set()
    for reporter_id, object_id, object_type, object_owner_id, report_reason, report_desc, report_create_time, report_status in tqdm(
            data, desc='step_1'):
        related_uid.add(reporter_id)
        related_uid.add(object_owner_id)
        if reporter_id not in user:
            user[reporter_id] = User()
            user[reporter_id].id = reporter_id
        if object_id not in obj:
            obj[object_id] = Obj()
            obj[object_id].id = object_id
            obj[object_id].type = object_type
        if object_owner_id not in user:
            user[object_owner_id] = User()
            user[object_owner_id].id = object_owner_id
        _rep = Report()
        _rep.type = report_reason
        _rep.msg = report_desc
        _rep.time = report_create_time
        _rep.status = report_status
        stt_status[report_status] += 2
        _rep.user = reporter_id
        _rep.obj = obj[object_id]
        report.append(_rep)
        user[reporter_id].report.append(_rep)
        user[object_owner_id].object.add(obj[object_id])
        if _rep.status == 2:
            user[object_owner_id].report_status = 2
        obj[object_id].user = user[object_owner_id]
        obj[object_id].report.append(_rep)
    print(str(dict(stt_status)))
    related_uid = list(related_uid)

    # 2
    # "user_id","user_create_days","status","is_fake_user","is_canceled","os","city_resident",
    # "report_reason_success_rate_30day","publish_activeness","vv","comment_cnt","like_cnt",
    # "follow_cnt","publish_cnt_30d","comment_cnt_30d","dist_device_id_90d","dist_ip_90d",
    # "dist_location_90d","login_90d_cnt"
    # "3131827223","1841","1","0","0","ios","约克","[0.0,0.0,1.0,0.9285714,1.0,0.0,0.0,0.8333333]","4","253","2","2","0","20","411","[]","[]","[]","0"
    # "6665194518","1752","1","0","0","ios","崇左","NULL","2","191","0","6","0","2","1","[1997179242681438]","[""171.111.232.150"",""106.127.108.206"",""111.58.114.216"",""106.127.102.119"",""240e:452:dd5f:4ec1:9cb4:5673:258b:6946"",""240e:452:dd70:c70f:c515:7513:db0a:d7e1"",""116.10.220.150"",""111.58.114.92""]","[""南宁"",""河池"",""崇左""]","8"
    print('begin sql_user_profile_blue')
    data = sql_user_profile_blue(None, time_span=time_span, limit=limit)
    print('end sql_user_profile_blue')
    print(data[:1])
    stt_status = defaultdict(int)
    for user_id, user_create_days, status, is_fake_user, is_canceled, os, city_resident, report_reason_success_rate_30day, publish_activeness, vv, comment_cnt, like_cnt, follow_cnt, publish_cnt_30d, comment_cnt_30d, dist_device_id_90d, dist_ip_90d, dist_location_90d, login_90d_cnt in tqdm(
            data, desc='step_2'):
        dist_device_id_90d = dist_device_id_90d
        dist_ip_90d = dist_ip_90d
        dist_location_90d = dist_location_90d
        if user_id not in user:
            user[user_id] = User()
        user[user_id].user_create_days = user_create_days
        user[user_id].status = status
        stt_status[status] += 1
        user[user_id].is_fake_user = is_fake_user
        user[user_id].is_canceled = is_canceled
        user[user_id].city_resident = city_resident
        user[user_id].publish_cnt_30d = publish_cnt_30d
        for a_device in dist_device_id_90d:
            if a_device not in device:
                device[a_device] = Device()
                device[a_device].id = a_device
                device[a_device].user.add(user_id)
            user[user_id].dist_device_id_90d.add(device[a_device])
        for a_ip in dist_ip_90d:
            if a_ip not in ip:
                ip[a_ip] = Ip()
                ip[a_ip].id = a_ip
                ip[a_ip].user.add(user[user_id])
            user[user_id].dist_ip_90d.add(ip[a_ip])
        user[user_id].dist_location_90d = dist_location_90d
    print(str(dict(stt_status)))

    # 4
    # "user_id","group_id","create_time","text","comment_count","login_digg_count","login_bury_count"
    # "101778196372","7161409601101925670","1667567130","没关系啊，今天刷到你愿意让榜一做什么然后给你多少钱的视频，我拒绝了[皱眉]，因为我发现你是我的榜一[害羞][送心]","0","0","0"
    # "2889988894104412","7166932025784438030","1668755111","…这个我有微信要不要","0","0","0"
    print('begin sql_comment')
    data = sql_comment(None, time_span=time_span, limit=limit)
    print('end sql_comment')
    print(data[:1])
    # Row(status=1, user_id=4361475301, group_id=7204620347394641191, review_status=0, create_time=1677469610, text='华为mate20 256二手的多少钱', comment_count=1, login_digg_count=0, login_bury_count=0)]
    for user_id, group_id, create_time, text, comment_count, login_digg_count, login_bury_count, _, _ in tqdm(data,
                                                                                                        desc='step_4'):
        if user_id not in user:
            continue
        _cmt = Comment()
        _cmt.hash = hash(text)
        _cmt.text = text
        _cmt.user = user[user_id]
        if group_id in obj:
            _cmt.obj = obj[group_id]
        _cmt.time = create_time
        user[user_id].cmt.append(_cmt)
        if _cmt.hash not in comment:
            comment[_cmt.hash] = []
        comment[_cmt.hash].append(_cmt)

    # 5
    # "device_id","uid","follow_type","ip","EXPR$4","EXPR$5","EXPR$6","EXPR$7","EXPR$8","EXPR$9","to_id","create_time"
    # "479820548964007","75762969718","2","112.19.88.37","微信","NULL","NULL","NULL","NULL","NULL","98669241889","1669618864"
    # "2080737358309576","88815193464","2","175.20.230.110","加","微信","微信","加","微信","NULL","84645287695","1669618815"
    print('begin sql_message')
    data = sql_message(time_span=time_span, limit=limit)
    print('end sql_message')
    print(data[:1])
    for device_id, uid, follow_type, _ip, EXPR4, EXPR5, EXPR6, EXPR7, EXPR8, EXPR9, to_id, create_time in tqdm(data,
                                                                                                               desc='step_5'):
        if device_id not in device:
            device[device_id] = Device()
            device[device_id].id = device_id
            device[device_id].user.add(uid)
        if uid in user:
            user[uid].dist_device_id_90d.add(device[device_id])
            if _ip not in ip:
                ip[_ip] = Ip()
                ip[_ip].id = _ip
            ip[_ip].user.add(user[uid])
        _msg = Message()
        _msg.device = device[device_id]
        _msg.follow_type = follow_type
        word_str = ''
        for w_str in [EXPR4, EXPR5, EXPR6, EXPR7, EXPR8, EXPR9]:
            if w_str and w_str != 'Null' and w_str != 'null' and w_str != 'NULL':
                word_str += w_str
        word_str = list(set(word_str))
        word_str.sort()
        word_str = ''.join(word_str)
        _msg.word = word_str
        if uid in user:
            _msg.user = user[uid]
            user[uid].msg.append(_msg)
        else:
            _msg.user = uid
        if to_id in user:
            _msg.to_user = user[to_id]
        else:
            _msg.to_user = to_id
        _msg.time = create_time
        message.append(_msg)
    return user, obj, comment, message, device, ip, report


# 已被处置的账号比例
def users_are_banned(users, user=None, print_pre=''):
    users = set(users)
    users_with_status = []
    banned = []
    for uid in users:
        if uid not in user or user[uid].report_status is None:
            continue
        users_with_status.append(uid)
        if user[uid].report_status == 2:
            banned.append(users)
    if len(users_with_status):
        rate = len(banned)/len(users_with_status)
    else:
        rate = 'NaN'
    print(print_pre, 'select', len(users), 'record', len(users_with_status), 'banned', len(banned),
          'rate', rate)
    return banned


# 1、刷评论：comment内容相同的多个号 + 被report用户
def search_same_comment(user=None, comment=None, file_name='1_大量相同内容comment'):
    rst = []
    tt = 0
    warn10all = []
    warn50all = []
    warn200all = []
    warn500all = []
    for key, cmts in tqdm(comment.items()):
        tt+=1
        user_count = defaultdict(int)
        warn10 = []
        warn50 = []
        warn200 = []
        warn500 = []
        tt += 1
        tt += 1
        for cmt in cmts:
            user_count[cmt.user.id] += 1
        for _uid, _time in user_count.items():
            if _time > 150:
                warn500.append(_uid)
                # warn500.append(user[_uid].report_status)
                warn500all.append(_uid)
            elif _time > 70:
                warn200.append(_uid)
                warn200.append(user[_uid].report_status)
                warn200all.append(_uid)
            elif _time > 30:
                warn50.append(_uid)
                warn50.append(user[_uid].report_status)
                warn50all.append(_uid)
            elif _time > 10:
                warn10.append(_uid)
                warn10.append(user[_uid].report_status)
                warn10all.append(_uid)
        if warn10 or warn50 or warn200 or warn500:
            rst.append([len(cmts), cmts[0].text, warn500, warn200, warn50, warn10])
    users_are_banned(warn500all, user=user, print_pre='warn500all')
    users_are_banned(warn200all, user=user, print_pre='warn200all')
    users_are_banned(warn50all, user=user, print_pre='warn50all')
    users_are_banned(warn10all, user=user, print_pre='warn10all')
    send_alert_msg(rst, msg=file_name)
    print('tt', tt)
    return rst


# 2、刷私信：一个人发过多数量Message + 被report用户
def search_massive_message(user=None, file_name='2_发过多数量私信'):
    user_list = []
    msg_list = []
    key_list = []
    tt = 0
    for uid, v in user.items():
        tt += 2
        _count = len(v.msg)
        if _count > 0:
            user_list.append(v)
            msg_list.append(_count)
            key_count = defaultdict(int)
            for _msg in v.msg:
                for w in _msg.word:
                    key_count[w] += 1
            key_list.append(key_count)
    user_count = len(user_list)
    msg_count = sum(msg_list)
    avg_msg_count = msg_count / user_count
    for power in range(2, 7):
        user_select = []
        rst_file = []
        for ul, ml, kl in zip(user_list, msg_list, key_list):
            if len(ul.object) == 0:
                continue
            if ml > avg_msg_count * power:
                user_select.append(ul.id)
                rst_file.append([ul.id, str(dict(kl))])
        users_are_banned(user_select, user=user, print_pre='power {}:'.format(power))
        send_alert_msg(rst_file, msg=file_name+'power {}'.format(power))
    print('tt', tt)
    return rst_file


# 3、过多report
def bad_report(user=None, file_name='3_过多Report'):
    rst = []
    tt = 0
    for uid, v in user.items():
        tt += 2
        rp_num = 0  # 总report数量
        rp_msgs = defaultdict(int)
        rp_times = []
        rp_status = defaultdict(int)
        rp_obj = set()  # 举报的obj
        for rp in v.report:
            rp_num += 1
            rp_msgs[rp.msg] += 1
            rp_times.append(rp.time)
            rp_status[rp.status] += 1
            rp_obj.add(rp.obj)
        if rp_num > 10:
            rst.append([uid, rp_num, len(rp_obj), str(dict(rp_status)), str(dict(rp_msgs))])
    send_alert_msg(rst, msg=file_name)
    print('tt', tt)
    return rst


# 4. 短时间内密集发评数量和密集发评占比
def dense_comment(user=None, interval=600, dense=5, file_name='4_dense_comment'):
    rst = []
    for uid, v in user.items():
        times = []
        for cmt in v.cmt:
            times.append(int(cmt.time))
        times.sort()
        size = len(times)
        if size < 5:
            continue
        dense_bag = 0  # 一共能找到几个dense区域
        dense_cmt = 0  # dense区域中一共有多少条评论
        h = t = 0
        while t < size-1:
            while h < size-1 and times[h+1] - times[t] < interval:
                h += 1
            if h-t+1 >= dense:
                dense_bag += 1
                dense_cmt += h-t+1
                h = t = min(h+1, size-1)
            else:
                t += 1
        if dense_bag > 0:
            rst.append([uid, size, dense_bag, dense_cmt, dense_cmt/size])
    send_alert_msg(rst, msg=file_name+'_itv{}_ds{}'.format(interval, dense))
    return rst


# 5、被举报成功的被处罚用户的举报人扩展，输出被举报3次的用户
def effective_reporter(user=None, file_name='./result/5_effective_reporter'):
    rst = []
    good_reporter = set()
    for uid, v in user.items():
        if v.status == 0:
            for ob in v.object:
                for rp in ob.report:
                    good_reporter.add(user[rp.user])
    print('good_reporter:', len(good_reporter))
    objs = defaultdict(int)
    for u in good_reporter:
        for rp in u.report:
            objs[rp.obj] += 1
    for o, t in objs.items():
        if t >= 1:
            rst.append([o, o.user, t])
    send_alert_msg(rst, msg=file_name)
    return rst


# 6、计算30天举报成功率和举封成功率，分别用1.0，0.5做阈值筛选被举报用户
def success_rate_reporter(user=None, report=None, thr_scs=0.2, thr_bad=0.1, file_name='6_success_rate_reporter'):
    bad_user = set()
    bad_obj = set()
    obj_scs = defaultdict(int)
    obj_bad = defaultdict(int)
    user_scs = defaultdict(int)
    user_bad = defaultdict(int)
    user2obj = defaultdict(set)
    for uid, v in user.items():
        if v.status == 0:
            bad_user.add(v)
    print('bad_user:', len(bad_user))
    for rp in report:
        if rp.status == 2:
            bad_obj.add(rp.obj)
    print('bad_obj:', len(bad_obj))

    for uid, v in user.items():
        _rp_all = 0  # 不及时未审核的举报
        _rp_scs = 0
        _rp_bad = 0
        # 计算用户的举报成功率和举报封号率
        for rp in v.report:
            if rp.status == '1':
                continue
            _rp_all += 1
            if rp.obj in bad_obj:
                _rp_scs += 1
            if rp.obj.user in bad_user:
                _rp_bad += 1
        if _rp_all == 0:
            continue
        _rp_rate_scs = _rp_scs / _rp_all
        _rp_rate_bad = _rp_bad / _rp_all
        # 计算被举报对象的分数
        for rp in v.report:
            obj_scs[rp.obj] += _rp_rate_scs
            obj_bad[rp.obj] += _rp_rate_bad
            user_scs[rp.obj.user] += _rp_rate_scs
            user_bad[rp.obj.user] += _rp_rate_bad
            user2obj[rp.obj.user].add(rp.obj)
    rst_obj = []
    for k, v in obj_scs.items():
        if v > thr_scs and obj_bad[k] > thr_bad:
            rst_obj.append([k.id, k.type, k.user, v, obj_bad[k]])
    rst_user = []
    for k, v in user_scs.items():
        if v > thr_scs and user_bad[k] > thr_bad:
            rst_user.append([k.id, k.type, k.user, v, user_bad[k], str(user2obj[k])])
    send_alert_msg(rst_obj, msg=file_name+'_obj')
    send_alert_msg(rst_user, msg=file_name+'_user')
    return rst_obj, rst_user


if __name__ == '__main__':
    from aitool import load_data4risk
    _user, _obj, _comment, _message, _device, _ip, _report = load_data4risk()

    # 1、刷评论：comment内容相同的多个号 + 被report用户
    search_same_comment(user=_user, comment=_comment)
    # 2、刷私信：一个人发过多数量Message + 被report用户
    search_massive_message(user=_user)
    # 3、过多report
    bad_report(user=_user)
    # 4. 短时间内密集发评数量和密集发评占比
    dense_comment(user=_user)
    # 5、被举报成功的被处罚用户的举报人扩展
    effective_reporter(user=_user)
    # 6、计算30天举报成功率和举封成功率，分别用1.0，0.5做阈值筛选被举报用户
    success_rate_reporter(user=_user, report=_report)
