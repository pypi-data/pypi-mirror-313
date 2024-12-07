# encoding:utf-8
"""
Author: feizhihui
Date: 2020-
"""

import os
from peft import PeftModel
from tqdm import tqdm
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from aitool import load_pickle, dump_pickle, load_lines, dump_excel
import json

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
adapter_path = "/mnt/bn/mlxlabzw/llm/data/checkpoint_0915/"
tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan-13B-Chat", use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan-13B-Chat", device_map="auto",  torch_dtype=torch.float16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan-13B-Chat")
model.generation_config.temperature = 10

pmodel = PeftModel.from_pretrained(model, adapter_path, adapter_name="first_lora")
rst = []
idx = 0
data = load_lines('/mnt/bn/mlxlabzw/llm/Baichuan-13B/sensitive_detection_bloom_test_data.jsonl')
for line in tqdm(data):
    try:
        df = json.loads(line)
        p = df['input']
        src = df['source']
        ans = df['output']
        print('>>> input')
        print(p)
        messages = []
        messages.append({"role": "user", "content": p})
        response = pmodel.chat(tokenizer, messages)
        print('>>> output')
        print(response)
        rst.append([p, src, ans, response])
        idx += 1
        if idx % 100 == 0:
            dump_pickle(rst, 'prompts_rst_chat_0915_2.pkl')
            dump_excel(rst, 'prompts_rst_chat_0915_2.xlsx')
    except Exception as e:
        print(e)
dump_pickle(rst, 'prompts_rst_chat_0915_2.pkl')
dump_excel(rst, 'prompts_rst_chat_0915_2.xlsx')


