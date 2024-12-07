# -*- coding: UTF-8 -*-
from aitool import pip_install, mkdir
import os
import glob


try:
    import cv2
except ModuleNotFoundError:
    pip_install('opencv-python')
    import cv2


def download_video(url, video_path):
    os.system('wget "{}" -O {}'.format(url, video_path))


def get_all_mp4(video_path):
    glob.glob(os.path.join(video_path, "*.mp4"))


def save_img(param):
    # video_path 必须是.mp4的视频
    # video_path 的视频名会建一个子文件夹
    out_pics = []
    video_path, pic_path = param
    subname = video_path.split('/')[-1]
    subname = subname.replace('.mp4', '')
    vc = cv2.VideoCapture(video_path)
    # 总帧数
    frames_num = vc.get(7)
    # 抽取间隔, 最少15帧间隔
    timeF = max(frames_num // 15, 15)
    c = 1
    if vc.isOpened():
        rval, frame = vc.read()
        mkdir(os.path.join(pic_path, subname))
    else:
        rval = False
    while rval:
        rval, frame = vc.read()
        if (c % timeF == 0):
            if frame is not None:
                _pth = os.path.join(pic_path, subname, str(c) + '.jpg')
                print(_pth)
                cv2.imwrite(_pth, frame)
                out_pics.append(_pth)
        c = c + 1
        if c >= timeF * 15:
            break
        cv2.waitKey(1)
    vc.release()
    return out_pics


def extract_img(param):
    return save_img(param)

def save_key_img(param):
    from Katna.video import Video  # pip install Katna
    from Katna.writer import KeyFrameDiskWriter
    video_path, pic_path = param
    subname = video_path.split('/')[-1]
    subname = subname.replace('.mp4', '')
    _pth = os.path.join(pic_path, subname)
    # initialize video module
    vd = Video()
    # number of images to be returned
    no_of_frames_to_returned = 12
    # initialize diskwriter to save data at desired location
    diskwriter = KeyFrameDiskWriter(location=_pth)
    # extract keyframes and process data with diskwriter
    vd.extract_video_keyframes(
        no_of_frames=no_of_frames_to_returned, file_path=video_path,
        writer=diskwriter
    )


if __name__ == '__main__':
    import sys
    from tqdm import tqdm
    from aitool import make_dir
    from concurrent.futures import ThreadPoolExecutor

    p_num = int(sys.argv[1])
    p_idx = int(sys.argv[2])

    video_path = '/mnt/bn/mlxlabzw/code/jupyter_notebooks/porn/tmpdata/may_porn_0925/'
    pic_path = '/mnt/bn/mlxlabzw/xiangyuejia/porn/video2pic_0925_may_porn/'
    make_dir(pic_path)

    query = []
    for video in tqdm(os.scandir(video_path)):
        query.append((video.path, pic_path))
    print(len(query))
    query.sort()
    p_len = len(query) // p_num
    query_p = query[p_idx * p_len:(p_idx + 1) * p_len]
    worker = 16
    with ThreadPoolExecutor(max_workers=worker) as executor:
        results = executor.map(save_img, query_p)
