# -*- coding: UTF-8 -*-
from typing import Union, List
from aitool import pip_install, singleton, is_file_exist, is_folder, print_green, print_red
import torch
import time
from random import random
import numpy as np
from transformers import ViTFeatureExtractor, AutoConfig
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import traceback
import logging
logger = logging.getLogger(__name__)

try:
    import laplace as la
except ModuleNotFoundError:
    pip_install('bytedlaplace')
    import laplace as la


@singleton
class PornImageClassifier:
    def __init__(
            self,
            target_yg='sd://ies.efficiency.turing_open_service_porn_image_classifier?idc=yg',
            target_lq='sd://ies.efficiency.turing_open_service_porn_image_classifier?idc=lq',
            model_name='turing_open_service_porn_image_detetor',
            model_checkpoint="/mnt/bn/mlxlabzw/xiangyuejia/porn/vit-large-patch16-224-finetuned-eurosat-1020-3-epoch8",
            feature_extractor=None,
            id2label=None,
            timeout=10,
    ):
        self.model_name = model_name
        self.laplace_yg = la.Client(target_yg, timeout=timeout)
        self.laplace_lq = la.Client(target_lq, timeout=timeout)
        if is_folder(model_checkpoint):
            print_green('load config from: {}'.format(model_checkpoint))
            self.feature_extractor = ViTFeatureExtractor.from_pretrained(model_checkpoint)
            config = AutoConfig.from_pretrained(model_checkpoint)
            self.id2label = config.id2label
            print(config)
        elif feature_extractor is not None and id2label is not None:
            print_green('use inputted feature_extractor and id2label')
            self.feature_extractor = feature_extractor
            self.id2label = id2label
        else:
            print_red('use default config')
            self.feature_extractor = ViTFeatureExtractor(
                do_normalize=True,
                do_rescale=True,
                do_resize=True,
                image_mean=[0.5, 0.5, 0.5],
                image_processor_type='ViTFeatureExtractor',
                image_std=[0.5, 0.5, 0.5],
                resample=2,
                rescale_factor=0.00392156862745098,
                size={'height': 224, 'width': 224},
            )
            self.id2label = {0: 'gory', 1: 'hentai', 2: 'knife', 3: 'noporn', 4: 'porn', 5: 'toxicant'}

    def _fx(self, img):
        return self.feature_extractor(images=img, return_tensors="pt")['pixel_values']

    def pick_out_porn(self, pics: Union[str, List[str]], batch_size=16, worker_num=12, show=False):
        if type(pics) is str:
            pics = [pics]

        rst = []
        rst_score = []
        rst_label = []
        p1 = time.time()
        batch = []
        batch_img = []
        pics_len = len(pics)
        for idx, pic in enumerate(pics):
            if len(batch) >= batch_size:
                batch = []
                batch_img = []
            if not is_file_exist(pic):
                continue
            try:
                img = Image.open(pic)
                batch_img.append(img)
                batch.append(pic)
            except Exception as e:
                print(e)
                continue
            if len(batch_img) != len(batch):
                batch = []
                batch_img = []
                continue
            if len(batch) < batch_size and idx < pics_len-1:
                continue
            p2 = time.time()
            # 单核
            # model_inputs = [feature_extractor(images=img, return_tensors="pt")['pixel_values'] for img in batch_img]
            # 多核
            with ThreadPoolExecutor(max_workers=worker_num) as executor:
                ppt = executor.map(self._fx, batch_img)
            model_inputs = [p for p in ppt]
            inputs = torch.cat(model_inputs, dim=0)
            p3 = time.time()
            failed = False
            inputs = {
                'image': inputs.numpy()
            }
            input_dtypes = {
                'image': np.float32
            }
            for i in range(3):
                try:
                    rand_k = random()
                    if rand_k <= 0.05:
                        results = self.laplace_yg.predict(
                            self.model_name, inputs, input_dtypes=input_dtypes)
                    else:
                        results = self.laplace_lq.predict(
                            self.model_name, inputs, input_dtypes=input_dtypes)
                    failed = False
                    t = torch.from_numpy(results['output'])
                    class_prob_all = torch.softmax(t, dim=-1)
                    class_prob, topclass = torch.max(class_prob_all, dim=1)
                    topclass_str = topclass.numpy().tolist()
                    topclass_str_name = [self.id2label[tc] for tc in topclass_str]
                    class_prob = class_prob.numpy()
                    class_prob = [str(round(a, 3)) for a in class_prob]
                    if len(batch) != len(topclass_str_name):
                        continue
                    for pic, pre_label, prb in zip(batch, topclass_str_name, class_prob):
                        if pre_label == 'noporn':
                            continue
                        rst.append(pic)
                        rst_label.append(pre_label)
                        rst_score.append(prb)
                    break
                except Exception as e:
                    if show:
                        s = traceback.format_exc()
                        print(s)
                        print(e)
                        logger.error(s)
                        logger.error(e)
                    time.sleep(3)
                    failed = True
                    continue
            if failed:
                continue
            p4 = time.time()
            if show:
                print('前处理', p2-p1, '图片特征', p3-p2, '调用接口', p4-p3, '总召回', len(rst))
            p1 = time.time()
        return rst, rst_label, rst_score


def pick_out_porn(pics, show=False, **kwargs):
    porn_classifier = PornImageClassifier(**kwargs)
    return porn_classifier.pick_out_porn(pics, show=show)


if __name__ == '__main__':
    _rst, _score = pick_out_porn([
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1020_hentai/7275726317159517440_1bk5w.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1020_hentai/7275726317159517440_1ckwp.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1020_noporn/7275726317159517440_621.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1020_noporn/7275726317159517440_2007.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1020_porn/7275726317159517440_614.jpg',
        '/mnt/bn/mlxlabzw/xiangyuejia/porn/eval_sample_data_1020_porn/7275726317159517440_2252.jpg',
    ])
    print(_rst, _score)
