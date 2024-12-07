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
安装pypi包。
- 此方法内不应调用aitool.shell方法，以避免循环引用
"""
from typing import NoReturn
import os
from aitool import print_green, is_contain


def pip_install_by_os(package_name: str) -> NoReturn:
    """
    通过os.system方法安装pypi包

    :param package_name: 包名
    :return: NoReturn
    """
    # 预防类似 && rm -rf * 的攻击
    if is_contain(package_name, ['-r', '&&', '|', '||', '*']):
        return
    try:
        os.system('pip3 install {}'.format(package_name))
    except ModuleNotFoundError:
        os.system('pip install {}'.format(package_name))


def pip_install_by_main(package_name: str) -> NoReturn:
    """
    通过pip.main方法安装pypi包

    :param package_name:
    :return: NoReturn
    """
    try:
        from pip import main
    except ImportError:
        pip_install_by_os('pip --upgrade')
        from pip import main
    x = main(['install', '{}'.format(package_name)])
    print(x)


def pip_install(package_name: str) -> NoReturn:
    """
    安装pip包。本方法会通过except Exception捕获所有报错，以保证即使安装失败也不中断程序。

    :param package_name: 包名
    :return: NoReturn

    >>> pip_install('jieba')  # doctest: +SKIP
    >>> pip_install('jieba==0.42.1')  # doctest: +SKIP
    >>> pip_install('jieba >= 0.42')  # doctest: +SKIP
    """
    print_green('lazy install package {}'.format(package_name))
    if '-' not in package_name:
        # 简单的直接用包名+版本号的格式
        try:
            pip_install_by_main(package_name)
        except Exception as e:
            print(e)
    try:
        # 复杂的格式
        pip_install_by_os(package_name)
    except Exception as e:
        print(e)


def pip_install_mac(package_name: str) -> NoReturn:
    """
    在mac m1电脑里有些包需要用arm64源码编译

    :param package_name: 包名
    :return: NoReturn
    """
    print('用于处理mac电脑报错 ImportError: mach-o file, but is an incompatible architecture (have arm64, need x86_64)')
    if '-r' in package_name or '&&' in package_name or '*' in package_name:
        raise ValueError('本方法仅支持简单的包名[版本限制]，不支持-r、&&、*')
    os.system('ARCHFLAGS="-arch arm64" pip install {} --compile --no-cache-dir'.format(package_name))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
