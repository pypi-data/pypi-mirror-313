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
from aitool import pip_install


def chatgpt(text, api_key):
    """
    最简单的单句调用模式，用一句话作为输入
    :param text:
    :return:

    # 获取 api_key
    - 在openai官网注册账号
    - https://platform.openai.com/docs/quickstart/build-your-application 生成 api_key

    # 查看 api 额度
    - https://platform.openai.com/account/usage
    - 一次请求大概0.1元

    >>> des = '一个拿着双手巨剑的熊猫人战士，强壮但是也很灵敏，朝着目标嘲讽般地大吼'
    >>> chatgpt('请为卡牌{}取10个名字'.format(des), 'sk-000000')
    """
    try:
        import openai
    except ModuleNotFoundError:
        pip_install('openai')
        import openai

    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
                {'role': 'user', 'content': text},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()
