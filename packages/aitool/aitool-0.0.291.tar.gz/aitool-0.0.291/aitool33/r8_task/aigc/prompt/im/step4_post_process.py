# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, dump_lines, split_char, dump_excel, get_ngram, term_similar


def clean(text, thred=0.9):
    rst = []
    smb = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.']
    for s in smb:
        text = text.replace(s, '$$$')
    pieces = text.split('$$$')
    for p in pieces:
        ori = p
        p = p.strip()
        if '地说' in p:
            continue
        if '推荐' in p:
            continue
        if '离线反馈' in p:
            continue
        if len(p) < 25:
            continue
        if '语言模型' in p:
            continue
        if '我感到非常' in p:
            continue
        if '我真的很生气' in p:
            continue
        if '我非常生气' in p:
            continue
        if '是一个' in p:
            continue
        if '是一名' in p:
            continue
        if '作为一个' in p:
            continue
        if '作为一名' in p:
            continue
        if '数据集' in p:
            continue
        if '请按照如下格式提供问题' in p:
            continue
        if '反馈' in p:
            continue
        if '！！！！' in p:
            continue
        if '客服' in p:
            continue
        if p[-1] in (',', ':', ';', '，', '：', '；'):
            continue
        p = p.replace('\"', '')
        p = p.replace('“', '')
        p = p.replace('”', '')
        p = p.replace('哎呀，', '')
        p = p.replace('hi，', '')
        p = p.replace('嘿，', '')
        p = p.replace('哦，', '')
        p = p.replace('嗨，', '')
        p = p.replace('天哪，', '')
        p = p.replace('用户ID', '')
        p = p.replace('哇塞', '')
        if p[:2] == '抖音':
            continue
        if p[:3] == '我真的':
            continue
        if '\n' in p:
            p = p.replace('\n\n', '')
            head = ['内容:', '内容：', '反馈:', '反馈：']
            for k in p.split('\n'):
                for h in head:
                    if h in k:
                        kp = k.split(h)[1]
                        if len(kp) > 10:
                            rst.append(kp.strip())
                            break
        else:
            head = ['内容:', '内容：', '反馈:', '反馈：']
            for h in head:
                if h in p:
                    p = p.split(h)[1]
                    break
            if len(p) > 10:
                rst.append(p.strip())
    # get sim
    select = []
    for p in rst:
        max_sim = 0
        for q in select:
            sim = term_similar(p, q)
            if sim > max_sim:
                max_sim = sim
        if max_sim <= thred:
            select.append(p)
    return select


input_file = [
    '/Users/bytedance/Downloads/prompts_rst_0913_p0.pkl',
    '/Users/bytedance/Downloads/prompts_rst_0913_p4.pkl',
]
onlyone = True
sim_th = 0.3
data = []
for file in input_file:
    print(file)
    data.extend(load_pickle(file))
rst_im = []
rst_ch = []
for line in tqdm(data):
    task = line[0]
    if task == '用户客服对话':
        rst_ch.append(line)
    else:
        ans = line[-1]
        cases = clean(ans, thred=sim_th)
        for case in cases:
            rst_im.append(line[:-1] + [case])
            if onlyone:
                break

dump_excel(rst_im, 'rst_im_0913.xlsx')
