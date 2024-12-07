# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, dump_lines, split_char, dump_excel, get_ngram, load_lines


def term4_similar(text1, text2):
    s1 = set(list(get_ngram(text1, ngram=2)))
    s2 = set(list(get_ngram(text2, ngram=2)))
    sim = len(s1 & s2) / min(len(s1), len(s2))
    return sim


def clean(text, thred=0.9):
    rst = []
    # smb = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '\"', '“', '”']
    smb = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '\n']
    for s in smb:
        text = text.replace(s, '$$$')
    pieces = text.split('$$$')[1:]
    for p in pieces:
        if len(p.strip()) < 10:
            continue
        rst.append(p.strip())

    # get sim
    select = []
    for p in rst:
        max_sim = 0
        for q in select:
            sim = term4_similar(p, q)
            if sim > max_sim:
                max_sim = sim
        if max_sim <= thred:
            select.append(p)
    return select


# input_file = [
#     '/Users/bytedance/Downloads/risk_rst/prompts_rst_1023_p0 (1).pkl',
# ]
from aitool import get_file
input_file = list(get_file('/Users/bytedance/Downloads/risk_rst/'))

onlyone = True
sim_th = 0.3
data = []
for file in input_file:
    print(file)
    for line in load_pickle(file):
        if line[0] not in ('不适合收录', '低俗', '国内领导人', '时政', '未成年色情', '色情', '违反公序良俗', '违法违规'):
            continue
        data.append(line)

rst = []
for line in tqdm(data):
    idx = line[0]
    query = line[2]
    ans = line[-1]
    cases = clean(ans, thred=sim_th)
    for case in cases:
        case = case.replace('\"', '')
        rst.append([idx, query, case])

from random import shuffle
shuffle(rst)
rst = sorted(rst, key=lambda x: (x[0], x[1]))

dump_lines(rst, 'eval_1027.txt')
dump_excel(rst, 'eval_1027.xlsx')
