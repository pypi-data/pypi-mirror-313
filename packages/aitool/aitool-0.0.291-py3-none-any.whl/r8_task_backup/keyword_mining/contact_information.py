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
from aitool import get_pinyin, singleton
import re


@singleton
class ContactInformation:
    def __init__(self):
        self.contact_words = [
            '+扣', '加我为朋友', '扫一扫上面的二维码图案', '二维码图案', '茄\/', '要v❤还是要电话', '我滴.徽', '真人茄徵',
            '加我微信聊会吧我的微信号就在下面', '我微信号', '我的微信号', '加个微信吧', 'q群', '我微', '查找帐号', '莪qq', '加我为朋',
            '扫一扫上面的二线(码', '一对一服务指导薇', '硪͇̿徽͇', '微信号', '小可爱薇信', '一下勿扰', '|v:', '取消搜索:', '订座电话:', '徽信',
            '莪...徵', 'q我', '上面连起来02305\/.4244', '茄硪q', '真人【q】', 'qq好友', '敢加就敢聊', '真人茄v', '莪.....徵', '联系微',
            '徽..信:', '<q.q>', '硪qq', '/3的微', '扣扣', '加扣', '加微', '搜索', '勿扰', '家扣', '可约', '联系', '截图', '我ꪜ᥊',
            '偶遇约泡', '约泡', '打开流懒器', 'qq:', '徽↑', '@薇', 'v❤', '十扣', '妹妹徵', '喔得q', '卫信:', '接受私聊', '徵👈🏻', '加wx',
            '十我ᑫᑫ', '↑微', '沃德徽', '+vx', '+薇', '圆兰器打开', '打开流懒嚣', '加v', 'ᑫᑫ', '↑微', '老妹徵', '↑徽', '莪滴徽',
            '6浪器打开', '手机浏览器', '加个微白', '我զզ', '刘岚器打开', '刘岚器', '我𝓆', '6懒器', '我𝐐𝐐', 'ⅴ♥', '我ǫǫ', '✓χ', 'ⅴ♥',
            '加微', '蔻蔻', '茄Q', '伽扣', '+威', 'weixin', '沃得胃', '沃得徵'
        ]
        self.contact_words = [w.lower() for w in set(self.contact_words)]
        self.contact_word_pinyin = [" ".join(get_pinyin(w)) for w in self.contact_words
                               if (2 <= len(w) <= 5 and len(get_pinyin(w)) > 1)]
        self.contact_word_pinyin = set(self.contact_word_pinyin)
        self.contact_word_pinyin.discard("o de")

        # 正则匹配
        # 1 手机号码
        pat = r'(?<=\D)1[34789]\d{9}'
        self.phone_re = re.compile(pat, re.S)

        # 2
        self.qq_re = re.compile(r'[1-9]\d{5,10}', re.IGNORECASE)
        self.wx_re = re.compile(u'^[a-zA-Z]{1}[-_a-zA-Z0-9]{5,19}', re.IGNORECASE)

        # 邮箱 域名
        self.mail = re.compile(r'[1-9]\d{5,10}', re.IGNORECASE)
        self.domain = re.compile(u'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'.encode('utf8'), re.IGNORECASE)

        self.reg_matchers = {}
        self.reg_matchers["phone"] = self.phone_re
        self.reg_matchers["qq"] = self.qq_re
        self.reg_matchers["weixin"] = self.wx_re

        self.pattern_keep = re.compile(r"[^\u4e00-\u9fa5^a-z^A-Z^0-9^\s^\.\@]")

        self.pattern_special_ch = re.compile(r'[-,$#+&*.( )（）  ⃣| ̲̲̅̅͜]')

        ch_set = "".join(list(set(list("lろろちᑴᑴчϭ𝟾ろ☡iб☡ろiらч☡ᑫろчiб☡らᑫчoiчȣчiȣらoᑫiᑫб┐б☡lヿららlбろ☡ヿ☡ら𝚀,ⳅꮞ৪,,7ᒿᒿ,"
                                       "iᑫ.ȣ）（iч.ч┐）（∃∃.i┐）7୨ƽolち☡ち𝟾9чろчбちiろ☡б┐i┐☡бȣilちろᑴ𝟾lちちろlllろ☡lϭ𝟾☡ヿliᑫ8ч☡ろбち7i "
                                       "iб☡ろiらч☡ᑫろчiб☡ろiらч☡i┐чiヿiヿiろ𝙊ろろ𝙊чlヿбoろolᑴヿᑴろlろбら8ヿ4☡ら4б☡𝟏𝟕𝟴𝟯𝟳𝟲𝟳𝟵𝟮5"
                                       "（i∃.i）（бᑫ.┐∃）（ら☡.i∃）ιちろㄐろoㄐろちろշ🅵🆆🅺➀➁➂➃➄➅➆➇➈➉➊➋➌➍➎➏➐➑➒➓iららろヿ"
                                       "，1️⃣ヿб8️⃣8️⃣ろ0️⃣ろ1️⃣чらら☡ᑴヿi𝙊lろoら8ろヿбo4ᑴ11️⃣ヿб8️⃣8️⃣ろ0️⃣ろ1️⃣чらi.ȣ.ら.ら.i.0.ȣ.2"
                                       ".0.ろ.7"))))

        self.pattern_special_ch_num = re.compile(r'[{}\d]+'.format(ch_set))

        self.pattern_mis_recall_word = re.compile(r'同城热榜|微笑|微小|好友小')

        self.pattern_douyin_account = re.compile(r'[抖音|剪映|剪影|tiktok|ID|快手][号]{0,2}.{0,2}[\d|a-zA-Z]{1,20}')

    def text_inference(self, text):
        text = str(text)
        contact_word_matched = []
        other_word_matched = []
        for w in self.contact_words:
            if w in text:
                contact_word_matched.append(w)

        text_for_pinyin = re.sub(self.pattern_mis_recall_word, ' ', text)

        text_pinyin = " ".join(get_pinyin(text_for_pinyin))

        for py in self.contact_word_pinyin:
            if py in text_pinyin:
                contact_word_matched.append("p#" + py)

        # clean text in different ways.
        text_cleaned = text
        for pattern in [self.pattern_keep, self.pattern_special_ch]:

            text_cleaned = re.sub(pattern, '', text_cleaned)

            # remove all douyin account in all case
            text_cleaned = re.sub(self.pattern_douyin_account, ' ', text_cleaned)

            for w in self.contact_words:
                if w not in contact_word_matched and w in text_cleaned:
                    contact_word_matched.append(w)

            phone_nums = self.phone_re.findall(text_cleaned)
            qq_nums = self.qq_re.findall(text_cleaned)
            weixin_nums = self.wx_re.findall(text_cleaned)

            for num in set(phone_nums + qq_nums + weixin_nums):
                num = num.replace(".", "")
                if len(num) >= 5:
                    #                     if len(num.replace(".","")) < 5:
                    #                         continue
                    # contact_word_matched.extend(ls)
                    num = num.strip(".,（）()，")
                    other_word_matched.append(num)

        # phone number with special character, contains japanese etc.
        text_remove_self_account = re.sub(self.pattern_douyin_account, ' ', text)

        special_num = re.findall(self.pattern_special_ch_num, text_remove_self_account)
        if len(special_num) > 0:
            for num in special_num:
                num = num.strip().replace(" ", "").replace(".", "")
                if num.isdigit():
                    continue
                num = num.strip('.,（）()，')
                if len(num) >= 5 and len(num) < 20 and num not in contact_word_matched:
                    other_word_matched.append(num)
        other_word_matched = list(set(other_word_matched))

        return other_word_matched


def get_contact(text):
    c = ContactInformation()
    return c.text_inference(text)


if __name__ == '__main__':
    print(get_contact('那你呢，夜晚 抖音号 weihaolni132132  剪映号 weihaolni132132 我wei：ᑴчϭ𝟾ろ☡iб☡ろiらч'))
    print(get_contact('我的手机号是+1118235201357'))