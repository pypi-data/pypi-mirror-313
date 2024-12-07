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
获取拼音
"""
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import ranked_permutation, pip_install


def get_pinyin(text: str, tone=False, heteronym=False, concat_heteronym=True, **kwargs) -> List:
    try:
        from pypinyin import pinyin, Style
    except ModuleNotFoundError:
        pip_install('pypinyin <1.0.0')
        from pypinyin import pinyin, Style

    if 'style' not in kwargs:
        if tone:
            kwargs['style'] = Style.TONE
        else:
            kwargs['style'] = Style.NORMAL
    if 'v_to_u' not in kwargs:
        kwargs['v_to_u'] = True
    if 'errors' not in kwargs:
        kwargs['errors'] = 'ignore'
    if heteronym:
        if concat_heteronym:
            return ranked_permutation(pinyin(text, heteronym=heteronym, **kwargs))
        else:
            return pinyin(text, heteronym=heteronym, **kwargs)
    else:
        return [_[0] for _ in pinyin(text, heteronym=heteronym, **kwargs)]


if __name__ == '__main__':
    print(get_pinyin('中心待遇好'))
    print(get_pinyin('中心待遇好', tone=True))
    print(get_pinyin('中心待遇好', tone=True, heteronym=True))
    print(get_pinyin('中心待遇好', tone=True, heteronym=True, concat_heteronym=False))
