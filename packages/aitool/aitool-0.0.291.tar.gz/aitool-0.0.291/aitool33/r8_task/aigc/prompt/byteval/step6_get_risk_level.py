# encoding:utf-8
"""
Author: feizhihui
Date: 2020-
"""
import sys
import os
from peft import PeftModel
from tqdm import tqdm
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from aitool import load_excel, dump_excel

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


def get_rst(count_gpu, index_gpu):
    adapter_path = "/mnt/bn/mlxlabzw/llm/data/checkpoint_0912/checkpoint-189000"
    tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan-13B-Chat", use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan-13B-Chat", device_map="auto",  torch_dtype=torch.float16, trust_remote_code=True)
    model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan-13B-Chat")
    model.generation_config.temperature=1

    pmodel = PeftModel.from_pretrained(model, adapter_path, adapter_name="first_lora")
    rst = []
    data = load_excel('./rst_risk_text_1008.xlsx', to_list=True)
    size_task = len(data)//count_gpu
    print('size_task', size_task)
    for line in tqdm(data[size_task*index_gpu:size_task*(index_gpu+1)]):
        ppt = line[2]
        messages = []
        messages.append({"role": "user", "content": ppt})
        # import ipdb
        # ipdb.set_trace()
        response = pmodel.chat(tokenizer, messages)
        line.append(response)
        rst.append(line)
        print(line[0])
        print(line[1])
        print(line[2])
        print(response)
        if len(rst) % 100 == 0:
            dump_excel(rst, './rst_risk_text_1008_with_level_p{}.xlsx'.format(index_gpu))
    dump_excel(rst, './rst_risk_text_1008_with_level_p{}.xlsx'.format(index_gpu))


if __name__ == '__main__':
    get_rst(int(sys.argv[1]),int(sys.argv[2]))
