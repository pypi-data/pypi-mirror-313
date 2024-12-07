# -*- coding: UTF-8 -*-
import torch
import sys
from tqdm import tqdm
from aitool import load_pickle, dump_pickle, send_file2tos
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig


def get_rst(count_gpu, index_gpu):
    data = load_pickle('./prompts_1029.pkl')
    tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan-13B-Chat", use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan-13B-Chat", device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
    model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan-13B-Chat")

    rst = []
    size_task = len(data)//count_gpu
    print('size_task', size_task)
    idx = 0
    for line in tqdm(data[size_task*index_gpu:size_task*(index_gpu+1)]):
        try:
            p = line[-1]
            print('>>> input')
            print(p)
            messages = []
            messages.append({"role": "user", "content": p})
            response = model.chat(tokenizer, messages)
            print('>>> output')
            print(response)
            line.append(response)
            rst.append(line)
            idx += 1
            if idx % 1000 == 0 or idx == size_task:
                dump_pickle(rst, 'prompts_rst_shengxi_1029_p{}.pkl'.format(index_gpu))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    get_rst(int(sys.argv[1]),int(sys.argv[2]))
