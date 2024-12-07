# -*- coding: UTF-8 -*-
from concurrent.futures import ThreadPoolExecutor
from aitool.r8_task.porn.vid2pic import download_save_img

# 输入数据，vid列表，每行一个vid，或用第一列是vid的csv格式
path = "/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/try0830/vids.txt"
# 输出图片的路径，格式为 dst_path/vid/00001.jpg
dst_path = "/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0830_try1/"

# 用于多线程打印进度
r_count = 0
# 用于记录所有图片的路径
rst = []

idx = 0
params = []
with open(path) as fin:
    for line in fin:
        nums = line.split(",", 0)
        try:
            nums = nums[0].strip().strip('"')
            int(nums)
            item_id = nums
        except:
            print(nums)
            continue
        item_id = str(item_id)
        idx += 1
        if idx % 10000 == 0:
            print("running index:", idx)
        params.append((item_id, dst_path))
    print(params[:3])
    print("len of vid to run ", len(params))
    with ThreadPoolExecutor(max_workers=32) as executor:
        executor.map(download_save_img, params)
