# -*- coding: UTF-8 -*-
import time
from aitool import dump_lines, load_lines, get_file_etime, pip_install, make_dir, send_feishu_sheet, split_path, \
    is_file_exist, dump_csv, load_csv, get_log, format_time
from tqdm import tqdm
from aitool.r8_task.porn.vid2pic import download_save_img
from aitool.r8_task.porn.porn_image_classifier import pick_out_porn
from aitool.r8_task.porn.get_video_info import vid2video_info
import logging
from time import sleep
from random import randint
import os
from queue import Queue
from threading import Thread
import traceback
logger = logging.getLogger(__name__)


def check_requirements():
    try:
        import euler
    except ModuleNotFoundError as e:
        pip_install('bytedeuler==0.42.1')
        import euler
    try:
        import kms
    except ModuleNotFoundError as e:
        pip_install('kms==1.0.1.3')
        import kms
    try:
        import builtwith
    except ModuleNotFoundError as e:
        pip_install('builtwith==1.3.4')
        import builtwith
        import builtwith
    try:
        from colorama import Fore
    except ModuleNotFoundError as e:
        pip_install('colorama==0.4.6')
        from colorama import Fore
    try:
        from bs4 import BeautifulSoup
    except ModuleNotFoundError as e:
        pip_install('bs4==0.0.1')
        from bs4 import BeautifulSoup


def query_vid2pic(q_vids, q_imgs, idx, show):
    # 现在的时间
    while True:
        try:
            vid, pic_dir = q_vids.get()
            pic_paths = download_save_img((vid, pic_dir, show))
            for path in pic_paths:
                q_imgs.put(path)
                if show:
                    print('query_vid2pic', 'idx', idx, 'vid', vid, 'path', path)
        except Exception as e:
            if show:
                s = traceback.format_exc()
                print(s)
                print(e)
                get_log('vid2pic').error('{}'.format(s))
                get_log('vid2pic').error('{}'.format(e))


def query_vid2video(out_q):
    pass


def video2pic(out_q):
    pass


def query_pic2porn(q_imgs, q_porn, idx, show, model_checkpoint):
    while True:
        try:
            pics = []
            while len(pics) < 16:
                p_path = q_imgs.get()
                pics.append(p_path)
            porn_pic, porn_label, porn_score = pick_out_porn(pics, show=show, model_checkpoint=model_checkpoint)
            for pic, lb, scr in zip(porn_pic, porn_label, porn_score):
                q_porn.put((pic, lb, scr))
                if show:
                    print('query_pic2porn', idx, pic, lb, scr)
                    logging.info('query_pic2porn {} {} {} {}'.format(idx, pic, lb, scr))
        except Exception as e:
            if show:
                s = traceback.format_exc()
                print(s)
                print(e)
                get_log('pic2porn').error('{}'.format(s))
                get_log('pic2porn').error('{}'.format(e))


def reporter(_dir, _record_file, _current_date):
    # 现在的时间
    now_time = time.time()
    # 获取dir目录下所有文件的编辑时间
    fet = get_file_etime(_dir)
    # 加载record_file（记录了哪些结果已经报出过）
    file_reported = set()
    if is_file_exist(_record_file):
        os.system('sudo chown tiger {}'.format(_record_file))
        file_reported = set(load_lines(_record_file))
    # 获取需要报出的数据
    data = []
    rst_vv = []
    for f, t in fet:
        if f not in file_reported and now_time - t > 30 * 60:
            rst_vv.append(['pic_index', f])
            file_reported.add(f)
            data.extend(load_csv(f, to_list=True))
    # 更新record_file
    dump_lines(list(file_reported), _record_file)
    # 获取需要报出的vids
    rst = set()
    for n, lb, scr in data:
        vid = n.split('/')[-2]
        rst.add((vid, lb, scr))
    rst = list(rst)
    rst_vv.append(['vid', 'label', 'score', 'vv', 'VideoStatus', 'CreateTime', 'CreateTime', 'uid', 'StickerIDs', 'DedupPairItemID'])
    for vid, lb, scr in tqdm(rst, 'get_vv'):
        try:
            vinfo = vid2video_info(vid)
            rst_vv.append([
                '{}'.format(vid),
                '{}'.format(lb),
                '{}'.format(scr),
                '{}'.format(vinfo.PlayVVCount),
                '{}'.format(vinfo.VideoStatus),
                '{}'.format(vinfo.CreateTime),
                '{}'.format(format_time('{}'.format(vinfo.CreateTime))),
                '{}'.format(vinfo.AuthorID),
                '{}'.format(vinfo.StickerIDs),
                '{}'.format(vinfo.DedupPairItemID),
            ])
        except Exception as e:
            s = traceback.format_exc()
            print(s)
            print(e)
            get_log('reporter').error('{}'.format(s))
            get_log('reporter').error('{}'.format(e))
    # 如果需要报出的vids大于0就输出
    # 获取group_id：https://open.feishu.cn/tool/token
    if len(rst) > 0:
        send_feishu_sheet(
            rst_vv,
            result_title='porn_vid_{}_{}_'.format(_current_date, len(rst)),
            lark_group_id='7277501750155198467',
            limit=10000,
            page_limit=10000,
            auto_cut=False,
        )


