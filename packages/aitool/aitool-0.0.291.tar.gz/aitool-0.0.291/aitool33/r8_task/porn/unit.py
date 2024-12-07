# -*- coding: UTF-8 -*-

# 下载图片
from aitool.r8_task.porn.vid2pic import download_save_img
print(download_save_img(('7196209869643386169', './')))

# # 下载视频
from aitool.r8_task.porn.download_video import download_vid
print(download_vid('7196209869643386169', './'))

# 获取视频vv
from aitool.r8_task.porn.get_video_info import vid2video_info
print(vid2video_info('7196209869643386169'))

# 调用pic-porn服务
from aitool.r8_task.porn.porn_image_classifier import pick_out_porn
_rst, _score = pick_out_porn(
    [
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7032507524838411553_00001.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7213202189592857891_00003.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7213352055279324449_00009.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7214429000595180803_00001.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7214442976964054311_00007.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7214473824153226554_00006.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7214474504188251449_00001.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7214506354147478845_00003.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/choose_porn_x_sample_3/7214638085320052008_00004.jpg',
    ],
    model_checkpoint="/mnt/bn/mlxlabzw/xiangyuejia/porn/vit-large-patch16-224-finetuned-eurosat-1218-3-epoch8",
    )
print(_rst, _score)

# 视频抽帧
from aitool.r8_task.porn.video2pic import extract_img
print(extract_img(('./7196209869643386169.mp4', './new_pic/')))