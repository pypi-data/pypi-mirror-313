# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, dump_lines, split_char, dump_excel, get_ngram, term_similar, print_green, print_blue, \
    print_red, is_contains_chinese
from aitool.r8_task.aigc.prompt.lanjun.step4_post_process_v1p import clean_sentence

def split_case(text):
    rst = []
    smb = ['\n', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.']
    for s in smb:
        text = text.replace(s, '$$$')
    pieces = text.split('$$$')
    for p in pieces:
        p = p.split(':')[-1]
        p = p.split('：')[-1]
        p = p.strip()
        if len(p) < 5:
            continue
        rst.append(p)
    return rst


input_file = [
    '/Users/bytedance/Downloads/prompts_rst_lanjun_0105_p0.pkl',
    '/Users/bytedance/Downloads/prompts_rst_lanjun_0105_p1.pkl',
    '/Users/bytedance/Downloads/prompts_rst_lanjun_0105_p2.pkl',
]

data = []
for file in input_file:
    print(file)
    data.extend(load_pickle(file))
rst_im = []
rst_ch = []
head = ['操作', '现象', '操作（同义词替换）', '现象（同义词替换）', '模型输入', '模型输出', '规则相似度']
rst_im.append(head)
print_green('以下为输入数据中的第一条数据的摘要，以方便确认')
for r_name, r_value in zip(head, data[0]):
    r_value_c = r_value.replace('\n', ' ')
    if len(r_value_c) > 40:
        r_value_c = r_value_c[:20]+' ... '+r_value_c[-20:]
    print_blue('{}: {}'.format(r_name, r_value_c))
for line in tqdm(data, 'clean'):
    theme = line[2] + line[3]
    ans = line[-1]
    cases = split_case(ans)
    for case in cases:
        case_clean = clean_sentence(case)
        if len(case_clean) < 15:
            continue
        score_theme = term_similar(case_clean, theme, ngram=1)
        if score_theme < 0.5:
            continue
        rst_im.append(line[:-1] + [case_clean] + [score_theme])

head_15 = set()
rst_im_clean = []
for line in rst_im:
    text = line[-2]
    h_text = text[:13]
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

dump_excel(rst_im_clean, 'rst_lanjun_0105.xlsx')
