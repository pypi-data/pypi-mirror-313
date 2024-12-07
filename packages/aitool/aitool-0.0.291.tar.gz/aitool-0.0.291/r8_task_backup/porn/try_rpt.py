# -*- coding: UTF-8 -*-
import time
from aitool import dump_lines, load_lines, get_file_etime, send_feishu_sheet, is_file_exist, load_csv
from tqdm import tqdm
from aitool.r8_task.porn.get_video_info import vid2video_info
import os

def reporter(_dir, _record_file, _current_date):
    # 现在的时间
    now_time = time.time()
    # 获取dir目录下所有文件的编辑时间
    print(_dir)
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
    for n, scr in data:
        vid = n.split('/')[-2]
        rst.add((vid, scr))
    rst = list(rst)
    rst_vv.append(['vid', 'score', 'vv', 'VideoStatus', 'CreateTime', 'uid', 'StickerIDs', 'DedupPairItemID'])
    for vid, scr in tqdm(rst, 'get_vv'):
        try:
            vinfo = vid2video_info(vid)
            rst_vv.append([
                '{}'.format(vid),
                '{}'.format(scr),
                '{}'.format(vinfo.PlayVVCount),
                '{}'.format(vinfo.VideoStatus),
                '{}'.format(vinfo.CreateTime),
                '{}'.format(vinfo.AuthorID),
                '{}'.format(vinfo.StickerIDs),
                '{}'.format(vinfo.DedupPairItemID),
            ])
        except Exception as e:
            print(e)
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


import time
_t = time.localtime(time.time())
currentdate='{}{}{}{}'.format(_t.tm_year, _t.tm_mon, _t.tm_mday, _t.tm_hour)
output_path='/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_rst'
reporter(
    output_path,
    '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/alart_record.txt',
    currentdate,
)


