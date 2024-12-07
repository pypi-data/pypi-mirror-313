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
from aitool import load_json, load_excel, get_keyword, dump_json
from tqdm import tqdm
bad_w = {'助手', '评价', '送心', '答复', '问题', '会话', '核实', '时间', '结束', '回复', '咨询', '工作人员', '请稍等',
         '看下', '推送', '处理', '服务', '看到', '相关', '解决方案', '跟进', '解决问题', '视频', '留意', '感谢', '帮忙',
         '关闭', '后续', '下载', '用户', '进展', '没有', '放心', '做出', '给予', '等待', '方案', '加快', '速度', '希望',
         '消息', '结果', '历史', '进行', '上传', '不了', '检测', '反馈', '试试', '尝试', '查看', '解决', '转接', '晚点',
         '服务中心', '限制', '原因', '进入', '地方', '草稿箱', '抖音', '可能', '看看', '亲亲', '导致', '试试看', '中心',
         '解决不了', '预兆', '需要', '客服', '时候', '知道', '发送', '同类', '指望', '软件', '团队', '毫无', '人工',
         '提示', '对应', '机器', '应用', '相信', '意义', '建议', '支持', '技术'}
im_text = load_excel('./im.xlsx', to_list=True)
cases = []
all_keys = []
for line in tqdm(im_text[:30000]):
    text = line[1]
    all_keyword = list(get_keyword(text).keys())
    keyword = []
    for k in all_keyword:
        if k not in bad_w:
            keyword.append(k)
    keyword = keyword[:8]
    # print(text)
    # print(keyword)
    if len(keyword) == 0:
        continue
    case = {
        "instruction": "生成一个抖音用户的在线反馈对话，涉及：{}".format('，'.join(keyword)),
        "input": "",
        "output": "{}".format(text)
    }
    cases.append(case)

dump_json(cases, 'task_im.json', formatting=True)

common_cases = load_json('./common.json')
print('len common', len(common_cases))
all_cases = common_cases + cases
dump_json(all_cases, 'all_cases_im.json', formatting=True)
