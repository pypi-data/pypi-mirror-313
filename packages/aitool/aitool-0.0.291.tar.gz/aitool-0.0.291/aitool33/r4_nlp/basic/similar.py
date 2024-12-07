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
from aitool import get_ngram


def term_similar(text1, text2, ngram=2):
    s1 = set(list(get_ngram(text1, ngram=ngram)))
    s2 = set(list(get_ngram(text2, ngram=ngram)))
    sim = len(s1 & s2) / min(len(s1), len(s2))
    return sim


def term_similar_bag(texts1, texts2, ngram=2):
    max_sim = 0
    if type(texts1) == str:
        texts1 = [texts1]
    if type(texts2) == str:
        texts2 = [texts2]
    for t1 in texts1:
        for t2 in texts2:
            sim = term_similar(t1, t2, ngram=ngram)
            max_sim = max(sim, max_sim)
    return max_sim


if __name__ == '__main__':
    print(term_similar('你吃过早饭了吗', '你会做早饭吗'))
    print(term_similar_bag('你吃过早饭了吗', ['你会做早饭吗', '吃过早饭啦']))
