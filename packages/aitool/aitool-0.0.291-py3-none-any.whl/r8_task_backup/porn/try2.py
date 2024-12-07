# -*- coding: UTF-8 -*-
from aitool.r8_task.porn.vit_infer_with_get_pic import infer


infer(
    '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/try0830/vids.txt',  # 每行一个vid
    0,  # 本进程的编号
    3,  # 一共有几个进程
    batch_size=128,
    batch_size_pic=1280,
    pic_dir='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/try0830/pic/',  # 输出图片的路径
    output_prefix='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0828_10_pic_index_rst_p',
    model_checkpoint='/mnt/bn/mlxlabzw/xiangyuejia/porn/swin-tiny-patch4-window7-224-finetuned-eurosat',
)
