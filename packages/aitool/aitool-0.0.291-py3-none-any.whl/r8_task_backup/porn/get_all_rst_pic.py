# -*- coding: UTF-8 -*-
# Copyright©2022 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

"""
from os import path
from tqdm import tqdm
from random import sample
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import get_file_etime, load_csv, make_dir, is_file_exist, shell_cp

rst_path = '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/t_rst'
out_path = '/mnt/bn/mlxlabzw/xiangyuejia/porn/hug/auto/check_1013'
pic_choose = 3000

make_dir(out_path)
pics = []
fet = get_file_etime(rst_path)
for f, t in fet:
    fp = [_[0] for _ in load_csv(f, to_list=True)]
    print(fp[:5])
    pics.extend(fp)
cnt = 0
pics = sample(pics, pic_choose)
for p in tqdm(pics):
    if not is_file_exist(p):
        continue
    shell_cp(p, path.join(out_path, '{}.jpg'.format(cnt)))
    cnt += 1
