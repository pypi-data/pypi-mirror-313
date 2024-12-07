from PIL import Image
from aitool import get_file, split_path, load_csv, is_file_exist, load_lines, dump_lines, make_dir, random_base64
from random import sample
import os
from transformers import AutoImageProcessor, ViTForImageClassification
import torch
from datasets import load_dataset
from transformers import pipeline
from tqdm import tqdm

f_name = "/mnt/bn/mlxlabzw/code/jupyter_notebooks/libs/im_porn_data/imges_12"
# output
path_porn = '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1213_porn'
path_noporn = '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1213_noporn'
path_hentai = '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1213_hentai'
path_gory = '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1213_gory'
path_knife = '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1213_knife'
path_toxicant = '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1213_toxicant'
make_dir(path_porn, is_dir=True)
make_dir(path_noporn, is_dir=True)
make_dir(path_hentai, is_dir=True)
make_dir(path_gory, is_dir=True)
make_dir(path_knife, is_dir=True)
make_dir(path_toxicant, is_dir=True)
# model
model_checkpoint = "/mnt/bn/mlxlabzw/xiangyuejia/porn/vit-large-patch16-224-finetuned-eurosat-1213-3-epoch8"


def shell_cp(source, target) -> None:
    try:
        os.system('cp {} {}'.format(source, target))
    except Exception as e:
        print(e)


log_data = []
porn_rst = []
noporn_rst = []
with torch.no_grad():
    classifier = pipeline("image-classification", model=model_checkpoint, device="cuda:0")
    print(classifier.model.config)
    batch_size = 100
    len_porn_rst = 0
    batch = []
    batch_img = []
    for k in os.scandir(f_name):
        vid = k.path
        len_porn_rst = len(porn_rst)
        print(vid)
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

        try:
            outputs = classifier(batch_img, top_k=1, batch_size=batch_size)
        except Exception as e:
            print(e)
        print('len batch', len(batch))
        print('len outputs', len(outputs))
        oss = set([_[0]['label'] for _ in outputs])
        for v, o in zip(batch, outputs):
            log_data.append(['{}'.format(v), '{}'.format(o[0])])
            if o[0]['label'] == 'porn':
                dir_name, full_file_name, file_name, file_ext = split_path(v)
                new_pic_name = os.path.join(path_porn, random_base64() + '.' + file_ext)
                print('porn', new_pic_name)
                shell_cp(v, new_pic_name)
            elif o[0]['label'] == 'gory':
                dir_name, full_file_name, file_name, file_ext = split_path(v)
                new_pic_name = os.path.join(path_gory, random_base64() + '.' + file_ext)
                print('gory', new_pic_name)
                shell_cp(v, new_pic_name)
            elif o[0]['label'] == 'hentai':
                dir_name, full_file_name, file_name, file_ext = split_path(v)
                new_pic_name = os.path.join(path_hentai, random_base64() + '.' + file_ext)
                print('hentai', new_pic_name)
                shell_cp(v, new_pic_name)
            elif o[0]['label'] == 'knife':
                dir_name, full_file_name, file_name, file_ext = split_path(v)
                new_pic_name = os.path.join(path_knife, random_base64() + '.' + file_ext)
                print('knife', new_pic_name)
                shell_cp(v, new_pic_name)
            elif o[0]['label'] == 'toxicant':
                dir_name, full_file_name, file_name, file_ext = split_path(v)
                new_pic_name = os.path.join(path_toxicant, random_base64() + '.' + file_ext)
                print('toxicant', new_pic_name)
                shell_cp(v, new_pic_name)
        if len(porn_rst) != len_porn_rst:
            dump_lines(porn_rst, 'log_fine_tuning_eval7_1211_true_porn.txt')

