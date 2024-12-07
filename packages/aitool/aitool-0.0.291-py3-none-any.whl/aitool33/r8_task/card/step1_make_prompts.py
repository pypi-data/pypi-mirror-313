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
from random import sample, shuffle, random
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import load_excel, dump_pickle, dump_excel, load_lines, timestamp


# 生成卡牌
def get_card(num=1000):
    rst = []
    cards = load_excel('./用户描述to卡.xlsx', to_list=True)
    for _ in range(num):
        exp = sample(cards, 3)
        prompt = '卡牌类型分为魔法卡、陷阱卡、随从卡。卡牌效果包括费用、攻击力、血量、效果。你是一个卡牌游戏设计者，请设计1卡牌，包括"卡牌类型、卡牌背景、卡牌效果、卡牌名称"。输出格式为：【卡牌类型】/【卡牌背景】/【卡牌效果】/【卡牌名称】。\n以下是一些示例：\n1、【{}】/【{}】/【{}】/【{}】\n2、【{}】/【{}】/【{}】/【{}】\n3、【{}】/【{}】/【{}】/【{}】'.format(exp[0][0], exp[0][1], exp[0][2], exp[0][3], exp[1][0], exp[1][1], exp[1][2], exp[1][3], exp[2][0], exp[2][1], exp[2][2], exp[2][3],)
        rst.extend([prompt])
    return rst


# 卡牌描述
def get_describe(num=1000):
    rst = []
    cards = load_excel('./用户描述to卡.xlsx', to_list=True)
    for _ in range(num):
        exp = sample(cards, 3)
        prompt_6 = '卡片的概念设计是用口语化的语言来描述一张卡牌的设计原型、形象特点、特质等信息。你是一个卡牌游戏设计者，请做出一张新卡概念设计。以下是一些示例：\n1、{}\n2、{}\n3、{}'.format(exp[0][1], exp[1][1], exp[2][1])
        rst.extend([prompt_6])
    return rst


# 卡牌描述
def get_name(power=100):
    rst = []
    describes = load_lines('./物料/生成_用户描述_1220.txt')
    for _ in range(power):
        for exp in describes:
            prompt = """你是一个游戏设计师，请为卡牌“{}”取10个名字。""".format(exp)
            rst.append([exp, prompt])
    return rst


# 卡牌参数
def get_element_chatgpt(num=100000):
    rst = []
    gap = [0, 0.1, 0.2, 0.3, 0.4, 0.5, -0.1, -0.2, -0.3, -0.4, -0.5]
    describes = load_lines('./物料/生成_用户描述_1220.txt')
    for _ in range(num):
        exp = sample(describes, 1)[0]
        prompt = """有5个不同背景的游戏设计师对卡牌“{}”进行评估，并取10个卡牌名字。

每个评估项应该给出5位评委各自的打分，分数是一个0到10之间的小数，应该准确到小数点后两位，分数越大越符合。以下是一些打分示例：
{}分：完全不符合，
{}分：有微弱关联，
{}分：有一些关联，
{}分：较符合，
{}分：非常符合。

评估维度包括：
1、是角色卡，
2、是魔法卡，
3、是陷阱卡，
4、攻击力很高，
5、生命值很高，
6、有单体伤害随从的能力，
7、有单体治疗随从的能力，
8、有群体伤害随从的能力，
9、有群体治疗随从的能力，
10、有群体治疗随从的能力，
11、有伤害御主的能力，
12、有治疗御主的能力，
13、普攻有暴击能力，
14、有辅助单体增加物理伤害的能力，
15、有辅助群体增加物理伤害的能力，
16、有辅助单体治疗能力，
17、有辅助全体增加法术伤害能力，
18、有抽牌的能力，
19、有无效化魔法或陷阱的能力，
20、有嘲讽敌人的能力
21、有使选定敌人变得毫无战斗力的能力

输出格式如下，将其中的xxx替换为具体内容
【是角色卡：xxx】/【是魔法卡：xxx】/【是陷阱卡：xxx】/【攻击力很高：xxx】/【生命值很高：xxx】/【有单体伤害随从的能力：xxx】/【有单体治疗随从的能力：xxx】/【有群体伤害随从的能力：xxx】/【有群体治疗随从的能力：xxx】/【有群体治疗随从的能力：xxx】/【有伤害御主的能力：xxx】/【有治疗御主的能力：xxx】/【普攻有暴击能力：xxx】/【有辅助单体增加物理伤害的能力：xxx】/【有辅助群体增加物理伤害的能力：xxx】/【有辅助单体治疗能力：xxx】/【有辅助全体增加法术伤害能力：xxx】/【有抽牌的能力：xxx】/【有无效化魔法或陷阱的能力：xxx】/【有嘲讽敌人的能力：xxx】/【有使选定敌人变得毫无战斗力的能力：xxx】/【十个候选名字：xxx】
        """.format(
            exp,
            round(0.5+sample(gap, 1)[0], 2),
            round(2.7+sample(gap, 1)[0], 2),
            round(5.0+sample(gap, 1)[0], 2),
            round(7.3+sample(gap, 1)[0], 2),
            round(9.5+sample(gap, 1)[0], 2),
        )
        rst.append([exp, prompt])
    return rst


# 卡牌参数
def get_element_baichuan(num=100000):
    rst = []
    describes = load_lines('./物料/生成_用户描述_1220.txt')
    for _ in range(num):
        exp = sample(describes, 1)[0]
        prompt = """请判断文本“{}”与下列各个文本的相关性分数，分数在0~1之间，0表示不相关，1表示完全相关,不能是0也不能是1。
回复时需要带上下列的文本。
1、是角色卡，
2、是魔法卡，
3、是陷阱卡，
4、攻击力很高，
5、生命值很高，
6、有单体伤害随从的能力，
7、有单体治疗随从的能力，
8、有群体伤害随从的能力，
9、有群体治疗随从的能力，
10、有群体治疗随从的能力，
11、有伤害御主的能力，
12、有治疗御主的能力，
13、普攻有暴击能力，
14、有辅助单体增加物理伤害的能力，
15、有辅助群体增加物理伤害的能力，
16、有辅助单体治疗能力，
17、有辅助全体增加法术伤害能力，
18、有抽牌的能力，
19、有无效化魔法或陷阱的能力，
20、有嘲讽敌人的能力
21、有使选定敌人变得毫无战斗力的能力
22、{}
        """.format(
            exp, exp
        )
        rst.append([exp, prompt])
    return rst


if __name__ == '__main__':
    inputs = []
    # inputs.extend(get_element_baichuan(num=100000))
    inputs.extend(get_name(power=100))
    # shuffle(inputs)
    dump_pickle(inputs, './中间产物/card_task_name_{}.pkl'.format(timestamp(style='min')))
    dump_excel(inputs, './中间产物/card_task_name_{}.xlsx'.format(timestamp(style='min')))
