# -*- coding: UTF-8 -*-
import os
from aitool import load_lines, split_path, make_dir
from tqdm import tqdm


def shell_cp(source, target):
    try:
        os.system('cp {} {}'.format(source, target))
    except Exception as e:
        print(e)


def cp_pic(pic_file_prefix, out_dir):
    make_dir(out_dir)
    dir_name, full_file_name, file_name, file_ext = split_path(pic_file_prefix)
    data = []
    for k in os.scandir(dir_name):
        file = k.path
        if full_file_name in file:
            print(file)
            data.extend(load_lines(file))
    print('len data', len(data))

    for pic in tqdm(data):
        new_name = pic.replace('/', '_')
        new_name = os.path.join(out_dir, new_name)
        shell_cp(pic, new_name)


if __name__ == '__main__':
    cp_pic(
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0828_10_pic_index_rst',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/candicate_porn_0828_10_pic_index_rst_2/',
    )
