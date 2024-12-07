# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, dump_lines, split_char, dump_excel, get_ngram, term_similar, print_green, print_blue, \
    print_red, is_contains_chinese, cut_until_char
from aitool.r8_task.aigc.prompt.lanjun.step4_post_process_v1p import clean_sentence

input_file = [
    '/Users/bytedance/Downloads/card_task_2023_12_22_22_30.rst.p0.pkl',
    '/Users/bytedance/Downloads/card_task_2023_12_22_22_30.rst.p1.pkl',
    '/Users/bytedance/Downloads/card_task_2023_12_22_22_30.rst.p2.pkl',
    '/Users/bytedance/Downloads/card_task_2023_12_22_22_30.rst.p3.pkl',
    '/Users/bytedance/Downloads/card_task_2023_12_22_22_30.rst.p4.pkl',
]

rank_name = [
    '角色卡',
    '魔法卡',
    '陷阱卡',
    '攻击力',
    '生命值',
    '有单体伤害随从的能力',
    '给一个己方随从+x生命 (1~12)',
    '对所有敌方随从造成x点伤害 (1~10)',
    '全体加x生命',
    '全体加x生命',
    '造成x点伤害 (1~10)',
    '造成x点治疗 (1~20)',
    '造成2倍攻击力的伤害',
    '给一个己方随从+x攻击 (1~12)',
    '全体加x攻击力',
    '给一个己方随从+x生命 (1~12)',
    '法强+x ()',
    '抽x张牌 (1~5)',
    '无效正在发动的魔法/陷阱卡效果',
    '嘲讽',
    '使选定随从变为其【幻象】',
]

data = []
for file in input_file:
    print(file)
    data.extend(load_pickle(file))
rst_im = []
rst_ch = []
rst = []
rst.append(['text'] + rank_name)
for text, input, output in data:
    scores = []
    scores.append(text)
    output.replace('\'', '')
    pieces = output.split('\n')
    if len(pieces) != 22:
        continue
    try:
        for po in pieces:
            rm_ch = ''
            for c in po:
                if is_contains_chinese(c):
                    continue
                else:
                    rm_ch += c
            po = rm_ch.strip()
            p = cut_until_char(po)
            p = p.replace('；', '')
            p = p.replace('。', '')
            p = p.replace(' ，', '')
            p = p.strip()
            items_1 = p.split(' ')
            items_2 = split_char('，,:：、为', items_1[-1])
            s = items_2[-1].strip()
            scores.append(float(s))
        rst.append(scores)
    except Exception as e:
        continue

dump_excel(rst, '生成_用户描述2分数.xlsx')
