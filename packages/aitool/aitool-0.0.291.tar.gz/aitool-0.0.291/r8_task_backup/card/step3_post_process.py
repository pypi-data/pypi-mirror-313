# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, dump_lines, split_char, dump_excel, get_ngram, term_similar, print_green, print_blue, \
    print_red, is_contains_chinese
from aitool.r8_task.aigc.prompt.lanjun.step4_post_process_v1p import clean_sentence

input_file = [
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p0.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p1.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p2.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p3.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p4.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p5.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p6.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p7.pkl',
    '/Users/bytedance/Downloads/prompts_rst_card_1219_p8.pkl',
]

data = []
for file in input_file:
    print(file)
    data.extend(load_pickle(file))
rst_im = []
rst_ch = []
text2task = {
    '请设计出1种卡牌特效，包括特效名称和相关说明': '特效名称+效果描述',
    '】写出该特效的相关说明': '效果描述',
    '张卡牌的设计原型、形象特点、特质等信息': '卡牌描述',
    '请做出一张新卡的身材': '身材',
    '卡牌类型、卡牌背景、卡牌效果、卡牌名称': '描述+身材+名称',
}
rst = [['task', '模型输入', '模型输出']]
for line in tqdm(data, 'clean'):
    input, output = line
    tag = ''
    for k in text2task:
        if k in input:
            tag = text2task[k]

    rst.append([tag, input, output])
dump_excel(rst, 'rst_card_1219.xlsx')
