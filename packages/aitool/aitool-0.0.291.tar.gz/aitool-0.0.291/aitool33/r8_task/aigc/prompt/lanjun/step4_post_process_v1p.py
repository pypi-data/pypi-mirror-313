# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, dump_lines, split_char, dump_excel, get_ngrams, term_similar, print_green, print_blue, \
    print_red, is_contains_chinese, rate_chinese


def clean_sentence(case):
    skip_case = {'语言模型', '感谢'}
    skip_piece_contain = {'你好', '您好', '谢谢', '我是', '抖音团队', '尊敬', '嗨', '抖音用户', '一名', '一个问题', '抖音客服',
                  '让我感到', '感到非常', '哎呀', '我真的很', '', '', '', '', '', '', '', '', ''}
    skip_piece_all = {'抖音'}
    case_ngram = set(list(get_ngrams(case, 2, 5)))
    if len(skip_case & case_ngram) > 0:
        return ''
    case = case.split(':')[-1]
    case = case.split('：')[-1]
    case = case.replace('\"', '')
    case = case.replace('“', '')
    case = case.replace('”', '')
    case = case.replace('我认为', '')
    case_pieces = split_char(',，、！。', case)
    choose = []
    for piece in case_pieces:
        if rate_chinese(piece) < 0.7:
            continue
        piece_ngram = set(list(get_ngrams(piece, 1, 7)))
        if len(skip_piece_contain & piece_ngram) > 0:
            continue
        if piece in skip_piece_all:
            continue
        if len(piece) <= 1:
            continue
        choose.append(piece)
    case_clean = '，'.join(choose)
    case_clean = case_clean.strip()
    if len(case_clean) <= 25:
        return ''
    return case_clean


if __name__ == '__main__':
    input_file = [
        '/Users/bytedance/Downloads/prompts_rst_lanjun_t0.3_1205_p0.pkl',
        '/Users/bytedance/Downloads/prompts_rst_lanjun_t0.3_1205_p1.pkl',
        '/Users/bytedance/Downloads/prompts_rst_lanjun_t0.3_1205_p2.pkl',
    ]
    onlyone = False
    sim_th = 0.3
    data = []
    for file in input_file:
        print(file)
        data.extend(load_pickle(file))
    rst_im = []
    rst_ch = []
    head = ['操作', '现象', '操作（同义词替换）', '现象（同义词替换）', '模型输入', '模型输出', '规则相似度']
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
        theme = line[2] + line[3]
        case = line[-1]
        case_clean = clean_sentence(case)
        if len(case_clean) < 15:
            continue
        score_theme = term_similar(case_clean, theme, ngram=2)
        rst_im.append(line[:-1] + [case_clean] + [score_theme])


    head_15 = set()
    rst_im_clean = []
    for line in rst_im:
        text = line[-2]
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

    dump_excel(rst_im, 'rst_lanjun_one_t0.3_1204_ori.xlsx')
    dump_excel(rst_im_clean, 'rst_lanjun_one_t0.3_1204.xlsx')
