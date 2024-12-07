# -*- coding: UTF-8 -*-
# Copyright©2020 xiangyuejia@qq.com All Rights Reserved
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
下载数据
"""
from typing import Any, NoReturn, Callable, Optional
import hashlib
import sys
from urllib import request, error
import os
import math
import tarfile
import zipfile
import gzip
from enum import Enum
import requests
from tqdm import tqdm
from aitool import WEB_PATH, DATA_PATH, make_dir, is_file_exist, is_writable, unzip, timestamp, split_path


def get_download_dir():
    """
    获取存储数据的文件夹路径
    Return the directory to which packages will be downloaded by default.

    >>> get_download_dir()  # doctest: +SKIP
    '/.../aitool_data'
    """
    # common path
    paths = []
    if sys.platform.startswith("win"):
        paths += [
            os.path.join(sys.prefix, "aitool_data"),
            os.path.join(sys.prefix, "share", "aitool_data"),
            os.path.join(sys.prefix, "lib", "aitool_data"),
            os.path.join(os.environ.get("APPDATA", "C:\\"), "aitool_data"),
            r"C:\aitool_data",
            r"D:\aitool_data",
            r"E:\aitool_data",
        ]
    else:
        paths += [
            os.path.join(sys.prefix, "aitool_data"),
            os.path.join(sys.prefix, "share", "aitool_data"),
            os.path.join(sys.prefix, "lib", "aitool_data"),
            "/usr/share/aitool_data",
            "/usr/local/share/aitool_data",
            "/usr/lib/aitool_data",
            "/usr/local/lib/aitool_data",
        ]
    for path in paths:
        if is_file_exist(path) and is_writable(path):
            return path

    # On Windows, use %APPDATA%
    if sys.platform == "win32" and "APPDATA" in os.environ:
        homedir = os.environ["APPDATA"]

    # Otherwise, install in the user's home directory.
    else:
        homedir = os.path.expanduser("~/")
        if homedir == "~/":
            raise ValueError("Could not find a default download directory")

    return os.path.join(homedir, "aitool_data")


class DownloadMethod(Enum):
    """ download_file函数的下载方法 """
    urlretrieve = 1
    get = 2


class ProcessMethod:
    """ download_file函数的进度条样式 """
    @classmethod
    def report_process(cls, block_num, block_size, total_size):
        sys.stdout.write('\r>> Downloading %.1f%%' % (float(block_num * block_size) / float(total_size) * 100.0))
        sys.stdout.flush()

    @classmethod
    def bar_process(cls) -> Callable[[int, int, int], None]:
        pbar = tqdm(total=None)

        def bar_update(count, block_size, total_size):
            if pbar.total is None and total_size:
                pbar.total = total_size
            progress_bytes = count * block_size
            pbar.update(progress_bytes - pbar.n)

        return bar_update


def download_file(
        url: str,
        filename: str,
        method: DownloadMethod = DownloadMethod.urlretrieve,
        reporthook: Callable = ProcessMethod.report_process,
        data: Any = None,
        show: bool = True,
) -> str:
    """
    下载url的数据

    :param url: 数据链接
    :param filename: 存储到本地的文件名
    :param method: 下载方法，默认是DownloadMethod.get，也可选DownloadMethod.urlretrieve
    :param reporthook: 透传给request.urlretrieve，默认是ProcessMethod.report_process，也可选ProcessMethod.bar_process
    :param data: 透传给request.urlretrieve
    :param show: 打印细节
    :return:

    >>> link = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
    >>> download_file(link, './x.jpg', method=DownloadMethod.get, show=False)
    './x.jpg'
    """
    try:
        if show:
            print("Start downloading {} to {}... {}".format(url, filename, timestamp()))
        if method == DownloadMethod.urlretrieve:
            request.urlretrieve(url, filename, reporthook, data)
        elif method == DownloadMethod.get:
            chunk_size = 1024
            make_dir(filename, file=True)
            resp = requests.get(url, stream=True)
            content_size = math.ceil(int(resp.headers['Content-Length']) / chunk_size)
            with open(filename, "wb") as file:
                for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=filename):
                    file.write(data)
        if show:
            print("Download {} successfully! {}".format(url, timestamp()))
    except (error.HTTPError, error.URLError) as e:
        print(e)
    return filename


def get_aitool_data(
        file_name,
        sub_path='',
        url_root=WEB_PATH,
        packed: bool = False,
        packed_name=None,
        pack_way=None,
):
    """
    通过文件名称获取数据的下载路径。
    - 本方法为cos源定制。
    - TODO 未来将和 prepare_data 方法合并

    :param file_name: 文件名称
    :param sub_path: 子路径
    :param url_root: 远端根路径
    :param packed: 是否被压缩
    :param packed_name: 压缩后的文件名
    :param pack_way: 压缩方式
    :return: 文件下载到本地后的路径

    >>> get_aitool_data('keyword.pkl')  # doctest: +SKIP
    '/.../keyword.pkl'
    """
    if not url_root:
        raise ValueError("invalid url_root")

    file_dir = get_download_dir()
    file_path = os.path.join(file_dir, sub_path, file_name)
    if is_file_exist(file_path):
        return file_path

    if not packed:
        # 不是压缩包
        url = os.path.join(url_root, file_name)
        download_file(url, file_path, method=DownloadMethod.get, show=True)
    else:
        # 是压缩包 (文件名不同，可能有多级路径)
        url = os.path.join(url_root, packed_name)
        pack_path = os.path.join(file_dir, packed_name)
        download_file(url, pack_path, method=DownloadMethod.get, show=True)
        # TODO 默认用zip解压，未考虑其他压缩格式
        if pack_way == 'zip':
            print('unzip', pack_path)
            unzip(pack_path, os.path.join(file_dir, sub_path))
        else:
            unzip(pack_path, os.path.join(file_dir, sub_path))
    if is_file_exist(file_path):
        return file_path
    else:
        raise ValueError("not find: {}".format(file_path))


def prepare_data(url: str, directory: str = None, packed: bool = False, tmp_dir: str = '') -> NoReturn:
    """
    直接从url下载文件到directory。如果packed=True则用unzip解压

    :param url: 下载文件的链接
    :param directory: 文件存储路径，如果没有指定则默认存储到包路径下
    :param packed: 是否被zip压缩
    :param tmp_dir: 如果被压缩过，将在临时路径下暂存压缩文件
    :return: 文件下载好的路径

    >>> link = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
    >>> prepare_data(link)  # doctest: +SKIP
    '/.../PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
    """
    if directory is None:
        _, file_name, _, _ = split_path(url)
        directory = os.path.join(DATA_PATH, file_name)
    if not packed:
        download_file(url, directory)
        return directory
    else:
        if not tmp_dir:
            tmp_dir = os.path.join(DATA_PATH, 'tmp')
        packed_file = download_file(url, tmp_dir)
        unzip(packed_file, directory)
        return directory


def calculate_md5(fpath: str, chunk_size: int = 1024 * 1024) -> str:
    """
    计算文件的md5

    :param fpath: 文件路径
    :param chunk_size: 计算尺寸
    :return: md5

    >>> calculate_md5('./data.pkl')  # doctest: +SKIP
    '8bb3a57bf3c044c5462e69e8fc67c1fb'
    """
    md5 = hashlib.md5()
    with open(fpath, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def check_md5(fpath: str, md5: str, **kwargs: Any) -> bool:
    """
    验证文件的md5是否一致

    :param fpath: 文件路径
    :param md5: 预期的md5
    :param kwargs: 透传给calculate_md5
    :return: 是否一致

    >>> check_md5('./data.pkl', '8bb3a57bf3c044c5462e69e8fc67c1fb')  # doctest: +SKIP
    True
    """
    if not os.path.isfile(fpath):
        return False
    if md5 is None:
        return True
    return md5 == calculate_md5(fpath, **kwargs)


def extract_archive(from_path: str, to_path: Optional[str] = None, remove_finished: bool = False) -> str:
    """
    解压文件。支持格式.tar.xz，.tar，.tar.gz，.tgz，.gz，.zip

    :param from_path: 压缩文件的路径
    :param to_path: 解压路径
    :param remove_finished: 解压后删除原始数据
    :return: 解压后的文件路径或文件夹路径

    >>> extract_archive('./x.jpg.zip', './demo/')  # doctest: +SKIP
    './demo/'
    """
    def _is_tarxz(filename: str) -> bool:
        return filename.endswith(".tar.xz")

    def _is_tar(filename: str) -> bool:
        return filename.endswith(".tar")

    def _is_targz(filename: str) -> bool:
        return filename.endswith(".tar.gz")

    def _is_tgz(filename: str) -> bool:
        return filename.endswith(".tgz")

    def _is_gzip(filename: str) -> bool:
        return filename.endswith(".gz") and not filename.endswith(".tar.gz")

    def _is_zip(filename: str) -> bool:
        return filename.endswith(".zip")

    def _is_within_directory(directory, target):
        abs_directory = os.path.abspath(directory)
        abs_target = os.path.abspath(target)
        prefix = os.path.commonprefix([abs_directory, abs_target])
        return prefix == abs_directory

    def _safe_extract(_tar, path=".", members=None, *, numeric_owner=False):
        for member in _tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not _is_within_directory(path, member_path):
                raise Exception("Attempted Path Traversal in Tar File")
        _tar.extractall(path, members, numeric_owner=numeric_owner)

    if to_path is None:
        to_path = os.path.dirname(from_path)

    if _is_tar(from_path):
        with tarfile.open(from_path, 'r') as tar:
            _safe_extract(tar, path=to_path)
    elif _is_targz(from_path) or _is_tgz(from_path):
        with tarfile.open(from_path, 'r:gz') as tar:
            _safe_extract(tar, path=to_path)
    elif _is_tarxz(from_path):
        with tarfile.open(from_path, 'r:xz') as tar:
            _safe_extract(tar, path=to_path)
    elif _is_gzip(from_path):
        to_path = os.path.join(to_path, os.path.splitext(os.path.basename(from_path))[0])
        with open(to_path, "wb") as out_f, gzip.GzipFile(from_path) as zip_f:
            out_f.write(zip_f.read())
    elif _is_zip(from_path):
        with zipfile.ZipFile(from_path, 'r') as z:
            z.extractall(to_path)
    else:
        raise ValueError("Extraction of {} not supported".format(from_path))

    if remove_finished:
        os.remove(from_path)

    return to_path


if __name__ == '__main__':
    import doctest

    doctest.testmod()
