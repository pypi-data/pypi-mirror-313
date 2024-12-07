# -*- coding: UTF-8 -*-
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan-13B-Chat", use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan-13B-Chat", device_map="auto", trust_remote_code=True)
inputs = tokenizer('假设你是抖音用户，发现自己的隐私权受到侵犯，需要向抖音反馈。请模拟用户语气.反馈内容为"没用抖音,但后台看到一直访问定位"，并融合成完整的句子。', return_tensors='pt')
inputs = inputs.to('cuda:0')
try:
    print('base')
    for i in range(5):
        pred = model.generate(**inputs, max_new_tokens=512, repetition_penalty=1.1)
        print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))
except Exception:
    pass
try:
    print('b5-False')
    for i in range(5):
        pred = model.generate(**inputs, max_new_tokens=512, repetition_penalty=1.1, num_beams=5, do_sample=False)
        print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))
except Exception as e:
    print(e)
try:
    print('b5-True')
    for i in range(5):
        pred = model.generate(**inputs, max_new_tokens=512, repetition_penalty=1.1, num_beams=5, do_sample=True)
        print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))
except Exception as e:
    print(e)
try:
    print('tem-0.3')
    for i in range(5):
        pred = model.generate(**inputs, max_new_tokens=512, repetition_penalty=1.1, temperature=0.3)
        print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))
except Exception as e:
    print(e)
try:
    print('tem-1.2')
    for i in range(5):
        pred = model.generate(**inputs, max_new_tokens=512, repetition_penalty=1.1, temperature=1.2)
        print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))
except Exception as e:
    print(e)

"""

"""