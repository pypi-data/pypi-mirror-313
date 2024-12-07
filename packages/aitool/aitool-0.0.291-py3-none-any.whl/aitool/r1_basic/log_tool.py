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
日志工具
"""
import os
import logging
from typing import Tuple, List, Any
from time import sleep, time, gmtime, strftime
from aitool import get_current_path, singleton, timestamp, dump_lines


@singleton
class LogSet:
    def __init__(self):
        """
        用于存储logger及其名称
        """
        self.name2log = {}

    def get_log(self, name, file=None, fmt=None, level=logging.DEBUG) -> logging.Logger:
        """
        通过名称获取logger

        :param name: logger的名称
        :param file: logger的存储文件
        :param fmt: logger的格式
        :param level: logger的通知消息等级
        :return:
        """
        if name in self.name2log:
            return self.name2log[name]
        else:
            if file is None:
                log_dir = get_current_path()
                file = os.path.join(log_dir, name + '.log')
                print('log name: {} path: {}'.format(name, file))
            if fmt is None:
                fmt = '[%(asctime)s - %(name)s - %(levelname)s] : %(message)s'
            logger = logging.getLogger(name)
            formatter = logging.Formatter(fmt)
            file_handler = logging.FileHandler(file, mode='a')
            file_handler.setFormatter(formatter)
            logger.setLevel(level)
            logger.addHandler(file_handler)
            self.name2log[name] = logger
            return logger


def get_log(*args, **kwargs) -> logging.Logger:
    """
    获取一个指向特定文件的log, 参考LogSet.get_log

    >>> get_log('log_1').error('error_1')  # doctest: +ELLIPSIS
    log name: log_1 path: ...log_1.log
    >>> get_log('log_2').error('error_2')  # doctest: +ELLIPSIS
    log name: log_2 path: ...log_2.log
    >>> get_log('log_1').info('info_3')
    >>> get_log('log_2').info('info_4')
    >>> from aitool import load_lines
    >>> load_lines('./log_1.log')  # doctest: +ELLIPSIS
    ['...ERROR...error_1', '...INFO...info_3']
    >>> load_lines('./log_2.log')  # doctest: +ELLIPSIS
    ['...ERROR...error_2', '...INFO...info_4']

    """
    log_set = LogSet()
    return log_set.get_log(*args, **kwargs)



class Record:
    def __init__(self, interval: float = 10, show: bool = True, name: str = ''):
        self.name = name
        self.record_file = './record/record_{}_{}.txt'.format(self.name, timestamp(style='sec'))
        self.record_info = []
        self.time_init = time()
        self.show = show
        self.time_last_display = 0
        self.interval = interval    # 距离上次输出的间隔时间

    def note(self, data: Tuple[str, Any], finish: bool = False, max_line: int = 1000):
        """列表类型的数据只输出前20列"""
        self.record_info.append([data, time()-self.time_init])
        if self.show:
            print('{:.1f}s'.format(time()-self.time_init), data)

        if time() - self.time_last_display >= self.interval or finish:
            self.time_last_display = time()
            record_output = []
            for line, timer in self.record_info:
                content = line[1]
                if isinstance(line[1], List):
                    content = '\n'.join(['{}'.format(_) for _ in line[1][:max_line]])
                record_output.append('【{} :: {}】'.format(line[0], strftime("%H:%M:%S", gmtime(timer))))
                record_output.append('{}\n\n'.format(content))

            dump_lines(record_output, self.record_file)

    def finish(self):
        """进行一次输出"""
        self.note(('finish', ''), finish=True)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
