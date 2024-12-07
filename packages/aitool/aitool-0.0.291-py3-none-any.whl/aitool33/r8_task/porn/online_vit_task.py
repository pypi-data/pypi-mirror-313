# -*- coding: UTF-8 -*-
from aitool import get_file, is_file_exist, split_path, send_file2tos, send_feishu_msg, make_dir
import os
import torch
from tqdm import tqdm
import laplace as la
import time
import numpy as np
from transformers import ViTFeatureExtractor, AutoConfig
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# 服务
target = 'sd://ies.efficiency.turing_open_service_porn_image_classifier?idc=yg'
model_name = 'turing_open_service_porn_image_detetor'
laplace = la.Client(target, timeout=10)
# input
f_name = "/mnt/bn/mlxlabzw/xiangyuejia/porn/video2pic_0925_may_porn/"
# output
path_porn = '/mnt/bn/mlxlabzw/xiangyuejia/porn/test_case_porn_0925'
path_noporn = '/mnt/bn/mlxlabzw/xiangyuejia/porn/test_case_noporn_0925'
make_dir(path_porn)
make_dir(path_noporn)
# model_feature_extractor
model_checkpoint = "/mnt/bn/mlxlabzw/xiangyuejia/porn/vit-large-patch16-224-finetuned-eurosat-0914-3-epoch8"
feature_extractor = ViTFeatureExtractor.from_pretrained(model_checkpoint)
config = AutoConfig.from_pretrained(model_checkpoint)
id2label = config.id2label
print(config)


def _fx(img):
    return feature_extractor(images=img, return_tensors="pt")['pixel_values']


def shell_cp(source, target) -> None:
    try:
        os.system('cp {} {}'.format(source, target))
    except Exception as e:
        print(e)


def call(process_num, process_idx):
    log_data = []
    porn_rst = []
    noporn_rst = []
    batch_size = 16
    worker_num=12
    batch = []
    batch_img = []
    print('batch_size', batch_size, 'worker_num', worker_num, 'process_num', process_num, 'process_idx', process_idx)

    p1 = time.time()
    pic_path = []
    for vid_dir in tqdm(os.scandir(f_name)):
        for vid in get_file(vid_dir.path):
            pic_path.append(vid)
    pic_path.sort()
    len_pic = len(pic_path) // process_num
    print('process', process_idx*len_pic, (process_idx+1)*len_pic)
    pic_path_idx = pic_path[process_idx*len_pic: (process_idx+1)*len_pic]

    out_len = 0
    for vid in tqdm(pic_path_idx):
        len_porn_rst = len(porn_rst)
        if len(batch) >= batch_size:
            batch = []
            batch_img = []
        if not is_file_exist(vid):
            continue
        try:
            img = Image.open(vid)
            batch_img.append(img)
            batch.append(vid)
        except Exception as e:
            print(e)
            continue
        if len(batch_img) != len(batch):
            batch = []
            batch_img = []
            continue
        if len(batch) < batch_size:
            continue
        p2 = time.time()
        # model_inputs = [feature_extractor(images=img, return_tensors="pt")['pixel_values'] for img in batch_img]
        with ThreadPoolExecutor(max_workers=worker_num) as executor:
            ppt = executor.map(_fx, batch_img)
        model_inputs = [p for p in ppt]
        inputs = torch.cat(model_inputs, dim=0)
        p3 = time.time()
        failed = False
        inputs = {
            'r5_image': inputs.numpy()
        }
        input_dtypes = {
            'r5_image': np.float32
        }
        for i in range(3):
            try:
                results = laplace.predict(
                    model_name, inputs, input_dtypes=input_dtypes)
                failed = False
                break
            except Exception as e:
                print(e)
                time.sleep(3)
                failed = True
                continue
        if failed:
            continue
        p4 = time.time()

        t = torch.from_numpy(results['output'])
        class_prob_all = torch.softmax(t, dim=-1)
        class_prob, topclass = torch.max(class_prob_all, dim=1)
        topclass_str = topclass.numpy().tolist()
        topclass_str_name = [id2label[tc] for tc in topclass_str]
        class_prob = class_prob.numpy()
        class_prob = [str(round(a, 3)) for a in class_prob]
        if len(batch) != len(topclass_str_name):
            continue
        for pic, pre_label, prb in zip(batch, topclass_str_name, class_prob):
            if pre_label == 'noporn':
                continue
            dir_name, full_file_name, file_name, file_ext = split_path(pic)
            dir_name_last = dir_name.split('/')[-1]
            new_pic_name = os.path.join(path_porn, dir_name_last + '_' + full_file_name)
            porn_rst.append(new_pic_name)
            if len(porn_rst) % 100 == 0:
                print('len porn_pic', len(porn_rst))
            shell_cp(pic, new_pic_name)
        p5 = time.time()
        print('前处理', p2-p1, '图片特征', p3-p2, '调用接口', p4-p3, '后处理', p5-p4, '总召回', len(porn_rst))
        p1 = time.time()
        if len(porn_rst)>0 and len(porn_rst) % 500 == 0 and out_len != len(porn_rst):
            try:
                out_len = len(porn_rst)
                print('zip -rq {}_p{}_len{}.zip {}'.format(path_porn, process_idx, len(porn_rst), path_porn))
                os.system('zip -rq {}_p{}_len{}.zip {}'.format(path_porn, process_idx, len(porn_rst), path_porn))
                tos_name = '{}_p{}_len{}.zip'.format(path_porn, process_idx, len(porn_rst)).split('/')[-1]
                print(send_file2tos('{}_p{}_len{}.zip'.format(path_porn, process_idx, 'may_porn'+tos_name, len(porn_rst)), name='porn'))
                send_feishu_msg('http://tosv.byted.org/obj/ies-turing-pornmarketing/{}'.format(tos_name), group_id='7277501750155198467')
            except Exception as e:
                print(e)

    print('zip -rq {}_p{}_len{}.zip {}'.format(path_porn, process_idx, len(porn_rst), path_porn))
    os.system('zip -rq {}_p{}_len{}.zip {}'.format(path_porn, process_idx, len(porn_rst), path_porn))
    tos_name = '{}_p{}_len{}.zip'.format(path_porn, process_idx, len(porn_rst)).split('/')[-1]
    print(send_file2tos('{}_p{}_len{}.zip'.format(path_porn, process_idx, 'may_porn'+tos_name, len(porn_rst)), name='porn'))
    send_feishu_msg('http://tosv.byted.org/obj/ies-turing-pornmarketing/{}'.format(tos_name), group_id='7277501750155198467')


if __name__ == '__main__':
    import sys
    p_num = int(sys.argv[1])
    p_idx = int(sys.argv[2])
    call(p_num, p_idx)
