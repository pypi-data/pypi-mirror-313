# -*- coding: UTF-8 -*-
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import load_lines, singleton
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig


@singleton
class Model:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto",
                                                     torch_dtype=torch.float16, trust_remote_code=True)
        self.model.generation_config = GenerationConfig.from_pretrained(model_path)

    def chat(self, history: List[str]):
        messages = []
        for idx, text in enumerate(history):
            if idx % 2 == 0:
                messages.append({"role": "user", "content": text})
            else:
                messages.append({"role": "assistant", "content": text})
        response = self.model.chat(self.tokenizer, messages)
        return response


def infer_baichuan(texts, model_path='baichuan-inc/Baichuan-13B-Chat'):
    """

    :param texts:
    :param model_path:
    :return:

    >>> texts = ['如何学习舞蹈？', '学习舞蹈需要时间、耐心和练习。', '我的时间很少每天只有10分钟，怎么办？']
    >>> infer_baichuan(texts)
    """
    model = Model(model_path)
    response = model.chat(texts)
    return response


if __name__ == '__main__':
    import doctest

    doctest.testmod()
