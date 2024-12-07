# -*- coding: UTF-8 -*-
from transformers import pipeline
from time import time
from math import ceil
from aitool import dump_lines, load_line, pip_install, make_dir
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from aitool.r8_task.porn.vid2pic import download_save_img


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
        vid_file,  # 每行一个vid
        widx,    # 本进程的编号
        wnum,   # 一共有几个进程
        batch_size=128,
        batch_size_pic=1280,
        time_end=9999999,
        worker=32,
        pic_dir='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0830_try1/',  # 输出图片的路径
        output_prefix='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0828_10_pic_index_rst_p',
        model_checkpoint='/mnt/bn/mlxlabzw/xiangyuejia/porn/swin-tiny-patch4-window7-224-finetuned-eurosat',
):
    begin_time = time()
    check_requirements()
    make_dir(pic_dir)

    classifier = pipeline("r5_image-classification", model=model_checkpoint, device="cuda:0", num_workers=32)

    params = []
    for line in tqdm(load_line(vid_file, separator=','), 'get vid'):
        nums = line[0]
        try:
            nums = nums.strip().strip('"')
            int(nums)
        except:
            # print(nums)
            continue
        item_id = str(nums)
        params.append((item_id, pic_dir))

    num_piece = len(params) // wnum
    params_piece = params[widx*num_piece: (widx+1)*num_piece]
    num_batch_pic = ceil(len(params_piece) // batch_size_pic)
    rst = []
    for nbp in tqdm(range(num_batch_pic), 'num_batch_pic'):
        batch_begin_time = time()
        pp = params_piece[nbp*batch_size_pic: (nbp+1)*batch_size_pic]
        with ThreadPoolExecutor(max_workers=worker) as executor:
            results = executor.map(download_save_img, pp)
        pic_paths = []
        for r in results:
            pic_paths.extend(r)
        print('pics in batch', len(pic_paths))
        batch_download_time = time()
        print('time download: {}'.format(batch_download_time-batch_begin_time))
        outputs = classifier(pic_paths, batch_size=batch_size)
        batch_classifier_time = time()
        print('time classifier: {}'.format(batch_classifier_time-batch_download_time))
        if len(pic_paths) != len(outputs):
            print('bad')
            continue
        for p, s in zip(pic_paths, outputs):
            o = {'noporn': 0, 'porn': 0}
            o[s[0]['label']] = s[0]['score']
            o[s[1]['label']] = s[1]['score']
            if o['porn'] > o['noporn']:
                rst.append(p)
        dump_lines(rst, output_prefix+'{}.txt'.format(widx))
        now_time = time()
        if now_time - begin_time > time_end:
            print('time end')
            exit(0)


if __name__ == '__main__':
    infer(
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/try0830/vids.txt',  # 每行一个vid
        0,  # 本进程的编号
        3,  # 一共有几个进程
        batch_size=128,
        batch_size_pic=160,
        time_end=2400,
        pic_dir='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/try0830/pic1653/',  # 输出图片的路径
        output_prefix='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0830_1653_pic_index_rst_p',
        model_checkpoint='/mnt/bn/mlxlabzw/xiangyuejia/porn/swin-tiny-patch4-window7-224-finetuned-eurosat',
    )