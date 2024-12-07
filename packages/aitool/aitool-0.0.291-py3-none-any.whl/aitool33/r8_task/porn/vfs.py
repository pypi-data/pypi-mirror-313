#!/usr/bin/env python
# encoding: utf-8
import euler
import kms
from aitool.r8_task.porn.sign import *
import logging.config
logger = logging.getLogger(__name__)
from aitool.r8_task.idls import base_thrift, guldan_thrift, vaudio_thrift


class VideoFingerPrintingService():
    def __init__(self, caller, ak, sk_kms_key, sk=None, kms_region="cn"):
        self.caller = caller
        self.ak = ak
        self.sk_kms_key = sk_kms_key

        # var client & base
        self.client = euler.Client(guldan_thrift.GuldanService, target='sd://toutiao.videoarch.guldan',
                                   transport="buffered")

        if sk is None:
            try:
                kclient = kms.KMSClient(caller)
                sk = kclient.get_config_by_name(sk_kms_key, kms_region)["result"]
            except Exception as e:
                # logger.info(e)
                import traceback
                s = traceback.format_exc()
                print(s)
                print(e)
                return
            logger.info(sk)
        self.sk = sk

        extra = {"email": "xiangyuejia@bytedance.com"}
        self.base = base_thrift.Base(
            Caller=self.caller,
            Extra=extra,
        )

    def _reconnect(self):
        self.client = euler.Client(guldan_thrift.GuldanService, target='sd://toutiao.videoarch.guldan',
                                   transport="buffered")

    def get_audit_frames(self, vid, retry=3):
        method = 'GetAuditFrames'
        extra = {
            'vid': vid
        }
        sig = sign_rpc_request(self.ak, self.sk, method, self.caller, extra=extra)

        req = guldan_thrift.GetAuditFramesRequest(
            Vid=vid,
            IdentityInfo=sig,
            MinFrameNum=10,
            Base=self.base
        )

        for i in range(retry):
            try:
                resp = self.client.GetAuditFrames(req)
                break
            except Exception as e:
                # logger.info(e)
                import traceback
                s = traceback.format_exc()
                print(s)
                print(e)
                self._reconnect()
                resp = None

        if resp is None or resp.BaseResp.StatusCode != 0:  # 请求失败
            if resp.BaseResp.StatusCode == 273007:
                logger.info("No permission, vid=%s" % (vid))
                return {"status_code": resp.BaseResp.StatusCode}
            else:
                # logger.info()("get_audit_frames failed, StatusCode=%d, StatusMessage=%s" %(resp.BaseResp.StatusCode, resp.BaseResp.StatusMessage))
                logger.info("get_audit_frames failed, vid=%s, StatusCode=%d, StatusMessage=%s" % (
                vid, resp.BaseResp.StatusCode, resp.BaseResp.StatusMessage))
            return None

        res = {
            "status_code": resp.BaseResp.StatusCode,
            "frame_list": {}
        }

        frames = resp.Frames
        for frame in frames:
            res["frame_list"][frame.FrameNo] = {
                "cut_time": frame.CutTime,
                "width": frame.Width,
                "height": frame.Height,
                "download_url": frame.DownloadURL
            }

        return res

    def get_audit_audio(self, vid, retry=3):
        method = 'GetAudio'
        extra = {
            'vid': vid
        }
        sig = sign_rpc_request(self.ak, self.sk, method, self.caller, extra=extra)

        extra = {"email": "xiangyuejia@bytedance.com"}
        req = guldan_thrift.GetAudioRequest(
            Vid=vid,
            IdentityInfo=sig,
            Base=self.base,
            Extra=extra,
        )

        for i in range(retry):
            try:
                resp = self.client.GetAudio(req)
                break
            except Exception as e:
                # logger.info(e)
                import traceback
                s = traceback.format_exc()
                print(s)
                print(e)
                self._reconnect()
                resp = None

        if resp is None or resp.BaseResp.StatusCode != 0:  # 请求失败
            # logger.info()("get_audit_audio failed, StatusCode=%d, StatusMessage=%s" %(resp.BaseResp.StatusCode, resp.BaseResp.StatusMessage))
            logger.info("get_audit_audio failed, vid=%s, StatusCode=%d, StatusMessage=%s" % (
            vid, resp.BaseResp.StatusCode, resp.BaseResp.StatusMessage))
            return None

        res = {
            "download_url": resp.DownloadURL
        }

        return res


