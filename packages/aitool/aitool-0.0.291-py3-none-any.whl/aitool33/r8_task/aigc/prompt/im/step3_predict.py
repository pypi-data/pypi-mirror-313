# -*- coding: UTF-8 -*-
import torch
from tqdm import tqdm
from aitool import load_pickle, dump_pickle
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
data = load_pickle('/mnt/bn/mlxlabzw/llm/Baichuan-13B/prompts.pkl')
tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan-13B-Chat", use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan-13B-Chat", device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan-13B-Chat")
messages = []
rst = load_pickle('prompts_rst.pkl')
print('len rst', len(rst))
idx = 0
try:
    for p in tqdm(data[len(rst):]):
        messages.append({"role": "user", "content": p})
        response = model.chat(tokenizer, messages)
        rst.append(response)
        idx += 1
        dump_pickle(rst, 'prompts_rst.pkl')
except Exception as e:
    print(e)


# model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan-13B-Chat", torch_dtype=torch.float16, trust_remote_code=True)
# model = model.quantize(8).cuda()