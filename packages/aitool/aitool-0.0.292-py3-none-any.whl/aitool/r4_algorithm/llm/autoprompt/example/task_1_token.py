# -*- coding: UTF-8 -*-
"""
Created on
"""
from aitool import dump_json, timestamp, AutoPrompt

task = "生成口令，口令应属于赞美、祝福、励志、正能量主题。口令的韵律感和节奏感强一些，用户看一遍能记住或者是文案趣味性强，能够吸引用户检索"

case_1 = [
    ('你如秋菊淡雅', 'good', '', ''),
    ('您的聪慧如星', 'good', '', ''),
    ('你像璀璨星辰', 'good', '', ''),
    ('乐观拥抱新希望', 'good', '', ''),
    ('勇敢踏上新道路', 'good', '', ''),
    ('善良收获温暖回报', 'good', '', ''),
    ('坚定信念向前行', 'good', '', ''),
    ('拼搏奋进创佳绩', 'good', '', ''),
    ('努力拼搏铸辉煌', 'good', '', ''),
    ('积极向上永不言弃', 'good', '', ''),
    ('活力满满心愿达成', 'good', '', ''),
    ('心怀希望展宏图', 'good', '', ''),
]

ap = AutoPrompt(task, case_1, 'good', 'bad', target_size=50, name='token')
output_prompts, output_input, output_text = ap.work()
dump_json({'prompts': output_prompts, 'cases': output_text}, './task_output/task_1_Token_{}.json'.format(timestamp(style='min')), formatting=True)
