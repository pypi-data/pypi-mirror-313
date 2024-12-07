# -*- coding: UTF-8 -*-
# 调用pic-porn服务
from aitool.task_customized.porn.porn_image_classifier import pick_out_porn
from aitool import dump_lines, make_dir, get_file, is_file_exist, split_path
import os
import time
from tqdm import tqdm

# input
f_name = "/mnt/bn/mlxlabzw/code/jupyter_notebooks/libs/im_porn_data/imges"
# output
path_porn = '/mnt/bn/mlxlabzw/xiangyuejia/porn/test_case_porn_1211'
path_noporn = '/mnt/bn/mlxlabzw/xiangyuejia/porn/test_case_noporn_1211'
make_dir(path_porn, is_dir=True)
make_dir(path_noporn, is_dir=True)


def shell_cp(source, target) -> None:
    try:
        os.system('cp {} {}'.format(source, target))
    except Exception as e:
        print(e)


def call(process_num, process_idx):
    porn_rst = []
    noporn_rst = []
    batch_size = 16
    worker_num = 12
    batch = []
    batch_img = []
    print('batch_size', batch_size, 'worker_num', worker_num, 'process_num', process_num, 'process_idx', process_idx)

    p1 = time.time()
    pic_path = []
    for vid in get_file(f_name):
        pic_path.append(vid)
    pic_path.sort()
    len_pic = len(pic_path) // process_num
    print('process', process_idx*len_pic, (process_idx+1)*len_pic)
    pic_path_idx = pic_path[process_idx*len_pic: (process_idx+1)*len_pic]
    dump_lines(pic_path_idx, 'processed_pic_1213_{}.txt'.format(process_idx))

    out_len = 0
    for vid in tqdm(pic_path_idx):
        len_porn_rst = len(porn_rst)
        if len(batch) >= batch_size:
            batch = []
        if not is_file_exist(vid):
            continue
        batch.append(vid)
        if len(batch) < batch_size:
            continue
        try:
            _rst, _score = pick_out_porn(batch)
            print(_rst, _score)
            for pic in _rst:
                dir_name, full_file_name, file_name, file_ext = split_path(pic)
                dir_name_last = dir_name.split('/')[-1]
                new_pic_name = os.path.join(path_porn, dir_name_last + '_' + full_file_name)
                porn_rst.append(new_pic_name)
                if len(porn_rst) % 100 == 0:
                    print('len porn_pic', len(porn_rst))
                shell_cp(pic, new_pic_name)
            time.sleep(0.1)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    import sys
    p_num = int(sys.argv[1])
    p_idx = int(sys.argv[2])
    call(p_num, p_idx)
