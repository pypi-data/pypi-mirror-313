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
from aitool import get_stop_word, get_punctuation, singleton
from random import sample, random


import random


def random_bool(probability=0.5):
    """Returns True with given probability

    Args:
        probability: probability to return True

    """
    assert (0 <= probability <= 1), "probability needs to be >= 0 and <= 1"
    return random.random() < probability


def count_lines(filename):
    """Returns the number of lines in the given file

    Args:
        filename: (string) path to the file

    """
    return sum(1 for line in open(filename))


def add_random_token(line, probability, tokens):
    """Delete random tokens in a given String with given probability

    Args:
        line: a String
        probability: probability to delete each token

    """
    line_split = [c for c in line]
    ret = [token if not random_bool(probability) else token+sample(tokens, 1)[0] for token in line_split]
    return "".join(ret)


def delete_random_token(line, probability):
    """Delete random tokens in a given String with given probability

    Args:
        line: a String
        probability: probability to delete each token

    """
    line_split = [c for c in line]
    ret = [token for token in line_split if not random_bool(probability)]
    return "".join(ret)


def replace_random_token(line, probability, tokens):
    """Replace random tokens in a String by a filler token with given probability

    Args:
        line: a String
        probability: probability to replace each token
        filler_token: token replacing chosen tokens

    """
    line_split = [c for c in line]
    for i in range(len(line_split)):
        if random_bool(probability):
            line_split[i] = sample(tokens, 1)[0]
    return "".join(line_split)


def random_token_permutation(line, probability, _range):
    """Random permutation over the tokens of a String, restricted to a range, drawn from the uniform distribution

    Args:
        line: a String
        _range: Max range for token permutation

    """
    line_split = [c for c in line]
    new_indices = [i+random.uniform(0, _range+1) if random_bool(probability) else i for i in range(len(line_split))]
    res = [x for _, x in sorted(zip(new_indices, line_split), key=lambda pair: pair[0])]
    return "".join(res)


@singleton
class DefaultTokens():
    def __init__(self):
        word_stop = get_stop_word()
        punctuation = get_punctuation()
        self.tokens = list(word_stop) + list(punctuation) * 2

    def get_tokens(self):
        return self.tokens


def add_noise(
        text,
        tokens=None,
        prob_ori=0.3,
        prob_add=0.1,
        prob_dlt=0.1,
        prob_rpl=0.1,
        prob_pmt=0.1,
        range_pmt=2,
):
    if tokens is None:
        dt = DefaultTokens()
        tokens = dt.get_tokens()
    if random_bool(prob_ori):
        return text
    text = add_random_token(text, probability=prob_add, tokens=tokens)
    text = delete_random_token(text, probability=prob_dlt)
    text = replace_random_token(text, probability=prob_rpl, tokens=tokens)
    text = random_token_permutation(text, probability=prob_pmt, _range=range_pmt)
    return text


if __name__ == '__main__':
    _text = '你吃过早饭了吗'
    for i in range(10):
        print(add_noise(_text))
