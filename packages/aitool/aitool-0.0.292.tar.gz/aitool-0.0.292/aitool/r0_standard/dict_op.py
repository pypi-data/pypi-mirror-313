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
操作字典
"""
from typing import Dict, List


def split_dict(ori_dict: Dict, keys: List) -> (Dict, Dict):
    """
    依据keys筛选出data里key在keys里的数据

    :param ori_dict: a dict
    :param keys: keys selected
    :return: selected_dict, abandon_dict

    >>> split_dict({1:'a', 2: 'b'}, [1])
    ({1: 'a'}, {2: 'b'})
    >>> split_dict({1:'a', 2: 'b'}, [1,3])
    ({1: 'a'}, {2: 'b'})
    """
    selected_dict = {}
    abandon_dict = {}
    for k, v in ori_dict.items():
        if k in keys:
            selected_dict[k] = v
        else:
            abandon_dict[k] = v
    return selected_dict, abandon_dict


if __name__ == '__main__':
    import doctest

    doctest.testmod()
