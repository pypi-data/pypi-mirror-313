# encoding=utf-8
import os
import requests
import numpy as np
import time
import shutil
import tempfile
import logging.config
from aitool.r8_task.porn.vfs import VideoFingerPrintingService

logger = logging.getLogger(__name__)


def download_frames(vfs, frames_path, req_id, video_id, url):
    start = time.time()
    try:
        frame_res = vfs.get_audit_frames(video_id)

        if frame_res is None:
            logger.info("[VFS][{}][{}] Fail to get audit frame info!".format(req_id, video_id))
            raise ValueError(f"Fail to get audit frame info!")

        if frame_res["status_code"] == 273007:
            raise ValueError("[VFS][{}][{}] no permission, frame_res['status_code'] == 273007".format(req_id, video_id))

        frame_list = sorted(frame_res["frame_list"].items(), key=lambda x: x[0])
        pre_frame_time = -100
        cnt = 0
        for frame_index, frame_info in frame_list:
            frame_url = frame_info["download_url"]
            frame_time = frame_info["cut_time"]
            if int(frame_time) == pre_frame_time:
                pre_frame_time = int(frame_time)
                continue
            try:
                r = requests.get(frame_url, timeout=4)
                frame_path = os.path.join(frames_path, "{:0>5d}.jpg".format(cnt))
                with open(frame_path, "wb") as fw:
                    fw.write(r.content)
                cnt += 1
            except Exception as e:
                import traceback
                s = traceback.format_exc()
                print(s)
                print(e)
                # s = traceback.format_exc()
                # logger.info("[VFS][{}][{}] failed to get video frame! {}".format(req_id, video_id, s))
                continue
        end = time.time()
        # logger.info("[VFS][{}][{}] 视频帧服务获取成功, cost {} seconds".format(req_id, video_id, str(end - start)))
        return 0, "success", frames_path
    except Exception as e:
        import traceback
        s = traceback.format_exc()
        print(s)
        print(e)
        end = time.time()
        # s = traceback.format_exc()
        s = ''
        logger.info("[VFS][{}][{}] 视频帧服务获取失败, 异常原因 [{}] cost {} seconds".format(req_id, video_id, s, str(end - start)))
        return -1, f"[视频帧服务获取失败] [{s}] [cost {str(end - start)} seconds]", frames_path


def download_audio(vfs, req_id, video_id, url):
    start_time = time.time()
    try:
        audio_res = vfs.get_audit_audio(video_id)

        if audio_res is None:
            logger.info("[VFS][{}][{}] Fail to get audio info!".format(req_id, video_id))
            raise ValueError("[VFS][{}][{}] Fail to get audio info!".format(req_id, video_id))

        audio_path = os.path.abspath(video_id + ".{}".format('wav'))
        audio_url = audio_res["download_url"]

        r = requests.get(audio_url, stream=True)
        with open(audio_path, "wb") as file:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
        end = time.time()
        # logger.info("[VFS][{}][{}] 音频服务获取成功 cost {} seconds".format(req_id, video_id, str(end - start_time)))
        return 0, "success", audio_path
    except Exception as e:
        import traceback
        s = traceback.format_exc()
        print(s)
        print(e)
        end = time.time()
        # s = traceback.format_exc()
        s = ''
        logger.info("[VFS][{}][{}] 音频服务获取失败 异常原因 {} cost {} seconds".format(req_id, video_id, s, str(end - start_time)))
        return -1, f"[音频服务获取失败] [{s}] [cost {str(end - start_time)} seconds]", None


def frame_audio(ReqID, video_id, url, frame_only=False):
    '''
    state 0 都成功
          -1 都不成功
          1 抽帧不成功
          2 抽音频不成功
    '''
    frames_path = None
    audio_path = None
    state = 0
    start_time = time.time()
    try:
        caller = "ies.efficiency.douyin_eco_audit_service"
        ak = '634b738e8fb2dd82483c202b606b8f7b'
        sk_kms_key = "iam_sk"
        sk = 'e675321771ba6524f2dd8d6ba7b59f87'
        kms_region = "cn"

        t_file = tempfile.mkdtemp(prefix=ReqID + '_', dir='./')
        vfs = VideoFingerPrintingService(caller, ak, sk_kms_key, sk, kms_region)
        state_frame, msg_frame, frames_path = download_frames(vfs, t_file, ReqID, video_id, url)
        if frame_only:
            return state_frame, msg_frame, frames_path, None
        state_audio, msg_audio, audio_path = download_audio(vfs, ReqID, video_id, url)
        if state_frame != 0 and state_audio != 0:
            state = -1
            raise ValueError(f"[{msg_frame}] [{msg_audio}]")
        if state_frame != 0:
            state = 1
            raise ValueError(f"[{msg_frame}] [success]")
        if not os.path.exists(frames_path):
            state = 1
            raise ValueError(f"[{frames_path} 不存在] [success]")
        if len(os.listdir(frames_path)) == 0:
            state = 1
            raise ValueError(f"[{frames_path} 无图片] [success]")

        if state_audio != 0:
            state = 2
            raise ValueError(f"[success] [{msg_audio}]")
        end = time.time()
        # logger.info("[VFS][{}][{}] 抽帧与音频服务获取成功 cost {} seconds".format(ReqID, video_id, str(end - start_time)))
        return state, "success", frames_path, audio_path
    except Exception as e:
        import traceback
        s = traceback.format_exc()
        print(s)
        print(e)
        if state != 0:
            if frames_path is not None and os.path.exists(frames_path):
                shutil.rmtree(frames_path)
                frames_path = None
        end = time.time()
        # s = traceback.format_exc()
        s = ''
        logger.info("[VFS][{}][{}] 抽帧音频服务获取失败 异常原因 [{}] cost {} seconds".format(ReqID, video_id, s, str(end - start_time)))
        return state, f"[抽帧音频服务获取失败] [{s}] [cost {str(end - start_time)} seconds]", frames_path, audio_path


if __name__ == "__main__":
    vid = "v0200fg10000c4frbprc77u5u16kajpg"
    frame_audio("12", vid, "url")
