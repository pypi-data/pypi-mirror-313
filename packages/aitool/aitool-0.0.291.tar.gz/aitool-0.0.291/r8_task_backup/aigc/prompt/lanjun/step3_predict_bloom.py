import torch
import sys
from tqdm import tqdm
from aitool import load_pickle, dump_pickle, dump_excel
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from transformers import BloomTokenizerFast, BloomForCausalLM

def get_rst(count_gpu, index_gpu):
    data = load_pickle('/mnt/bn/mlxlabzw/llm/Baichuan-13B/prompts_lanjun_compare_1129.pkl')
    # tokenizer = AutoTokenizer.from_pretrained("bigscience/bloomz-7b1")
    # model = AutoModelForCausalLM.from_pretrained("bigscience/bloomz-7b1", device_map="auto", torch_dtype='auto')
    tokenizer = BloomTokenizerFast.from_pretrained('Langboat/bloom-6b4-zh')
    model = BloomForCausalLM.from_pretrained('Langboat/bloom-6b4-zh')

    rst = []
    size_task = len(data)//count_gpu
    print('size_task', size_task)
    idx = 0
    for line in tqdm(data[size_task*index_gpu:size_task*(index_gpu+1)]):
        try:
            # p = line
            # print('>>> input')
            # print(p)
            # inputs = tokenizer.encode(p, return_tensors="pt").to("cuda")
            # outputs = model.generate(inputs, max_length=200)
            # response = tokenizer.decode(outputs[0])
            inputs = tokenizer.encode(line, return_tensors='pt')
            outputs = model.generate(inputs)
            response = tokenizer.batch_decode(outputs)

            import ipdb
            ipdb.set_trace()
            print('>>> output')
            print(response)
            rst.append([line, response])
            idx += 1
            if idx % 100 == 0:
                dump_pickle(rst, 'rst_prompts_lanjun_compare_bloomz_1129_p{}.pkl'.format(index_gpu))
        except Exception as e:
            print(e)
    dump_pickle(rst, 'rst_prompts_lanjun_compare_bloomz_1129_p{}.pkl'.format(index_gpu))
    dump_excel(rst, 'rst_prompts_lanjun_compare_bloomz_1129_p{}.xlsx'.format(index_gpu))


if __name__ == '__main__':
    get_rst(int(sys.argv[1]),int(sys.argv[2]))
