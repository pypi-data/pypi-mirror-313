# -*- coding: UTF-8 -*-
from aitool.r8_task.porn.vit_infer_with_get_pic_pool_v2 import infer
infer(
    task_size_vid=1600,
    worker_vid2pic=8,
    worker_pic2porn=8,
    show=False,
    model_checkpoint="/mnt/bn/mlxlabzw/xiangyuejia/porn/vit-large-patch16-224-finetuned-eurosat-1218-3-epoch8",
)
