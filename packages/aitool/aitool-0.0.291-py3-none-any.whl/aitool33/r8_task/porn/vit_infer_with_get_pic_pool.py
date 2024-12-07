# -*- coding: UTF-8 -*-
import time
from math import ceil
from aitool import dump_lines, load_lines, load_line, pip_install, make_dir, get_new_file, split_path, is_file_exist
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from aitool.r8_task.porn.vid2pic import download_save_img
import logging
from time import sleep
from random import randint
import os

def check_requirements():
    try:
        import euler
    except ModuleNotFoundError as e:
        pip_install('bytedeuler==0.42.1')
        import euler
    try:
        import kms
    except ModuleNotFoundError as e:
        pip_install('kms==1.0.1.3')
        import kms
    try:
        import builtwith
    except ModuleNotFoundError as e:
        pip_install('builtwith==1.3.4')
        import builtwith
    try:
        from colorama import Fore
    except ModuleNotFoundError as e:
        pip_install('colorama==0.4.6')
        from colorama import Fore
    try:
        from bs4 import BeautifulSoup
    except ModuleNotFoundError as e:
        pip_install('bs4==0.0.1')
        from bs4 import BeautifulSoup


def infer(
        vid_file_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_vids',      # 每行一个vid
        record_file_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_rcd',    # 记录
        pic_dir_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_pics',
        output_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_rst',
        batch_size=1024,
        batch_size_pic=1600,
        task_size_vid=16000,
        worker=32,
        model_checkpoint='/mnt/bn/mlxlabzw/xiangyuejia/porn/swin-tiny-patch4-window7-224-finetuned-eurosat',
):
    try:
        from transformers import pipeline
    except ModuleNotFoundError as e:
        pip_install('transformers')
        from transformers import pipeline

    make_dir(record_file_path)
    make_dir(pic_dir_path)
    make_dir(output_path)
    check_requirements()
    classifier = pipeline("r5_image-classification", model=model_checkpoint, device="cuda:0", num_workers=32)

    while True:
        _t = time.localtime(time.time())
        currentdate='{}{}{}{}'.format(_t.tm_year, _t.tm_mon, _t.tm_mday, _t.tm_hour)
        vid_file = os.path.join(vid_file_path, currentdate+'.txt')
        if not is_file_exist(vid_file):
            os.system('hdfs dfs -ls hdfs://haruna/home/byte_faceu_qa/data/yuejiaxiang/| sort -rk6,7 | awk \'{print $NF}\' | head -n 1 | xargs -I {} hdfs dfs -ls {} | grep part | awk \'{print $NF}\' | xargs -I {} hdfs dfs -copyToLocal {} '+vid_file)
        if not is_file_exist(vid_file):
            sleep(3+randint(1, 10))
            continue
        # new_vid_file = get_new_file(vid_file_path)[0]
        new_vid_file = vid_file
        record_file = os.path.join(record_file_path, split_path(new_vid_file)[2]+'.rcd')
        pic_dir = os.path.join(pic_dir_path, split_path(new_vid_file)[2]+'/')
        make_dir(pic_dir)
        output_file = os.path.join(output_path, split_path(new_vid_file)[2]+'.txt')
        print(currentdate)
        print(new_vid_file)
        print(record_file)
        print(pic_dir)
        print(output_file)
        logging.info(currentdate)
        logging.info(new_vid_file)
        logging.info(record_file)
        logging.info(pic_dir)
        logging.info(output_file)
        head_line = 0
        if is_file_exist(record_file):
            head_line = int(load_lines(record_file)[0])
            dump_lines([head_line + task_size_vid], record_file)
        else:
            dump_lines([head_line + task_size_vid], record_file)
        print('load vids', new_vid_file, head_line, task_size_vid)
        logging.info('load vids {} {} {}'.format(new_vid_file, head_line, task_size_vid))
        all_vids = load_lines(new_vid_file, separator=',')
        params = []
        for line in all_vids[head_line: head_line+task_size_vid]:
            nums = line[0]
            try:
                nums = nums.strip().strip('"')
                int(nums)
            except:
                continue
            item_id = str(nums)
            params.append((item_id, pic_dir))
        if len(params) == 0:
            sleep(3+randint(1, 10))
            continue

        num_batch_pic = ceil(len(params) // batch_size_pic)

        for nbp in tqdm(range(num_batch_pic), 'num_batch_pic'):
            rst = []
            batch_begin_time = time.time()
            pp = params[nbp*batch_size_pic: (nbp+1)*batch_size_pic]
            with ThreadPoolExecutor(max_workers=worker) as executor:
                results = executor.map(download_save_img, pp)
            pic_paths = []
            for r in results:
                pic_paths.extend(r)
            if len(pic_paths) == 0:
                continue
            print('pics in batch', len(pic_paths))
            logging.info('pics in batch {}'.format(len(pic_paths)))
            batch_download_time = time.time()
            print('time download {}'.format(batch_download_time-batch_begin_time))
            logging.info('time download {}'.format(batch_download_time-batch_begin_time))
            outputs = classifier(pic_paths, batch_size=batch_size)
            batch_classifier_time = time.time()
            print('time classifier {}'.format(batch_classifier_time-batch_download_time))
            logging.info('time classifier {}'.format(batch_classifier_time-batch_download_time))
            if len(pic_paths) != len(outputs):
                print('bad')
                continue
            for p, s in zip(pic_paths, outputs):
                o = {'noporn': 0, 'porn': 0}
                o[s[0]['label']] = s[0]['score']
                o[s[1]['label']] = s[1]['score']
                if o['porn'] > o['noporn']:
                    rst.append(p)
            if len(rst) > 0:
                print('find new pic ', len(rst))
                logging.info('find new pic {}'.format(len(rst)))
                all_rst = []
                if is_file_exist(output_file):
                    all_rst = load_lines(output_file)
                all_rst.extend(rst)
                dump_lines(all_rst, output_file)
                print(output_file, len(all_rst))
                logging.info('{} {}'.format(output_file, len(all_rst)))


if __name__ == '__main__':
    infer()
