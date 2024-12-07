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
import re
from aitool import pip_install, is_all_chinese, singleton, exe_time


@singleton
class POSFilter:
    def __init__(self, method='jieba'):
        self.method = method
        if self.method == 'text_cutter':
            # todo 依赖的内部包text_cutter在mac上执行会报错，只能在线上环境执行
            # todo text_cutter在多进程时会出错
            print('Init POSFilter')
            try:
                import text_cutter
            except ModuleNotFoundError as e:
                pip_install('https://luban-source.byted.org/repository/scm/search.nlp.libcut_py_2.3.0.52.tar.gz')
                import text_cutter
            self.cutter = text_cutter.load('libcut/zh_v19')
            self.pos = text_cutter.load('pos/zh_20201212_conv')
        elif self.method == 'jieba':
            import jieba.posseg as psg
            self.pos = psg.cut
        else:
            import jieba.posseg as psg
            self.pos = psg.cut

    def get_pos(self, text):
        if self.method == 'text_cutter':
            text = re.sub('@.*?[ ,.?!，。？！]', ' ', text)
            words_s, words_l = self.cutter.segment(text)
            word_valid = []
            word_pos = self.pos.pos(words_l)
            word_pos = [val[2] for val in word_pos if len(val[1]) == 1]
            return word_pos
        elif self.method == 'jieba':
            # jieba中词性的定义：https://gist.github.com/hscspring/c985355e0814f01437eaf8fd55fd7998
            word_pos = list(self.pos(text))
            word_pos = [(_.word, _.flag) for _ in word_pos]
            return word_pos
        else:
            word_pos = list(self.pos(text))
            word_pos = [(_.word, _.flag) for _ in word_pos]
            return word_pos

    def is_pos_valid(self, text, show_detail=False, target=None, vv=None, ths_target=0.63, ths_vv=0.71):
        if target is None:
            # jieba中词性的定义：https://gist.github.com/hscspring/c985355e0814f01437eaf8fd55fd7998
            target = ['NR', 'NT', 'NN', 'VV', 'n', 'ng', 'nr', 'nrfg', 'nrt', 'ns', 'nt', 'nz',
                      'r', 'rg', 'rr', 'rz', 'v', 'vd', 'vg', 'vi', 'vn', 'vq']
        if vv is None:
            vv = ['VV', 'v', 'vd', 'vg', 'vi', 'vn', 'vq']
        if show_detail:
            print('target', target)
            print('vv', vv)
            print('ths_target', ths_target)
            print('ths_vv', ths_vv)

        word_pos = self.get_pos(text)

        pos_count = len(word_pos)
        if pos_count == 0:
            return False

        target_count = 0
        vv_count = 0
        for p in word_pos:
            if p in target:
                target_count += 1
            if p in vv:
                vv_count += 1

        target_score = target_count / pos_count
        vv_score = vv_count / pos_count
        print(text, target_score, vv_score)
        if target_score >= ths_target and vv_score <= ths_vv:
            if show_detail:
                print(text, 'True', target_score, vv_score, word_pos)
            return True
        else:
            if show_detail:
                print(text, 'False', target_score, vv_score, word_pos)
            return False


