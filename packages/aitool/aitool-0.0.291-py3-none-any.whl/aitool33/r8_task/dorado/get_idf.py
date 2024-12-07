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
from os import path
from tqdm import tqdm
from aitool import get_ngram_idf, load_csv, dump_lines, DATA_PATH, dict2ranked_list, load_line


def clean_idf_badline(file, separator='\t'):
    # 由于一些特殊字符，导致写文件后出现空行
    idf_list = load_line(file, separator=separator)
    out_list = []
    idf_dict = {}
    count = 0
    for line in tqdm(idf_list, 'load idf dict', delay=5):
        try:
            word, score = line
            idf_dict[word] = float(score)
            out_list.append('{}\t{}'.format(word, score))
        except ValueError:
            count += 1
    print('count', count)
    dump_lines(out_list, file+'_new.txt')


if __name__ == '__main__':
    # 本文件用于生产离线的idf词典
    limit = 10000000
    raw_data = load_csv('/Users/bytedance/Downloads/281475002909830-graph-自动化查询模板-查询2 (1).csv')
    print('len raw_data', len(raw_data))
    data = []
    for line in raw_data[:2000000]:
        choose_line = [line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[12], line[13], line[14],
            line[15], line[16], line[17], line[18], line[20]]
        data.append(' '.join([str(_) for _ in choose_line]))
    print(data[:3])
    # rst = get_ngram_idf(data, split_method='jieba', idf_method='rate', min_gram=1, max_gram=6, all_chinese=True)
    # dump_lines(['{}\t{}'.format(_k, round(_v, 8)) for _k, _v in dict2ranked_list(rst)], path.join(DATA_PATH, 'dorado', 'idf_jieba_rate.txt'))
    # rst = get_ngram_idf(data, split_method='jieba', idf_method='log', min_gram=1, max_gram=6, all_chinese=True)
    # dump_lines(['{}\t{}'.format(_k, round(_v, 8)) for _k, _v in dict2ranked_list(rst)], path.join(DATA_PATH, 'dorado', 'idf_jieba_log.txt'))
    rst = get_ngram_idf(data, split_method='char', idf_method='log', min_gram=1, max_gram=6, all_chinese=False, all_content=True)
    dump_lines(['{}\t{}'.format(_k, round(_v, 8)) for _k, _v in dict2ranked_list(rst)][:limit], path.join(DATA_PATH, 'dorado', 'idf_jieba_log_multilingual.txt'))
    clean_idf_badline(path.join(DATA_PATH, 'dorado', 'idf_jieba_log_multilingual.txt'))
    # rst = get_ngram_idf(data, split_method='char', idf_method='rate', min_gram=2, max_gram=6, all_chinese=True)
    # dump_lines(['{}\t{}'.format(_k, round(_v, 8)) for _k, _v in dict2ranked_list(rst)], path.join(DATA_PATH, 'dorado', 'idf_char_rate.txt'))
    # rst = get_ngram_idf(data, split_method='char', idf_method='log', min_gram=2, max_gram=6, all_chinese=True)
    # dump_lines(['{}\t{}'.format(_k, round(_v, 8)) for _k, _v in dict2ranked_list(rst)], path.join(DATA_PATH, 'dorado', 'idf_char_log.txt'))
