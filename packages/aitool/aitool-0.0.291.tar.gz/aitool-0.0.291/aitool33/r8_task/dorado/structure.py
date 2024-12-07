# -*- coding: UTF-8 -*-


class User:
    def __init__(self):
        self.id = 0
        self.user_create_days = 0
        self.status = None
        self.is_fake_user = None
        self.is_canceled = None
        self.city_resident = None
        self.publish_cnt_30d = None
        self.dist_device_id_90d = set()
        self.dist_ip_90d = set()
        self.dist_location_90d = set()
        # relation
        self.report = []
        self.report_status = None
        self.object = set()
        self.cmt = []
        self.msg = []


class Obj:
    def __init__(self):
        self.id = 0
        self.type = 0
        # relation
        self.user = None
        self.report = []


class Report:
    def __init__(self):
        self.type = 0
        self.msg = ''
        self.time = 0
        self.status = 0
        # relation
        self.user = None  # 举报人
        self.obj = None


class Comment:
    def __init__(self):
        self.hash = 0
        self.text = 0
        self.time = 0
        # relation
        self.user = None
        self.obj = None


class Message:
    def __init__(self):
        # 私信拿不到内容所以没有做hash的必要
        self.word = set()
        self.time = 0
        # relation
        self.device = None
        self.user = None
        self.to_user = None
        self.follow_type = None  # 目前没有建到User上


class Device:
    def __init__(self):
        self.id = 0
        # relation
        self.user = set()


class Ip:
    def __init__(self):
        self.id = 0
        # relation
        self.user = set()
