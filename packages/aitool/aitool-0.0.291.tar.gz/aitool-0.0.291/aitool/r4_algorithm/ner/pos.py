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
        if self.method == 'jieba':
            import jieba.posseg as psg
            self.pos = psg.cut
        else:
            import jieba.posseg as psg
            self.pos = psg.cut

    def get_pos(self, text):
        if self.method == 'jieba':
            # jieba中词性的定义：https://gist.github.com/hscspring/c985355e0814f01437eaf8fd55fd7998
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


if __name__ == '__main__':
    data = [
        '你们这是什么鬼',
        '手机相册是空的，照片早已删除',
        '我手机格式化过',
        '有关证件我在手机相册里',
        '我的摄像头权限一直是关闭的',
    ]
    x = POSFilter()
    for d in data:
        print(d)
        print(x.get_pos(d))

