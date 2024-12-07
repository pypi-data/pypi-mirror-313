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
加密工具
"""
from hashlib import md5


def encrypt_md5(text: str) -> str:
    """
    获取text的md5编码结果

    :param text: 待加密文本
    :return: md5编码结果

    >>> encrypt_md5('hello')
    '5d41402abc4b2a76b9719d911017c592'
    """
    new_md5 = md5()
    new_md5.update(text.encode(encoding='utf-8'))
    return new_md5.hexdigest()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
