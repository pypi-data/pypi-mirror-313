# -*- coding: UTF-8 -*-
import os
from aitool import load_lines, split_path, make_dir, get_file
from tqdm import tqdm


def shell_cp(source, target):
    try:
        os.system('cp {} {}'.format(source, target))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    out_file = '/Users/bytedance/Downloads/merlin/pos_new'
    idx = 5163
    for file in get_file('/Users/bytedance/Downloads/merlin/pos'):
        shell_cp(file, os.path.join(out_file, 'porn_{}.jpg'.format(idx)))
        idx += 1
