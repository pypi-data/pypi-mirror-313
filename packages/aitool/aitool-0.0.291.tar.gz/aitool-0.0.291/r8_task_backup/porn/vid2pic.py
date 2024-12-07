# -*- coding: UTF-8 -*-
import logging
import os
import shutil
from aitool.r8_task.porn.converter import Converter
from aitool.r8_task.porn.cut_frame_audio_req import frame_audio
import traceback
import cv2

logger = logging.getLogger(__name__)


def download_save_img(param):
    """
    使用视频item_id 通过帧服务获取分帧后结果并下载
    """
    frames_path = None
    show = True
    try:
        item_id = param[0]
        dst_dir = param[1]
        if len(param) >= 3:
            show = param[2]
        else:
            show = True
        converter = Converter()
        res = converter.item_id2url(item_id)
        if len(res) == 0:
            if show:
                print("item_id2url empty")
            return []
        url, vid = res
        try:
            if vid and vid.startswith('v'):
                state_vfs, msg_vfs, frames_path, _ = frame_audio("req_id", vid, url, frame_only=True)
                if state_vfs != 0:
                    if frames_path and os.path.exists(frames_path):
                        shutil.rmtree(frames_path)
                    frames_path = None
            else:
                frames_path = None
        except Exception as e:
            if show:
                s = traceback.format_exc()
                logger.error(e)
                logger.info("[{}] VFS获取异常 {}".format(item_id, s))
                print(e)
                print(s)
            if frames_path and os.path.exists(frames_path):
                shutil.rmtree(frames_path)
            frames_path = None
        if frames_path is None:
            return []
        pic_paths = []
        for i, j in enumerate(sorted(os.listdir(frames_path))):
            img = cv2.imread(os.path.join(frames_path, j))
            dst_img = os.path.join(dst_dir, str(item_id))
            if not os.path.exists(dst_img):
                os.mkdir(dst_img)
            dst_img_dir = os.path.join(dst_img, str(j))
            cv2.imwrite(dst_img_dir, img)
            pic_paths.append(dst_img_dir)
        if show:
            print("vid download img success:", item_id)
        return pic_paths

    except Exception as e:
        if show:
            s = traceback.format_exc()
            print(s)
            print(e)
            logger.error(s)
            logger.error(e)
        return []
    finally:
        if frames_path is not None and os.path.exists(frames_path):
            shutil.rmtree(frames_path)


if __name__ == '__main__':
    from tqdm import tqdm
    from aitool import load_line
    from concurrent.futures import ThreadPoolExecutor

    # 输入数据，vid列表，每行一个vid，或用第一列是vid的csv格式
    path = "/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/try0830/vids.txt"
    # 输出数据，存的图片，格式为 dst_path/vid/00001.jpg
    dst_path = "/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/porn_0830_try1/"

    # 用于多线程打印进度
    r_count = 0
    # 用于记录所有图片的路径
    rst = []

    idx = 0
    params = []
    for line in tqdm(load_line(path, separator=','), 'get vid'):
        nums = line[0]
        try:
            nums = nums.strip().strip('"')
            int(nums)
        except Exception as e:
            print(nums)
            continue
        item_id = str(nums)
        params.append((item_id, dst_path))

    print(params[:3])
    print("len of vid to run ", len(params))

    with ThreadPoolExecutor(max_workers=32) as executor:
        executor.map(download_save_img, params)
