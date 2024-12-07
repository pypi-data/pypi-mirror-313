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
去重
"""
from typing import List, Iterator, Any, NoReturn, Tuple, Union
from aitool.r0_standard.security import encrypt_md5


def deduplicate(items: Iterator[Union[str, int, Tuple]]) -> List[Union[str, int, Tuple]]:
    """
    在不影响原顺序的情况下对 items 去重

    >>> deduplicate([1,2,3,2,1])
    [1, 2, 3]
    """
    cache = set()
    item_ddp = []
    for item in items:
        if item not in cache:
            cache.add(item)
            item_ddp.append(item)
    return item_ddp


class Deduplication:
    """
    is_duplication 判定某个元素是否已经出现过
    """
    def __init__(self, use_md5: bool = True):
        """
        存储以前判定过的元素

        :param use_md5: 是否用md5来存储元素
        """
        self.use_md5 = use_md5
        self.data = set()

    def add(self, item: Any) -> NoReturn:
        """
        记录元素
        :param item: 元素
        :return: 无
        """
        if not isinstance(item, str):
            item = '{}'.format(item)
        if self.use_md5:
            self.data.add(encrypt_md5(item))
        else:
            self.data.add(item)

    def clean(self) -> NoReturn:
        """
        清空之前纯粹的元素
        """
        self.data = set()

    def is_duplication(self, item: Any, update=True) -> bool:
        """
        判断item是否重复出现。默认使用md5压缩存储。

        :param item: 待判定的元素
        :param update: 判定后是否将item存储到 self.data
        :return: 是否重复

        >>> deduplication = Deduplication()
        >>> for data in [1,1,2]:
        ...     deduplication.is_duplication(data)
        False
        True
        False
        """
        if not isinstance(item, str):
            item = '{}'.format(item)
        if self.use_md5:
            item = encrypt_md5(item)
        if item in self.data:
            return True
        else:
            if update:
                self.data.add(item)
        return False


if __name__ == '__main__':
    import doctest

    doctest.testmod()
