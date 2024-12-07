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


def get_sentiment(text):
    # 对短语的效果不佳
    try:
        from snownlp import SnowNLP
    except ModuleNotFoundError:
        pip_install('snownlp <1.0.0')
        from snownlp import SnowNLP

    s = SnowNLP(text)
    return s.sentiments


if __name__ == '__main__':
    _text = ['受害者有罪', '酒店老板', '酒吧老板', '扫黑除恶', '苍蝇不叮无缝', '孩子父母', '家长责任', '父母的责任', '酒店也有责任',
             '教育孩子', '不判死刑', '老板酒吧', '女孩父母', '儿子的，请教育', '女孩去酒店', '可怜的孩子', '孩子家长', '父母教育',
             '延迟退休', '退休工资', '退休延迟', '工作到退休', '公务员退休', '退休，工作', '法国人民', '退休，国家', '不想退休',
             '制定政策', '退休人员', '人民服务', '免费医疗', '专家80岁退休', '国家政策', '退休[流泪', '工作时间', '不生孩子']
    for _t in _text:
        print(_t)
        print(get_sentiment(_t))