def show_info(q_vids, q_pics, q_porn, show, output_file):
    try:
        info_str = 'TASK: q_vids {} q_pics {} q_porn {}'.format(q_vids.qsize(), q_pics.qsize(), q_porn.qsize()),
        print(info_str)
        logging.info(info_str)
        # q_porn里有N个数据就输出
        if q_porn.qsize() >= 3:
            new_porn_pics = []
            while not q_porn.empty():
                p_info = q_porn.get()
                new_porn_pics.append([p_info[0], p_info[1], p_info[2]])
            all_rst = []
            if is_file_exist(output_file):
                os.system('sudo chown tiger {}'.format(output_file))
                all_rst = load_csv(output_file, to_list=True)
            all_rst.extend(new_porn_pics)
            dump_csv(all_rst, output_file, index=False)
            print('DUMP: {} porn to {}'.format(len(all_rst), output_file))
            logging.info('DUMP: {} {}'.format(output_file, len(all_rst)))
    except Exception as e:
        if show:
            s = traceback.format_exc()
            print(s)
            print(e)
            get_log('show_info').error('{}'.format(s))
            get_log('show_info').error('{}'.format(e))


def infer(
        vid_file_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_vids',      # 每行一个vid
        record_file_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_rcd',    # 记录
        pic_dir_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_pics',
        output_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_rst',
        task_size_vid=1600,
        worker_vid2pic=16,
        worker_pic2porn=16,
        show=False,
        model_checkpoint="/mnt/bn/mlxlabzw/xiangyuejia/porn/vit-large-patch16-224-finetuned-eurosat-1218-3-epoch8",
):
    try:
        from transformers import pipeline
    except ModuleNotFoundError as e:
        pip_install('transformers')
        from transformers import pipeline

    make_dir(record_file_path)
    make_dir(pic_dir_path)
    make_dir(output_path)
    check_requirements()
    q_vids = Queue()
    q_pics = Queue()
    q_porn = Queue()
    for i in range(worker_vid2pic):
        t = Thread(target=query_vid2pic, args=(q_vids, q_pics, i, show))
        t.start()
    for i in range(worker_pic2porn):
        t = Thread(target=query_pic2porn, args=(q_pics, q_porn, i, show, model_checkpoint))
        t.start()
    old_currentdate = ''
    while True:
        # 下载sql结果文件到本地
        _t = time.localtime(time.time())
        currentdate='{}{}{}{}'.format(_t.tm_year, _t.tm_mon, _t.tm_mday, _t.tm_hour)
        if currentdate != old_currentdate:
            if show:
                print('new current date {}'.format(currentdate))
                get_log('main').info('new current date {}'.format(currentdate))
            while not q_vids.empty():
                q_vids.get()
            while not q_pics.empty():
                q_pics.get()
            reporter(
                output_path,
                '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/alart_record.txt',
                currentdate
            )
            old_currentdate = currentdate
        vid_file = os.path.join(vid_file_path, currentdate+'.txt')
        if not is_file_exist(vid_file):
            os.system('hdfs dfs -ls hdfs://haruna/home/byte_faceu_qa/data/yuejiaxiang/| sort -rk6,7 | awk \'{print $NF}\' | head -n 1 | xargs -I {} hdfs dfs -ls {} | grep part | awk \'{print $NF}\' | xargs -I {} hdfs dfs -copyToLocal {} '+vid_file)
        if not is_file_exist(vid_file):
            print('MAIN: get new vid_file failed {}'.format(vid_file))
            get_log('main').info('MAIN: get new vid_file failed {}'.format(vid_file))
            sleep(10+randint(1, 10))
        else:
            # 如果队列里数量过多，则等待一段时间后重试
            size_q_vids = q_vids.qsize()
            if size_q_vids > task_size_vid * 3:
                print('size_q_vids too large {}'.format(size_q_vids))
                get_log('main').info('size_q_vids too large {}'.format(size_q_vids))
                sleep(30)
                continue
            # 建立sql进度文件，输出路径
            new_vid_file = vid_file
            record_file = os.path.join(record_file_path, split_path(new_vid_file)[2]+'.rcd')
            pic_dir = os.path.join(pic_dir_path, split_path(new_vid_file)[2]+'/')
            make_dir(pic_dir)
            output_file = os.path.join(output_path, split_path(new_vid_file)[2]+'.csv')

            t = Thread(target=show_info, args=(q_vids, q_pics, q_porn, show, output_file))
            t.start()

            print(currentdate)
            print(new_vid_file)
            print(record_file)
            print(pic_dir)
            print(output_file)
            get_log('main').info(currentdate)
            get_log('main').info(new_vid_file)
            get_log('main').info(record_file)
            get_log('main').info(pic_dir)
            get_log('main').info(output_file)

            head_line = 0
            if is_file_exist(record_file):
                os.system('sudo chown tiger {}'.format(record_file))
                head_line = int(load_lines(record_file)[0])
                dump_lines([head_line + task_size_vid], record_file)
            else:
                dump_lines([head_line + task_size_vid], record_file)
            print('load vids', new_vid_file, head_line, task_size_vid)
            get_log('main').info('load vids {} {} {}'.format(new_vid_file, head_line, task_size_vid))
            all_vids = load_lines(new_vid_file, separator=',')
            bag_vids = []
            for line in all_vids[head_line: head_line+task_size_vid]:
                nums = line[0]
                try:
                    nums = nums.strip().strip('"')
                    int(nums)
                except:
                    continue
                item_id = str(nums)
                bag_vids.append(item_id)
            if len(bag_vids) == 0:
                # 说明已经没有待处理的vid，等几秒后看看是否有新vid文件
                sleep(20+randint(1, 10))
                continue

            for vid in bag_vids:
                q_vids.put((vid, pic_dir))

            _tb = time.time()
            while True:
                # 执行一定时间后看看是否有新vid文件要处理
                if time.time() - _tb > 200+randint(1, 100):
                    break
                # 待处理图片较少后拉新的一批vid
                if q_vids.qsize() < 1000:
                    break
                sleep(1)


if __name__ == '__main__':
    infer(show=True)
