# -*- coding: UTF-8 -*-
import hashlib
import os
from importlib import import_module
from random import sample
import time
from aitool import pip_install

# 你需要访问的thrift的服务路径，比如：
SERVER_SERVICE = 'aitool.r8_task.idls.risk_thrift.TaskService'
SERVER_TARGET = 'sd://ies.efficiency.redshied_ms_task?cluster=default'
# 你的thrift文件的路径，比如：
SERVER_THRIFT = 'aitool.r8_task.idls.risk_thrift'


def make_rowkey_pre4(i):
    return md5Pre4(str(i)) + "_" + str(i)


def md5Pre4(uid):
    md_temp = hashlib.md5(uid.encode("utf-8")).hexdigest()[:4]
    hash = str(int(md_temp, 16))
    return hash.zfill(5)


def get_env_type():
    """
    环境类型: dev、boe、prod
    """
    euler_env = os.getenv("EULER_ENV", '')
    return euler_env.split('.')[-1]


def import_attr(path):
    modules = path.split('.')
    module_name = '.'.join(modules[:-1])
    attr_name = modules[-1]
    return getattr(import_module(module_name), attr_name)


class Task():
    def __init__(self):
        """
        # - 报送产品线：抖音
        """
        try:
            import euler
        except ModuleNotFoundError:
            pip_install('bytedhbase  --index-url=https://bytedpypi.byted.org/simple/')
            pip_install('euler  --index-url=https://bytedpypi.byted.org/simple/')
            import euler
        try:
            import byteddps
        except ModuleNotFoundError:
            pip_install('byteddps  --index-url=https://bytedpypi.byted.org/simple/')
            import byteddps
        self.env = get_env_type()
        self.client = euler.Client(import_attr(SERVER_SERVICE), SERVER_TARGET)
        self.server_thrift = import_attr(SERVER_THRIFT)
        extra = {"kani": "{\"redshield_god\":[\"all\"], \"data_query_l5\":[\"secret_item\"]}",
                 "email": "xiangyuejia@bytedance.com"}
        # TODO 端口做了权限控制，需要使用用户自己有权限的psm，找yangjing.yl开通
        self.base = self.server_thrift.base.Base(
            Caller='ies.efficiency.text_analyse',
            Extra=extra
        )
        gdpr_token = byteddps.get_token()
        # print(gdpr_token)

    def query_risk(self, time_start, time_end) -> list:
        the_GangQueryCondition = self.server_thrift.GangQueryCondition(
            StatusList=['risk'],
            RecallWayList=['known'],
            StartJudgeTime=int(time_start),
            EndJudgeTime=int(time_end),
        )
        the_CommonQueryCondition = self.server_thrift.CommonQueryCondition(
            PageNum=1,
            PageSize=100,
            OrderByColumn='CreateTime',
            OrderType='desc',
        )

        req = self.server_thrift.GetGangListRequest(
            GangQueryCondition=the_GangQueryCondition,
            CommonQueryCondition=the_CommonQueryCondition,
            Base=self.base,
        )
        resp = self.client.GetGangList(req)
        return resp


def get_risk(time_start=None, time_end=None, day=1):
    time_now = time.time()
    if time_start is None:
        time_start = time_now - day*24*60*60
    if time_end is None:
        time_end = time_now
    try:
        import euler
    except ModuleNotFoundError:
        pip_install('bytedhbase --index-url=https://bytedpypi.byted.org/simple/')
        import euler

    euler.install_thrift_import_hook()
    test_service = Task()
    video_info_list = test_service.query_risk(time_start, time_end)

    rst = []
    for Gang in video_info_list.GangList:
        name = Gang.Name
        uids = []
        vids = []
        for user_info in Gang.GangUserInfoList:
            _uid = user_info.UserID
            uids.append(_uid)
            for _vid in user_info.VideoItemIDList:
                vids.append(_vid)
        seed_link = 'https://redshield.bytedance.net/Home/Audit/search?type=video&data={}&from=list'.format(
            '%2C%20'.join(map(str, sample(vids, min(10, len(vids))))))
        rst.append({
            'name': name,
            'link': seed_link,
            'uid': uids,
            'vid': vids,
        })
    print('len', len(rst))
    print(rst[:1])
    return rst


if __name__ == '__main__':
    data = get_risk()
