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
# See the License for the specific language governing permissiozns and
# limitations under the License.
"""

"""
from typing import Dict, Union, List, Any, NoReturn, Tuple
import sys
import os
from aitool import load_byte, pip_install


def get_client(name=None, storage=None, key=None, endpoint='tos-cn-north.byted.org', timeout=60, connect_timeout=60):
    try:
        import bytedtos
    except ModuleNotFoundError:
        pip_install('bytedtos --index-url=https://bytedpypi.byted.org/simple/')
        if sys.platform == 'darwin':
            # mac电脑上需要重新编译bytedlogger
            os.system('pip uninstall bytedlogger -y')
            os.system('ARCHFLAGS="-arch arm64" pip install bytedlogger --compile --no-cache-dir --index-url=https://bytedpypi.byted.org/simple/')
        import bytedtos
    if name == 'model':
        storage = 'pypi-model-storage'
        key = 'YOLZ0N0N9LBU6JVKCB9X'
    if name == 'dorado':
        storage = 'dorado-output-file'
        key = 'DQM6AD4TPB0QP0LEFEC6'
    if name == 'porn':
        storage = 'ies-turing-pornmarketing'
        key = 'VSHS8IU4P9O1Q45F056W'
    return bytedtos.Client(storage, key, endpoint=endpoint, timeout=timeout, connect_timeout=connect_timeout)


def send_text2tos(file_name, text: str, **kwargs):
    tos_client = get_client(**kwargs)
    resp = tos_client.put_object(file_name, text)
    # 请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
    from bytedtos.consts import ReqIdHeader
    print(resp.headers.get(ReqIdHeader))
    # HTTP响应头部。
    print(resp.headers)


def send_file2tos(obj_key, file_path, **kwargs):
    try:
        import bytedtos
    except ModuleNotFoundError:
        pip_install('bytedtos --index-url=https://bytedpypi.byted.org/simple/')
        if sys.platform == 'darwin':
            # mac电脑上需要重新编译bytedlogger
            os.system('pip uninstall bytedlogger -y')
            os.system('ARCHFLAGS="-arch arm64" pip install bytedlogger --compile --no-cache-dir --index-url=https://bytedpypi.byted.org/simple/')
        import bytedtos
    total_size = os.path.getsize(file_path)
    part_size = 10 * 1024 * 1024
    try:
        client = get_client(**kwargs)
        upload_id = client.init_upload(obj_key).upload_id
        parts_list = []
        with open(file_path, 'rb') as f:
            part_number = 1
            offset = 0
            while offset < total_size:
                print(offset/total_size)
                if total_size - offset < 2 * part_size:
                    num_to_upload = total_size - offset
                else:
                    num_to_upload = min(part_size, total_size - offset)
                f.seek(offset, os.SEEK_SET)
                cur_data = f.read(num_to_upload)
                upload_part_resp = client.upload_part(obj_key, upload_id, part_number, cur_data)
                parts_list.append(upload_part_resp.part_number)
                offset += num_to_upload
                part_number += 1
        comp_resp = client.complete_upload(obj_key, upload_id, parts_list)
        print("action suc")
        download_url = 'http://tosv.byted.org/obj/' + '{}/'.format(client.bucket) + obj_key
        return download_url
    except bytedtos.TosException as e:
        print("action failed. code: {}, request_id: {}, message: {}".format(e.code, e.request_id, e.msg))


if __name__ == "__main__":
    # 此方法仅支持字符串，且小于100M
    # print(send_text2tos('test', 'hello world', name='porn'))

    # 此方法支持大文件
    # print(send_file2tos('查询结果.csv.zip', '/Users/bytedance/Downloads/查询结果.csv.zip', name='dorado'))

    # 此方法支持大文件
    print(send_file2tos('wenboyan资料.z04', '/Users/bytedance/Downloads/Desktop/wenboyan资料.z01', name='dorado'))
