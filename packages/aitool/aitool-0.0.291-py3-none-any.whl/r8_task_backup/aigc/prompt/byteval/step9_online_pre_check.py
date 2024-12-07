# encoding:utf-8
import requests
import json
from aitool import load_excel, dump_excel
from aitool.r8_task.aigc.prompt.byteval.step10_online_pos_check import identify
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from time import sleep
from threading import Thread


def check_pre(param):
    _cid, _tag, _noise, _risk, _text, q_rst = param
    _pre = identify(_text)
    q_rst.put((_cid, _tag, _noise, _risk, _pre, _text))
    print(_cid, _tag, _noise, _risk, _pre, _text)


def out_file(q_rst):
    old_size = 0
    rst = []
    while True:
        rst.append(q_rst.get())
        rst_size = len(rst)
        if rst_size - old_size >= 10:
            old_size = rst_size
            print('size {}'.format(rst_size))
            dump_excel(rst, './rst_pre_check_1102.xlsx')


if __name__ == '__main__':
    data = load_excel('./rst_noise_1102.xlsx', to_list=True)
    out = [['tag', 'noise', 'risk', 'pre', 'text']]
    query = []
    q_rst = Queue()
    for cid, (tag, noise, risk, text) in tqdm(enumerate(data)):
        query.append((cid, tag, noise, risk, text, q_rst))

    t = Thread(target=out_file, args=(q_rst, ))
    t.start()

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_pre, query)


