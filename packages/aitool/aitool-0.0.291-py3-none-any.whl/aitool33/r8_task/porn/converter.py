import os
import json
import logging
from urllib.request import urlopen
from aitool import singleton
from aitool.r8_task.idls import PATH as IDLS_PATH
import euler
import thriftpy2
logger = logging.getLogger(__name__)
item_info_service_thrift = thriftpy2.load(os.path.join(IDLS_PATH, 'item_info_service.thrift'),
                                                  module_name="item_info_service_thrift")
base_thrift = thriftpy2.load(os.path.join(IDLS_PATH, 'base.thrift'), module_name="base_thrift")
from base_thrift import Base, BaseResp


@singleton
class Converter:
    def __init__(self):
        self.item_id2vid_client = euler.Client(item_info_service_thrift.ItemInfoService,
                                               "sd://ies.item.info?cluster=online", timeout=5)

    def item_id2vid(self, item_id):
        vid = None
        title = None
        for sub_time in range(3):
            try:
                extra = {"email": "xiangyuejia@bytedance.com"}
                item_info_req = item_info_service_thrift.IdListRequest(
                    Ids=[int(item_id)],
                    Info={"stats": "0"},
                    Base=Base(
                        Caller="ies.efficiency.turing_open_service_decision_blue_army", Extra=extra)
                )
                content = self.item_id2vid_client.GetItem(item_info_req).Items[0].Content
                vid = json.loads(content)
                vu = vid.get('video_id', None)
                title = vid.get('text', None)
                vid = str(vu)
                break
            except IndexError as e:
                pass
            except Exception as e:
                # s = traceback.format_exc()
                # logger.error(s)
                # logger.error(e)
                import traceback
                s = traceback.format_exc()
                print(s)
                print(e)
                vid = None
                title = None
        return vid, title

    def vid2url(self, vid):
        response = urlopen('http://ii.snssdk.com/video/urls/1/toutiao/mp4/{}?nobase64=true&vps=1'.format(vid))
        res = json.loads(response.read().decode('utf-8'))
        url = ''
        video_list = res.get('data', {}).get('video_list', {}).values()
        video_list = sorted(video_list,
                            key=lambda x: x['vwidth'],
                            reverse=True)
        for v in video_list:
            url = v.get('main_url', '')
            if url != '':
                break
        return url

    def item_id2url(self, item_id):
        vid, title = self.item_id2vid(item_id)
        if vid is not None:
            url = self.vid2url(vid)
        else:
            url = None
        return url, vid

    def item_id2images(self, item_id):
        images_urls = []
        for sub_time in range(3):
            try:
                extra = {"email": "xiangyuejia@bytedance.com"}
                item_info_req = item_info_service_thrift.IdListRequest(
                    Ids=[int(item_id)],
                    Info={"stats": "0"},
                    Base=Base(
                        Caller="ies.efficiency.turing_open_service_decision_blue_army", Extra=extra)
                )
                content = self.item_id2vid_client.GetItem(item_info_req).Items[0].Content
                info = json.loads(content)
                images_items = info.get('images', [])
                for images_item in images_items:
                    uri = images_item['uri']
                    url = 'https://tosv.byted.org/obj/' + uri
                    images_urls.append(url)
                break
            except Exception as e:
                # s = traceback.format_exc()
                # logger.error(s)
                # logger.error(e)
                import traceback
                s = traceback.format_exc()
                print(s)
                print(e)
                pass
        return images_urls
