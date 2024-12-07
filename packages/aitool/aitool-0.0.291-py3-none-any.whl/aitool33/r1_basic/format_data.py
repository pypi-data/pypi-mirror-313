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
转变数据格式
"""
import ast
import json
from collections import Counter
from typing import Dict, Union, List, Any, Iterable, Generator
import numpy as np
from aitool import pip_install


def flatten(data: Any, ignore_types: tuple = (str, bytes)) -> Generator:
    """
    逐个输出data里的元素

    :param data: any data
    :param ignore_types: types will not be flattened
    :return: a generator of a flatten list

    >>> list(flatten([[1,2,('a',4)],'hello']))
    [1, 2, 'a', 4, 'hello']
    >>> list(flatten('a'))
    ['a']
    >>> list(flatten({1:2}))
    [1, 2]
    >>> list(flatten([{1:2}, {('a', 3.0): '4'}]))
    [1, 2, 'a', 3.0, '4']
    """

    if isinstance(data, ignore_types):
        yield data
    elif isinstance(data, dict):
        yield from flatten(list(data.items()))
    elif isinstance(data, Iterable):
        for item in data:
            if isinstance(item, Iterable) and not isinstance(item, ignore_types):
                yield from flatten(item)
            else:
                yield item
    else:
        yield data


def html2text(html: str) -> str:
    """
    抽取出html中的字符串

    :param html: html的文本
    :return: html中的内容部分

    >>> html2text('<html><head><title>标题</title></head><body>网页内容</body></html>')
    '标题网页内容'
    """
    try:
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        pip_install('bs4')
        from bs4 import BeautifulSoup
    try:
        import lxml
    except ModuleNotFoundError:
        pip_install('lxml')
        import lxml
    content = BeautifulSoup(html, 'lxml').text
    content = content.replace('\xa0', ' ')
    return content


def content2text(data: Any, debug: bool = True) -> str:
    """
    提取以下两种数据格式中的文本部分：
    1、html格式
    2、'[{'info':'text'}, {'info':'text'}]'

    :param data: 待处理的数据格式
    :param debug: debug模式下会打印报错信息
    :return: content中的文本格式

    >>> content2text('<html><head><title>标题</title></head><body>网页内容</body></html>')
    '标题网页内容'
    >>> content2text("[{'info':'text'}, {'info':'!'}]")
    'text!'
    """
    content = ''
    try:
        for item in ast.literal_eval(data):
            if 'info' in item:
                content += item['info']
    except Exception as e1:
        try:
            content = html2text(data)
        except Exception as e2:
            if debug:
                print(data)
                print(e1, e2)
    return content


def split_part(text: str, sep: List[str]) -> List[str]:
    """
    依据sep做切分。对sep的匹配是贪心的。
    :param text:
    :param sep:
    :return:

    >>> split_part('1234512345', ['1', '34'])
    ['1', '2', '34', '5', '1', '2', '34', '5']
    """
    sp_text = []
    head = 0
    last_head = 0
    while head < len(text):
        for s in sep:
            if text[head:head + len(s)] == s:
                if head > last_head:
                    sp_text.append(text[last_head:head])
                sp_text.append(text[head:head + len(s)])
                head = head + len(s)
                last_head = head
                break
        head += 1
    if last_head < len(text):
        sp_text.append(text[last_head:])
    return sp_text


def get_pair(
        data,
        only_leaf=True,
        str_format=False,
        do_eval=False,
        key_eval=None,
        key_skip=None,
        separator='.',
        fullname=True,
        show_index=False,
) -> List[List[Any]]:
    """
    将结构化的数据 转化为 list[路径,值]的格式。例如将

    :param data: 结构化的数据
    :param only_leaf: 仅输出叶子节点
    :param str_format: 将输出值转为str格式
    :param do_eval: 对字符串进行解析
    :param key_eval: TODO 待重新色剂
    :param key_skip: 忽略的节点名 TODO 目前需要用内部名，不方便
    :param separator: 连接不同层级的符号
    :param fullname: True则输出全部路径，False则只输出最后一层路径
    :param show_index: 是否附带list的下标作为路径
    :return: List[路径,值]的数据

    >>> get_pair({1:2, 3:{4:5}})  # 基础用法
    [['1', 2], ['3.4', 5]]

    >>> get_pair({1:2, 3:int}, str_format=True)  # 输出的值转为str格式
    [['1', '2'], ['3', "<class 'int'>"]]

    >>> get_pair([1, 2, [3, 4]])  # 基础用法
    [['', 1], ['', 2], ['', 3], ['', 4]]

    >>> get_pair([1, 2, [3, 4]], show_index=True)  # 附带list的下标作为路径
    [['0', 1], ['1', 2], ['2.0', 3], ['2.1', 4]]

    >>> get_pair({1:2, 3:{4:[5,6]}, 7:'{8,9}'})  # 基础用法
    [['1', 2], ['3.4', 5], ['3.4', 6], ['7', '{8,9}']]

    >>> get_pair({1:2, 3:{4:[5,6]}, 7:'{8,9}'}, separator='->')  # 修改连接符
    [['1', 2], ['3->4', 5], ['3->4', 6], ['7', '{8,9}']]

    >>> get_pair({1:2, 3:{4:[5,6]}, 7:'{8,9}'}, fullname=False)  # 输出简短的名称
    [['1', 2], ['4', 5], ['4', 6], ['7', '{8,9}']]

    >>> get_pair({1:2, 3:{4:[5,6]}, 7:'{8,9}'}, do_eval=True)  # 对字符串进行解析
    [['1', 2], ['3.4', 5], ['3.4', 6], ['7', 8], ['7', 9]]

    >>> get_pair({1:2, 3:{4:[5,6]}}, only_leaf=False)  # 同时输出非叶子的pair对
    [['', {1: 2, 3: {4: [5, 6]}}], ['1', 2], ['3', {4: [5, 6]}], ['3.4', [5, 6]], ['3.4', 5], ['3.4', 6]]
    """

    def _format_kv_data(_data, _str_format=True):
        """
        用于将各种类型的数据通过format方法转为字符串
        """
        if _str_format:
            return '{}'.format(_data)
        return _data

    def _get_kv_pair(
            _data,
            pre='',
            _only_leaf=True,
            _str_format=False,
            _do_eval=False,
            _key_eval=None,
            _key_skip=None,
            _separator_key='$k.',
            _separator_index='$i.',
    ):
        """
        用于递归地遍历各个项
        """
        kv_pair = []

        if _key_skip and pre in _key_skip:
            return kv_pair

        if _do_eval and isinstance(_data, str):
            try:
                if _key_eval is None or pre in _key_eval:
                    kv_pair.extend(
                        _get_kv_pair(ast.literal_eval(_data), pre=pre, _only_leaf=_only_leaf, _str_format=_str_format,
                                     _do_eval=_do_eval, _key_eval=_key_eval, _key_skip=_key_skip,
                                     _separator_key=_separator_key, _separator_index=_separator_index))
                    return kv_pair
            except (TypeError, SyntaxError, NameError):
                pass
            try:
                if _key_eval is None or pre in _key_eval:
                    kv_pair.extend(_get_kv_pair(json.loads(_data), pre=pre, _only_leaf=_only_leaf,
                                                _str_format=_str_format, _do_eval=_do_eval, _key_eval=_key_eval,
                                                _key_skip=_key_skip, _separator_key=_separator_key,
                                                _separator_index=_separator_index))
                    return kv_pair
            except (TypeError, SyntaxError, NameError, json.decoder.JSONDecodeError):
                pass

        if isinstance(_data, dict):
            if not _only_leaf:
                kv_pair.append((pre, _format_kv_data(_data, _str_format=_str_format)))
            for _k, _v in _data.items():
                kv_pair.extend(
                    _get_kv_pair(_v, pre=pre + _separator_key + str(_k), _only_leaf=_only_leaf, _str_format=_str_format,
                                 _do_eval=_do_eval, _key_eval=_key_eval, _key_skip=_key_skip,
                                 _separator_key=_separator_key, _separator_index=_separator_index))
        elif isinstance(_data, (list, tuple, set)):
            if not _only_leaf:
                kv_pair.append((pre, _format_kv_data(_data, _str_format=_str_format)))
            for index, d in enumerate(_data):
                kv_pair.extend(_get_kv_pair(d, pre=pre + _separator_index + str(index), _only_leaf=_only_leaf,
                                            _str_format=_str_format, _do_eval=_do_eval, _key_eval=_key_eval,
                                            _key_skip=_key_skip,
                                            _separator_key=_separator_key, _separator_index=_separator_index))
        else:
            kv_pair.append((pre, _format_kv_data(_data, _str_format=_str_format)))
        return kv_pair

    if not fullname:
        show_index = False
    separator_key = '$$@@key.'
    separator_index = '$$@@ind.'

    all_kv_pair = _get_kv_pair(
        data,
        pre='',
        _only_leaf=only_leaf,
        _str_format=str_format,
        _do_eval=do_eval,
        _key_eval=key_eval,
        _key_skip=key_skip,
        _separator_key=separator_key,
        _separator_index=separator_index)

    pair = []
    for k, v in all_kv_pair:
        name_part = []
        need = True
        for k_sp in split_part(k, [separator_key, separator_index]):
            if k_sp == separator_index:
                if not show_index:
                    need = False
                continue
            if k_sp == separator_key:
                continue
            if need:
                name_part.append(k_sp)
            else:
                need = True
        if fullname:
            name = separator.join(name_part)
        else:
            name = name_part[-1] if len(name_part) > 0 else ''
        pair.append([name, v])

    return pair


def np2list(data) -> list:
    """
    将np转为list。

    :param data:
    :return: list

    >>> print(np2list(np.array([1, 2])))
    [1, 2]

    >>> print(np2list(np.array([[1, 2], [3, 4]])))
    [[1, 2], [3, 4]]
    """
    _type = type(data)
    if _type == np.ndarray:
        if data.ndim >= 1:
            return [np2list(d) for d in data]
    if _type in [np.intp, np.int8, np.int16, np.int32, np.int64]:
        return int(data)
    return data


def get_most_item(items: List[str], short=True) -> str:
    """
    选出出现次数最高的字符串。
    :param items: 字符串的列表
    :param short: short=True: 出现次数相同时，选长度最短的。short=False: 出现次数相同时，选长度最长的。
    :return: 出现次数最高的字符串

    >>> get_most_item(['aa','a','aa','a','ab',])
    'a'

    >>> get_most_item(['aa','a','aa','a','ab',], short=False)
    'aa'
    """
    text = ''
    cnt = 0
    for k, c in Counter(items).items():
        if c > cnt:
            text = k
            cnt = c
        elif c == cnt:
            if short and len(k) < len(text):
                text = k
                cnt = c
            if not short and len(k) > len(text):
                text = k
                cnt = c
    return text


def dict2ranked_list(
        the_dict: Dict[Any, Union[int, float]],
        limit: int = -1,
        reverse: bool = False,
):
    """
    将字典转为有序数组，要求value为int或float
    对结果排序，以便在在内存有限时只读取头部的部分数据

    :param the_dict: dict数据，其中value都是int或float
    :param limit: 输出前limit个数据，如果是-1则无限制
    :param reverse: 是否逆序排序
    :return: 有序数组

    >>> dict2ranked_list({'A':3, 'B':1})
    [['B', 1], ['A', 3]]

    >>> dict2ranked_list({'A':3, 'B':1}, limit=1)
    [['B', 1]]

    >>> dict2ranked_list({'A':3, 'B':1}, reverse=True)
    [['A', 3], ['B', 1]]
    """
    ranked_list = []
    for k, v in the_dict.items():
        ranked_list.append([k, v])
    ranked_list.sort(key=lambda _: _[1], reverse=reverse)
    if limit >= 0:
        ranked_list = ranked_list[:limit]
    return ranked_list


if __name__ == '__main__':
    import doctest

    doctest.testmod()
