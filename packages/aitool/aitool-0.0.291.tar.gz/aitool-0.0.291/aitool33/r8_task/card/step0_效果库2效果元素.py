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
from aitool import load_excel, get_chinese, dump_excel, timestamp
from collections import defaultdict


# x/x 手动改掉
erp = load_excel('./物料/卡牌效果库_20231222.xlsx', to_list=True)
text = []
typ2name = {0: '随从', 1: '魔法', 2: '陷阱'}
typ_list = list(typ2name.keys())
typ_list.sort()
mechanism = ['无', '拦截', '埋伏', '战吼', '光环']
ability2key = {
    '嘲讽': ['嘲讽', ],
    '抽x张牌 (1~5)': ['抽张牌'],
    '对所有敌方随从造成x点伤害 (1~10)': ['对所有敌方随从造成点伤害'],
    '对选定随从造成x点伤害 (1~15)': ['对选定随从造成点伤害'],
    '法强+x ()': ['法强加', ],
    '无效正在发动的魔法/陷阱卡效果': ['无效正在发动的魔法陷阱卡效果', ],
    '造成2倍攻击力的伤害': ['造成倍攻击力的伤害', ],
    '使选定随从变为其【幻象】': ['使选定随从变为其幻象', ],
    '造成x点伤害 (1~10)': ['造成点伤害'],
    '造成x点治疗 (1~20)': ['造成点治疗'],
    '给一个己方随从+x攻击 (1~12)': ['给一个己方随从加攻击', ],
    '给一个己方随从+x生命 (1~12)': ['给一个己方随从加生命', ],
    '无效果': ['无效果', ],
    '召唤1个x/x的随从 (1~9)': ['召唤个的随从', ],
    '全体加1/1': ['全体加', ],
    '全体加x生命': ['全体加生命', ],
    '全体加x攻击力': ['全体加攻击力', ],
}
ability_list = list(ability2key.keys())
ability_list.sort()

key2ability = {}
for k, v in ability2key.items():
    for vi in v:
        key2ability[vi] = k

rst = defaultdict(set)
both = defaultdict(set)
both_case = defaultdict(set)
bad_line = []
for line in erp:
    desc = line[6]+line[11]
    desc = desc.replace('+', '加')  # 先手动将 + 全改为加
    typ = line[9]
    all_skill = []
    for text in desc.split(','):
        mec = '无'
        if ':' in text:
            mec, text = text.split(':')
        mec = get_chinese(mec)
        if mec not in mechanism:
            bad_line.append(text)
            continue
        for piece in text.split('、'):
            piece = get_chinese(piece)
            if piece not in key2ability:
                bad_line.append(piece)
                continue
            abl = key2ability[piece]
            rst[(mec, abl)].add(int(typ))
            all_skill.append(abl)
    for abl_1 in all_skill:
        for abl_2 in all_skill:
            if abl_1 != abl_2:
                both[abl_1].add(abl_2)
                both[abl_2].add(abl_1)
                both_case[(abl_1, abl_2)].add(line[5])
print('异常数据:')
for line in bad_line:
    print(line)

output_1 = [[''] + mechanism]
for abl in ability_list:
    line = [abl]
    for mec in mechanism:
        tpys = []
        for typ in typ_list:
            if typ in rst[(mec, abl)]:
                tpys.append(typ2name[typ])
        tpys_str = '，'.join(tpys)
        line.append(tpys_str)
    output_1.append(line)
output_1.append(['攻击 (0~15)', '随从'])
output_1.append(['生命 (1~15)', '随从'])

output_2 = [['共现'] + ability_list]
for abl in ability_list:
    line = [abl]
    for ab in ability_list:
        if ab in both[abl]:
            line.append('Y')
            if ab == abl:
                tmp = both_case[(ab, ab)]
                print('same')
        else:
            line.append('')
    output_2.append(line)

dump_excel({'技能': output_1, '共现': output_2}, './物料/卡牌效果元素_{}.xlsx'.format(timestamp(style='day')))
