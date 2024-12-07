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
from typing import Any
from aitool import singleton, pip_install, print_yellow


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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
