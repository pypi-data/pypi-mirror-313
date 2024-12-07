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
执行shell指令
"""
import subprocess
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import is_folder, is_file


def shell(
        cmd,
        b: bool = True,
        show: bool = False,
        quiet: bool = False,
) -> Any:
    """
    执行shell指令

    :param cmd: 指令
    :param b: True:bytes格式字符串， False:utf-8格式字符串
    :param show: 打印细节信息
    :param quiet: 返回值为None
    :return: 指令执行结果

    >>> shell('pwd')  # doctest: +ELLIPSIS
    b...

    >>> shell('pwd', show=True)  # doctest: +ELLIPSIS
    CMD pwd
    b...

    >>> shell('pwd',  quiet=True)  # 无返回

    >>> shell('kkk')
    Traceback (most recent call last):
        ...
    subprocess.CalledProcessError: Command 'kkk' returned non-zero exit status 127.
    """
    if show:
        print('CMD', cmd)
    try:
        out_bytes = subprocess.check_output('{}'.format(cmd), shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode, e.output)
        raise e
    if quiet:
        return None
    if b:
        return out_bytes
    else:
        return str(out_bytes, encoding="utf-8")


def mkdir(path, **kwargs):
    """
    新建一个目录，如果有多层会递归地新建。
    TODO 此方法路径名大小写不敏感。如果已有路径'./A',在执行mkdir('./a/b')后得到的是'./A/b'

    :param path: 目录
    :param kwargs: 透传给shell的参数
    :return: shell的返回值

    >>> mkdir('./demo/A/b')
    >>> is_folder('./demo/A/b')
    True
    """
    shell('mkdir -p "{}"'.format(path), **kwargs)


def shell_cp(source_path, target, **kwargs):
    """
    复制文件或文件夹

    :param source_path: 源文件或文件夹
    :param target: 复制后的文件或复制后的路径
    :param kwargs: 透传给shell的参数
    :return: shell的返回值

    >>> mkdir('./demo/A')
    >>> mkdir('./demo/B')
    >>> shell('touch ./demo/A/a.txt', quiet=True)
    >>> shell_cp('./demo/A/a.txt', './demo/B')

    >>> mkdir('./demo/A')
    >>> shell('touch ./demo/A/a.txt', quiet=True)
    >>> shell_cp('./demo/A', './demo/B')
    """
    if is_file(source_path):
        shell('cp "{}" "{}"'.format(source_path, target), **kwargs)
    elif is_folder(source_path):
        shell('cp -r "{}" "{}"'.format(source_path, target), **kwargs)
    else:
        raise ValueError('{}既不是文件也不是文件夹'.format(source_path))


def cp(**kwargs):
    """
    调用shell_cp
    """
    shell_cp(**kwargs)


def shell_mv(source_path, target, **kwargs):
    """
    移动文件或文件夹

    :param source_path: 源文件或文件夹
    :param target: 新位置
    :param kwargs: 透传给shell的参数
    :return: shell的返回值

    >>> mkdir('./demo/A')
    >>> shell('touch ./demo/A/a.txt', quiet=True)
    >>> shell_mv('./demo/A/a.txt', './demo/A/b.txt')

    >>> mkdir('./demo/A')
    >>> shell('touch ./demo/A/a.txt', quiet=True)
    >>> shell_mv('./demo/A', './demo/B')
    """
    shell('mv "{}" "{}"'.format(source_path, target), **kwargs)


def mv(**kwargs):
    """
    调用shell_mv
    """
    shell_mv(**kwargs)


def install_conda():
    """
    安装conda
    """
    shell('wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ./miniconda.sh')
    shell('bash ./miniconda.sh -b -p $HOME/miniconda')
    shell('export PATH="$HOME/miniconda/bin:$PATH"')


def activate_env(name):
    """
    激活env
    """
    shell('conda activate {}'.format(name))
    shell('source activate {}'.format(name))


def create_env(name, requirements: List[str]):
    """
    创建env
    """
    shell('export PATH="$HOME/miniconda/bin:$PATH"')
    shell('conda create -n {}'.format(name))
    for pkg in requirements:
        shell('pip install {}'.format(pkg))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
