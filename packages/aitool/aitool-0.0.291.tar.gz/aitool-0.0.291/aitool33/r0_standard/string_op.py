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
操作字符串
"""
from typing import Tuple, Union, List, Iterator


def is_contain(text: str, subs: List[str]) -> bool:
    """
    判定text里是否包含任何一个subs中的元素

    :param text: 文本
    :param subs: 多个文本
    :return: text是否包含subs中的任何一个文本
    """
    for sub in subs:
        if sub in text:
            return True
    return False


def get_str(*args, **kwargs) -> str:
    """
    将输出参数转化为字符串

    >>> get_str(1, 'a')
    "(1, 'a')"
    >>> get_str(b=2, c={4:5})
    "{'b': 2, 'c': {4: 5}}"
    >>> get_str(1, 'a', b=2, c={4:5})
    "(1, 'a'){'b': 2, 'c': {4: 5}}"
    """
    args_str = ''
    kwargs_str = ''
    if len(args):
        args_str = '{}'.format(args)
    if len(kwargs):
        kwargs_str = '{}'.format(kwargs)
    return args_str + kwargs_str


def is_contains_english(text: str) -> bool:
    """
    判定是否包含英文

    :param text: 文本
    :return: 是否包含英文

    >>> is_contains_english('A')
    True
    >>> is_contains_english('123')
    False
    >>> is_contains_english('粤A50572')
    True
    """
    for c in text:
        _ord = ord(c)
        if 65 <= _ord <= 90 or 97 <= _ord <= 122:
            return True
    return False


def cut_until_char(text: str, delimiter: set = None) -> str:
    """
    从遇到的第一个截断符处截断

    :param text: 文本
    :param delimiter: 多个截断符，用set存储。如果为空则使用默认的截断符
    :return: 第一个截断符前的文本

    >>> cut_until_char('正文（附录）')
    '正文'
    """
    if delimiter is None:
        delimiter = {'(', '[', '【', '〔', '（'}
    for index, char in enumerate(text):
        if char in delimiter:
            return text[:index]
    return text


def delete_char(text: str, discard: set = None):
    """
    删除属于丢弃集的字符

    :param text: 文本
    :param discard: 丢弃集，用set存储。如果为空则使用默认的丢弃集
    :return: 删除了丢弃集中的字符的文本

    >>> delete_char('正文（附录）')
    '正文附录'
    """
    if discard is None:
        discard = {'(', '[', '【', '〔', '（', ')', '-', '.', '—', '“', '”', '《', '〕', '）', '－'}
    new_text = ''
    for char in text:
        if char not in discard:
            new_text += char
    return new_text


def is_contains_figure(text: str) -> bool:
    """
    判定是否包含数字

    :param text: 文本
    :return: 是否包含数字

    >>> is_contains_figure('粤A')
    False
    >>> is_contains_figure('粤A13')
    True
    """
    for char in text:
        if char.isdigit():
            return True
    return False


def is_contains_chinese(text) -> bool:
    """
    判定是否包含中文

    :param text: 文本
    :return: 是否包含中文

    >>> is_contains_figure('粤A')
    False
    >>> is_contains_figure('粤A13')
    True
    """
    for _char in text:
        if '\u4e00' <= _char <= '\u9fff':
            return True
    return False


def is_all_chinese(text: str) -> bool:
    """
    判定是否全是中文

    :param text: 文本
    :return: 是否全是中文

    >>> is_all_chinese('粤省')
    True
    >>> is_all_chinese('粤A')
    False
    """
    for char in text:
        if not is_contains_chinese(char):
            return False
    return True


def get_chinese(text: str) -> str:
    """
    抽取出中文

    :param text: 文本
    :return: 中文文本

    >>> get_chinese('粤+省=PROVINCE')
    粤省
    """
    rst = ''
    for char in text:
        if is_contains_chinese(char):
            rst += char
    return rst


def rate_chinese(text: str) -> float:
    """
    中文的占比

    :param text: 文本
    :return: 中文的占比

    >>> rate_chinese('粤省')
    1.0
    >>> rate_chinese('粤A')
    0.5
    >>> rate_chinese('ABC')
    0.0
    """
    cnt = 0
    for char in text:
        if is_contains_chinese(char):
            cnt += 1
    if len(text) == 0:
        return 1
    return cnt/len(text)


def is_no_symbol(text: str, symbol: set = None) -> bool:
    """
    是否不包含任何symbol(单个字符)

    :param text: 文本
    :param symbol: 符号
    :return: 中文的占比

    >>> is_no_symbol('你好，吃过了吗？')
    False
    >>> is_no_symbol('Alice你好吃过了吗')
    True
    """
    if symbol is None:
        symbol = {' ', '，', ',', '。', '？', '?', ']', '[', '】', '【', '！', '!', '\t', '\n', '(', ')', '（', '）', '：',
                  ':', '、', '\"', '\'', '”', '“', '～', '~', '|', '—'}
    for char in text:
        if char in symbol:
            return False
    return True


def find_all_position(substr: str, text: str) -> List[Tuple[int, int]]:
    """
    找到substr在context里出现的所有位置

    :param substr: 需要查找的文本片段
    :param text: 文本
    :return: substr在context里出现的所有位置

    >>> find_all_position('12', '12312312')
    [(0, 2), (3, 5), (6, 8)]
    """
    return [(i, i + len(substr)) for i in range(len(text)) if text.startswith(substr, i)]


def get_ngram(text: str, ngram: int = 2, no_chars: str = '') -> Iterator[str]:
    """
    获取text的所有ngram片段

    :param no_chars: ngram里不可以保护的char集
    :param text: 文本
    :param ngram: 判断的字长
    :return: text的所有ngram片段

    >>> list(get_ngram('abcd'))
    ['ab', 'bc', 'cd']
    """
    for i in range(len(text)-ngram+1):
        n = text[i: i+ngram]
        if len(set(n) & set(no_chars)) > 0:
            continue
        yield n


def get_ngrams(text: Union[str, List[str]], min_gram: int, max_gram: int) -> List[str]:
    """
    获取text的多个ngram片段

    :param text: 字符串或list
    :param min_gram: 最小gram数
    :param max_gram: 最大gram数
    :return: ngram片段

    >>> list(get_ngrams('abcd', 1, 3))
    ['a', 'b', 'c', 'd', 'ab', 'bc', 'cd', 'abc', 'bcd']
    >>> list(get_ngrams(['a', 'bc', 'd', 'ef'], 1, 3))
    [['a'], ['bc'], ['d'], ['ef'], ['a', 'bc'], ['bc', 'd'], ['d', 'ef'], ['a', 'bc', 'd'], ['bc', 'd', 'ef']]
    """
    rst = []
    for ngram in range(min_gram, max_gram+1):
        rst.extend(list(get_ngram(text, ngram)))
    return rst


def ngrams_permutation(text: Union[str, List[str]], min_gram: int, max_gram: int) -> List[List]:
    """
    获取text的多个ngram片段

    :param text: 字符串或list
    :param min_gram: 最小gram数
    :param max_gram: 最大gram数
    :return: ngram片段

    >>> list(ngrams_permutation('abcd', 1, 3))
    [['a', 'b', 'c', 'd'], ['a', 'b', 'cd'], ['a', 'bc', 'd'], ['a', 'bcd'], ['ab', 'c', 'd'], ['ab', 'cd'], ['abc', 'd']]
    >>> list(ngrams_permutation(['a', 'bc', 'd', 'ef'], 1, 3))
    [[['a'], ['bc'], ['d'], ['ef']], [['a'], ['bc'], ['d', 'ef']], [['a'], ['bc', 'd'], ['ef']], [['a'], ['bc', 'd', 'ef']], [['a', 'bc'], ['d'], ['ef']], [['a', 'bc'], ['d', 'ef']], [['a', 'bc', 'd'], ['ef']]]
    """
    def _permutation(remainder, prefix, items):
        if len(remainder) == 0:
            yield prefix
        for item in items:
            len_item = len(item)
            if remainder[:len_item] == item:
                yield from _permutation(remainder[len_item:], prefix+[item], items)

    ngrams = get_ngrams(text, min_gram, max_gram)
    yield from _permutation(text, [], ngrams)


def token_hit(text: str, tokens: Iterator[str]) -> List[str]:
    """
    获取text中包含的token的列表

    :param text: 待处理的文本
    :param tokens: 字符串的列表
    :return: 命中的字符串的列表

    >>> token_hit('1234567', ['1', '34', '9'])
    ['1', '34']
    """
    hit_token = []
    tokens = set(list(tokens))
    for token in tokens:
        if token in text:
            hit_token.append(token)
    return hit_token


def filter_keyword(text: str, keywords: List[str], min_count: int = 1) -> bool:
    """
    判定test里命中keywords里的词的数量是否大于等于min_count个

    :param text: 待判定文本
    :param keywords: 多个关键词组成的List
    :param min_count: 最小命中个数
    :return: 是否命中min_count个关键词】

    >>> filter_keyword('12345', ['234', '45'], 2)
    True
    """
    keywords = set(keywords)
    keywords_len = [len(k) for k in keywords]
    min_ngram = min(keywords_len)
    max_ngram = max(keywords_len)
    the_grams = set(get_ngrams(text, min_ngram, max_ngram))
    if len(keywords & the_grams) >= min_count:
        return True
    return False


if __name__ == '__main__':
    import doctest

    doctest.testmod()
