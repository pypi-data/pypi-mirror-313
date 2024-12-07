# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, dump_lines, split_char, dump_excel, get_ngram, term_similar, print_green, print_blue, \
    print_red, is_contains_chinese


def clean(text, thred=0.9):
    rst = []
    smb = ['\n', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.']
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
        if len(p) > 60:
            continue
        if len(p) < 5:
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
        if '不明白' in p:
            continue
        if '什么意思' in p:
            continue
        if '这个' in p:
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
            if len(p) > 20:
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
    '/Users/bytedance/Downloads/prompts_rst_shengxi_1107_p0.pkl',
    '/Users/bytedance/Downloads/prompts_rst_shengxi_1107_p1.pkl',
    '/Users/bytedance/Downloads/prompts_rst_shengxi_1107_p2.pkl',
    '/Users/bytedance/Downloads/prompts_rst_shengxi_1107_p3.pkl',
    '/Users/bytedance/Downloads/prompts_rst_shengxi_1107_p4.pkl',
]
onlyone = False
sim_th = 0.3
data = []
for file in input_file:
    print(file)
    data.extend(load_pickle(file))
rst_im = []
rst_ch = []
head = ['任务', '模板', '规则', '主题', '约束', '例子', '输入', '输出', '规则相似度', '核心规则相似度', '元素']
rst_im.append(head)
print_green('请确认输入文档各列的依次为：任务、模板、规则、主题、约束、例子、输入、输出')
print_green('以下为输入数据中的第一条数据的摘要，以方便确认')
for r_name, r_value in zip(head, data[0]):
    r_value_c = r_value.replace('\n', ' ')
    if len(r_value_c) > 40:
        r_value_c = r_value_c[:20]+' ... '+r_value_c[-20:]
    print_blue('{}: {}'.format(r_name, r_value_c))
for line in tqdm(data):
    task = line[0]
    if task == '用户客服对话':
        rst_ch.append(line)
    else:
        theme_core = line[2].split('-')[-1]
        theme = line[2]
        ans = line[-1]
        meta = '，'.join([_.replace('涉及', '') for _ in line[4].split('，') if '涉及' in _])
        cases = clean(ans, thred=sim_th)
        for case in cases:
            if '这' in case[:4]:
                continue
            if '怎么办' in case:
                continue
            if '如果' in case:
                continue
            if '自动私信' in case:
                continue
            score_theme = term_similar(case, theme, ngram=1)
            score_theme_core = term_similar(case, theme_core, ngram=1)
            rst_im.append(line[:-1] + [case] + [score_theme, score_theme_core, meta])
            if onlyone:
                break

head_15 = set()
rst_im_clean = []
for line in rst_im:
    text = line[-4]
    h_text = text[:15]
    if h_text in head_15:
        continue
    w_cn = 0
    w_all = 0
    for w in text:
        w_all += 1
        if is_contains_chinese(w):
            w_cn += 1
    if w_cn / w_all < 0.7:
        continue
    head_15.add(h_text)
    rst_im_clean.append(line)


dump_excel(rst_im_clean, 'rst_shengxi_1115.xlsx')
