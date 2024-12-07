# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from tqdm import tqdm
from aitool import load_pickle, get_chinese, split_char, dump_excel, get_ngram, term_similar, print_green, print_blue, \
    is_all_chinese, delete_char, split_punctuation
from aitool.r8_task.aigc.prompt.lanjun.step4_post_process_v1p import clean_sentence

input_file = [
    '/Users/bytedance/Downloads/card_task_name_2023_12_22_22_58.rst.p0.pkl',
]

data = []
for file in input_file:
    print(file)
    data.extend(load_pickle(file))
rst_im = []
rst_ch = []
rst = []
rst.append([''] + ['名称'])
for text, input, output in data:
    names = split_punctuation(output)
    clear_names = []
    for name in names:
        name = delete_char(name, {'【', '】', '《', '》', ' '})
        name = get_chinese(name)
        if len(name) <= 1:
            continue
        if len(name) >= 6:
            continue
        clear_names.append(name)
    if len(clear_names) == 0:
        continue
    rst.append([text] + clear_names)
dump_excel(rst, '生成_用户描述2名称.xlsx')
