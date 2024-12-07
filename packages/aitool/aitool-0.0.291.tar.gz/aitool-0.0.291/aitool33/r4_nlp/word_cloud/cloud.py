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
import jieba


def word_cloud(text, font_path, out_file):
    from wordcloud import WordCloud

    words = jieba.lcut(text)     # 精确分词
    newtxt = ''.join(words)     # 空格拼接
    wordcloud = WordCloud(font_path=font_path).generate(newtxt)
    wordcloud.to_file('中文词云图2.jpg')


if __name__ == '__main__':
    word_cloud(
        '我希望你充当一个语文作业工具，我将提供一个中文句子，你的任务是对句子进行改写、改写出5个内容一致的句子',
        font_path='/Library/Fonts/Arial Unicode.ttf',
        out_file='./云图.jpg',
    )
