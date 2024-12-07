# -*- coding: UTF-8 -*-
# Copyright©2020 xiangyuejia@qq.com All Rights Reserved
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
词级别的文本操作
"""
import os
import warnings
import logging
import re
from typing import Dict, Union, List, Any, NoReturn
from aitool import DATA_PATH
from aitool import is_file_exist, load_lines, load_json
from aitool import prepare_data
from aitool import is_contains_english, cut_until_char, delete_char, is_contains_figure, is_contains_chinese, \
    is_all_chinese, singleton, pip_install, print_yellow


def is_nick_name(text: str) -> bool:
    """
    是否是昵称

    :param text: 文本
    :return: 是否是昵称

    >>> is_nick_name('老王')
    True
    >>> is_nick_name('王总')
    True
    """
    nick_name_prefix = {'大', '女', '小', '男', '老', '阿'}
    nick_name_postfix_relation = {'哥', '姐', '总'}
    nick_name_postfix_num = {'一', '丁', '七', '三', '丙', '乙', '九', '二', '五', '八', '六', '十', '四', '壬', '己', '庚',
                             '戊', '甲', '癸', '辛'}
    if len(text) == 2:
        if text[0] in nick_name_prefix:
            return True
        if text[1] in nick_name_postfix_relation:
            return True
        if text[0] in nick_name_postfix_num or text[1] in nick_name_postfix_num:
            return True
    if len(text) == 3:
        if text[2] in nick_name_postfix_relation:
            return True
        if text[0] in nick_name_postfix_num and text[1] in nick_name_postfix_num:
            return True
    return False


@singleton
class NLTK:
    def __init__(self):
        try:
            import nltk
        except ModuleNotFoundError:
            print_yellow(
                """如果下面的指令卡很久请尝试手动执行：
                import nltk
                nltk.download('punkt')
                nltk.download('averaged_perceptron_tagger')
                nltk.download('wordnet')
                """
            )
            pip_install('nltk')
            import nltk

        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')


def get_wordnet_pos(tag: str) -> Any:
    """
    将nltk的pos按ADJ、VERB、NOUN、ADV

    :param tag: nltk的pos
    :return: ADJ、VERB、NOUN、ADV 或 None
    """
    NLTK()
    from nltk.corpus import wordnet

    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def get_word_prototype(word: str) -> str:
    """
    获取单词的原形

    :param word: 单词
    :return: 单词的原形

    >>> get_word_prototype('tried')
    'try'
    >>> get_word_prototype('books')
    'book'
    """
    NLTK()
    from nltk import word_tokenize, pos_tag
    from nltk.corpus import wordnet
    from nltk.stem import WordNetLemmatizer

    tokens = word_tokenize(word)
    tagged_sent = pos_tag(tokens)  # 获取单词词性

    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))  # 词形还原

    return lemmas_sent[0]


chinese_family_name = set()
File_Bag = ['', os.path.join(DATA_PATH, 'r4_nlp', 'words')]
File_Chinese_Family_Name = os.path.join(DATA_PATH, 'r4_nlp', 'words', 'Names', 'Chinese_family_name.txt')


def has_family_name(name: str) -> bool:
    """

    :param name:
    :return:

    >>> has_family_name('项羽')
    >>> has_family_name('翼德')
    """
    if not chinese_family_name:
        if not is_file_exist(File_Chinese_Family_Name):
            prepare_data(*File_Bag, packed=True)
        for item in load_lines(File_Chinese_Family_Name):
            chinese_family_name.add(item)
    if len(name) > 0 and name[0] in chinese_family_name:
        return True
    return False


word_common = set()
DIR_THUOCL = os.path.join(DATA_PATH, 'r4_nlp', 'words', 'THUOCL')
FILE_XINHUA_CI = os.path.join(DATA_PATH, 'r4_nlp', 'words', 'XINHUA', 'ci.json')


def init_word_common(threshold: int = 10) -> NoReturn:
    if not is_file_exist(DIR_THUOCL) or not is_file_exist(FILE_XINHUA_CI):
        prepare_data(*File_Bag, packed=True)
    files = os.listdir(DIR_THUOCL)
    for file in files:
        with open(os.path.join(DIR_THUOCL, file), 'r') as fin:
            for line in fin:
                w, f = line.strip().split('\t')
                if eval(f) > threshold:
                    word_common.add(w)
    data = load_json(FILE_XINHUA_CI)
    for line in data:
        word_common.add(line['ci'])


def is_common_word(text: str) -> bool:
    """

    :param text:
    :return:

    >>> is_common_word('汽车')
    >>> is_common_word('唐三')
    """
    if not word_common:
        init_word_common()
    if text in word_common:
        return True
    return False


def get_common_word():
    if not word_common:
        init_word_common()
    return word_common


word_stop = set()
FILE_STOPWORDS = os.path.join(DATA_PATH, 'r4_nlp', 'words', 'stopwords.txt')


def init_word_stop() -> NoReturn:
    if not is_common_word(FILE_STOPWORDS):
        init_word_common()
    with open(FILE_STOPWORDS, 'r') as fin:
        for line in fin:
            word = line.strip()
            word_stop.add(word)
            for w in word:
                word_stop.add(w)


def is_stop_word(text: str) -> bool:
    """

    :param text:
    :return:

    >>> is_stop_word('的')
    >>> is_stop_word('匿')
    """
    if not word_stop:
        init_word_stop()
    if text in word_stop:
        return True
    return False


def get_stop_word():
    if not word_stop:
        init_word_stop()
    return word_stop


relationship_title = {}
FILE_RELATIONSHIP = os.path.join(DATA_PATH, 'r4_nlp', 'words', 'Names', 'relationship.txt')


def init_relationship_title() -> NoReturn:
    if not is_file_exist(FILE_RELATIONSHIP):
        prepare_data(*File_Bag, packed=True)
    relationship_title_addition = {'店长', '法师', '醫生', '大力士', '护士', '父亲', '天后', '教练', '保安', '计师', '管事',
                                   '知事', '道长', '妃', '母亲', '头目', '乞丐', '妻', '局长', '官员', '', '', '', '', '',
                                   '', '', '', '', '', '', '', '', '', '', '', '', '', ''}
    data = set(load_lines(FILE_RELATIONSHIP)) | relationship_title_addition
    for item in data:
        item_len = len(item)
        if item_len not in relationship_title:
            relationship_title[item_len] = set()
        relationship_title[item_len].add(item)


def get_relationship_title():
    if not relationship_title:
        init_relationship_title()
    return relationship_title


def is_relationship_title(text: str) -> bool:
    """
    >>> is_relationship_title('张老师')
    >>> is_relationship_title('唐三')

    :param text:
    :return:
    """
    if not relationship_title:
        init_relationship_title()
    text_len = len(text)
    for title_len, title_items in relationship_title.items():
        if title_len + 1 != text_len:
            continue
        if text[:-1] in title_items or text[1:] in title_items:
            return True
    return False


age_describes = ['童年', '老奶奶', '幼年', '老年', '少年', ]


def delete_age_describe(text: str) -> str:
    for describe in age_describes:
        text = text.replace(describe, '')
    return text


black_name = {'未知', '收废品员', '开发商', '理发师', '小棉袄', '大高个', '地下党', '', '', '', '', '', '', '', '', '', '',
              '', '', '', '',
              '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
              '', '', '', '', ''}


def is_black_name(text: str) -> bool:
    warnings.warn("is_black_name will be deprecated "
                  "because black_name should be disassemble to relationship_title", DeprecationWarning)
    if text in black_name:
        return True
    return False


def clean_role(text: str) -> (str, int):
    """

    :param text:
    :return:

    >>> clean_role('汽车')
    >>> clean_role('唐三')
    >>> clean_role('唐三(主角)')
    """
    score = 10
    text = cut_until_char(text)
    text = delete_char(text)
    text = delete_age_describe(text)
    if not text:
        return '', -100
    if not is_contains_chinese:
        return '', -100
    if has_family_name(text):
        score -= 1
    if is_common_word(text):
        score -= 1
    if is_relationship_title(text):
        score -= 1
    if is_contains_english(text):
        score -= 1
    if is_nick_name(text):
        score -= 1
    if is_contains_figure(text):
        score -= 1
    if is_all_chinese(text):
        score += 1
    if is_black_name(text):
        score -= 1
    logging.info('{}, {}'.format(text, score))
    return text, score


def clean_alias(text: str) -> (str, int):
    score = 13
    if not text:
        return '', -100
    if not is_contains_chinese:
        score -= 5
    if is_common_word(text):
        score -= 5
    if is_relationship_title(text):
        score -= 3
    if is_contains_english(text):
        score -= 1
    if is_nick_name(text):
        score -= 1
    if is_contains_figure(text):
        score -= 1
    if is_all_chinese(text):
        score += 1
    logging.info('{}, {}'.format(text, score))
    return text, score

import sys
from unicodedata import category
punctuation_chars = set([chr(i) for i in range(sys.maxunicode)
                             if category(chr(i)).startswith("P")])
punctuation_chars |= set(['`', ' '])


def get_punctuation():
    return punctuation_chars


def is_punctuation(char):
    return char in punctuation_chars


def select_nested_text(
        text: str,
        deep_add: tuple = ('《',),
        deep_reduce: tuple = ('》',)
) -> str:
    """

    :param text:
    :param deep_add:
    :param deep_reduce:
    :return:

    >>> select_nested_text('《xxxx》')
    """
    new_text = ''
    deep = 0
    for char in text:
        if char in deep_reduce and deep > 0:
            deep -= 1
        if deep != 0:
            new_text += char
        if char in deep_add:
            deep += 1
    return new_text


def delete_nested_text(
        text: str,
        deep_add: tuple = ('(', '（', '[', '【',),
        deep_reduce: tuple = (')', '）', ']', '】',)
) -> str:
    # 删除以（）、()修饰的嵌套成分
    new_text = ''
    deep = 0
    for char in text:
        if char in deep_add:
            deep += 1
        if deep == 0:
            new_text += char
        if char in deep_reduce and deep > 0:
            deep -= 1
    return new_text


pattern_1 = re.compile(r'(全|第)[1-90一二三四五六七八九十零〇]+(章|季|集|部分|部|卷)')
pattern_2 = re.compile(r'[:：]*[（([]*(结局一|结局二|结局三|法国版|完全版|剧场版|电影版|剧场剪辑版|印度版|合体版＋|合体版|重置版|合体剧场版|原版|正序版|精编版|粤语版|总集篇|电视剧版|电视剧|全集|动画版)[）)\]]*')
pattern_3 = re.compile(r'[1-90一二三四五六七八九十零〇]+$')


def get_core_ip(ip: str) -> str:
    """

    :param ip:
    :return:

    >>> get_core_ip('托马斯和他的朋友们第十九部分')
    >>> get_core_ip('托马斯和他的朋友们19')
    >>> get_core_ip('托马斯和他的朋友们结局一')
    >>> get_core_ip('托马斯和他的朋友们(结局一))')
    >>> get_core_ip('托马斯 和他的朋友们:(结局一)')
    >>> get_core_ip('斗罗大陆（全14卷）')
    >>> get_core_ip('一')
    """
    ip = delete_nested_text(ip)
    ip = re.sub(pattern_1, '', ip)
    ip = re.sub(pattern_2, '', ip)
    ip = re.sub(pattern_3, '', ip)
    ip = ip.split(' ')[0]
    ip = ip.split('-')[0]
    return ip


def is_sub_ip(ip: str) -> bool:
    """

    :param ip:
    :return:

    >>> is_sub_ip('托马斯和他的朋友们第十九部分')
    >>> is_sub_ip('托马斯和他的朋友们19')
    >>> is_sub_ip('托马斯和他的朋友们结局一')
    >>> is_sub_ip('托马斯和他的朋友们(结局一))')
    >>> is_sub_ip('托马斯 和他的朋友们:(结局一)')
    >>> is_sub_ip('斗罗大陆（全14卷）')
    >>> is_sub_ip('一')
    """
    if re.search(pattern_1, ip):
        return True
    if re.findall(pattern_2, ip):
        return True
    if re.findall(pattern_3, ip):
        return True
    return False


if __name__ == '__main__':
    import doctest

    doctest.testmod()