def is_pos_valid(text, method='jieba', **kwargs):
    if text in {'我会', '没人', '不想', '你好', '谢谢', '希望抖音', '平台给我', '大人给我', '好好改正', '导致账号', '给予我账号',
                '希望官方', '官方您好', '抖音爸爸', '谢谢抖音', '希望工作人员', '审核员大人', '感谢抖音', '平台给我', '大人给我',
                '官方审核员大人', '非常感谢审核员', '请求官方', '大人给我一次机会', '深刻体会', '官方给我', '违反了抖音', '希望平台',
                '恳请官方', '体会到失误', '深刻体会到失误', '审核员大人给我', '尊敬的审核', '认真学习平台', '遵守平台',
                '认真学习抖音', '抖音是正能量', '谢谢官方', '能量视频', '工作人员能给我', '情况下导致', '希望工作人员能给我',
                '不知情的情况下导致', '官方给予', '抖音是一个正能量', '抖音平台的优质', '万分感谢', '我会好好', '原因导致',
                '平台给予', '工作人员您好', '给我提供', '不符合社区', '抖音给我提供', '感谢抖音给我', '平台希望',
                '谢谢抖音的工作人员', '请问抖音', '官方再给我', '客服你好', '给我解决', '感谢官方', '平台希望抖音',
                '尊敬的抖音审核', '尊敬的审核员', '抖音工作人员您好', '尊敬的审核人员', '抖音审核人员', '恳请审核员',
                '官方再给我一次机会', '维护抖音', '规则的事', '取消抖音', '审核员您好', '平台给次', '官方爸爸', '我会好好珍惜',
                '希望平台给我', '平台给次机会', '平台再给我', '给我一次改过', '人员您好', '希望领导', '谢谢抖音官方',
                '你好我知道抖音', '不做违反社区规则', '审核员给予我账号', '导致了账号', '请求审核员', '大人给予', '请求平台',
                '给予一次机会', '官方审核员给予', '请求审核员给予', '审核人员您好', '麻烦帮忙', '感谢平台', '这一误导',
                '视频抖音是正能量', '努力的人一次机会', '希望能给我', '没有擦边这一误导', '误导的视频', '没有擦边这一',
                '也许我在学习', '道路上触及', '大人给予我账号', '审核员大人给予', '非常感谢抖音官方', '提供这么好的正能量',
                '照片类都没有擦边', '误导的视频抖音', '这一误导的视频', '道路上触及到了平台', '抖音官方是会珍惜',
                '官方是会珍惜每一位', '平台能给我', '违反了平台', '好好去珍惜', '机会将账号恢复正常', '抖音规则导致', '平台带来',
                '肯定会好好去珍惜', '努力发正', '你好官方', '抖音带给', '带来的麻烦我感到', '平台里展现', '希望客服', '抖音我会',
                '亲爱的尊敬', '希望抖爸爸', '理解抖音', '机会解封', '保证会认真仔细', '好不容易积累', '熟知社区', '爸爸给我',
                '人员你好', '导致抖音', '乐趣的平台', '发布了一条', '希望官方给予', '我想请问', '抖音大人', '抖音去表达',
                '抖音官方给我', '珍惜这个账号努力', '账号努力', '账号努力发正', '视频谢谢抖音', '导致了我的账号', '普普通通的抖音',
                '一名普普通通', '普普通通的抖音用户', '抖音的热爱我一直不离', '审核人员你好', '请问官方', '美好生活抱歉',
                '做出更加合适', '求求官方', '提供了这么好的正能量', '原因涉嫌', '给予账号', '账号于近日', '申请抖音', '优秀的平台',
                '抖音这个优秀', '碰到了平台', '喜欢抖音这个优秀', '审核大大您好', '请求官方帮忙', '请求你们再给我', '给我机会',
                '携手共同维护', '希望给一次机会', '感受到了国家', '抖音感受到了国家', '抖音为伴', '给我账号', '官方工作人员',
                '对不起官方', '其他用户带来', '抖音平台是一个值得', '平台是一个值得', '平台是一个值得信赖', '希望平台给予',
                '尊敬的审核大大您好', '深刻地感受到我的错误', '感受到我的错误', '深刻地感受', '给我带来', '我会遵守', '保证下次',
                '保证以后好好', '渴望日后', '减轻家庭', '抖音官方会珍惜', '抖音团队', '平常都会利用空闲', '希望可以解封',
                '谢谢抖音平台', '严格遵守平台', '失误触碰到了平台', '满满的的短视频平台', '无知和失误触碰到', '给我推送', '官方添麻烦',
                '感谢抖音这个平台', '官方会珍惜每一位', '今日打开', '请问我的账号', '抖音平台你好', '希望您能给我一次改过', '机会谢谢',
                '审核人员给正在努力', '坚信自己并没有违反', '我要申请', '过得机会', '时间来刷刷', '时间来刷刷抖音', '给我一次改正',
                '抖音官方添麻烦', '喜欢这个平台', '发生符合抖音', '政策的时候抖音', '求求抖音', '带来的娱乐', '大人在给我',
                '官方大人在给我', '给我一次改正的机会', '抖音的机会', '为啥给我', '诚心来过得', '诚心来过得机会'
                }:
        return False
    if text[:2] in {'不到'}:
        return False
    if len(text) >= 8:
        return False
    # 有3个以上相同的字
    if len(text) - len(set(text)) >= 2:
        return False
    # 包含特殊的词，例如破折号
    # 有称谓词的直接删除，例如你我他
    ew = ['一一', '你', '我', '他', '她']
    for w in ew:
        if w in text:
            return False
    # 短词直接通过
    if len(text) <= 3:
        return True
    pos_filter = POSFilter(method=method)
    pos_result = pos_filter.is_pos_valid(text, **kwargs)
    return pos_result


@exe_time(print_time=False)
def filter_words_with_pos(words, method='jieba', **kwargs):
    rst = []
    for word in words:
        if is_pos_valid(word, method=method, **kwargs):
            rst.append(word)
    return rst


if __name__ == '__main__':
    from aitool import load_excel
    # pos_filter = POSFilter(method='jieba')
    # print(pos_filter.get_pos('5月24日疫情专项：孙春兰指导北京防疫强调“动态清零”、网传社区不让回家特斯拉工人睡工厂地板'))
    bad = ['也没有涉及到', '给我选择', '但是我的意思', '他说不清楚', '别人看不到', '你听能听明白', '事是吗', '不会收取',
           '你知道', '我想咨询', '不到美化', '什么意思', '可能认识']
    good = ['医疗美容', '申诉失败', '医疗健康广告', '账号封禁', '涉嫌违规', '职业认证', '医疗作品', '团购外卖',
            '外卖到家相关', '软件服务费', '平台配送', '外卖扣点', '外卖服务商', '外卖佣金', '修改肤色', '伴奏的声音',
            '没有搜索功能', '上传就找不到', '拍摄视频', '浏览和访客', '减少推荐', '抖音访客', '记录功能']
    case = ['孙春兰', '网传', '特斯拉', '工人睡工厂', '工人睡工厂地板', '特斯拉工人',
            '社区不让', '孙春兰指导', '网传社区', '孙春兰指导北京', '指导北京防疫', '指导北京', '不让回家特斯拉工人', '工厂地板', '北京防疫',
            '疫情专项', '动态清零', '特斯拉工人睡工厂']
    bug = ['找不到实际生活', '找不到该作者', '找不到我关注的账号', '找不到我粉丝的账号', '', '', '', '', '']
    # print(filter_words_with_pos(bad))
    # print(filter_words_with_pos(good))
    # print(filter_words_with_pos(case))
    print(filter_words_with_pos(bug, show_detail=True))
