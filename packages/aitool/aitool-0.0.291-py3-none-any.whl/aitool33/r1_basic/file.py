# -*- coding: UTF-8 -*-
# @Time    : 2020/10/29
# @Author  : xiangyuejia@qq.com
"""
文件相关的操作
"""
import os
import sys
import json
import stat
import fileinput
import warnings
import pickle
from collections import defaultdict
import inspect
import functools
from typing import Any, List, Union, NoReturn, Dict, Iterator, Callable, Tuple
from numpy import ndarray
import numpy as np
import pandas as pd
from pandas import DataFrame
from aitool import split_dict, Deduplication, pip_install


def abspath(path: str) -> str:
    """
    输出绝对路径

    :param path: 路径
    :return: 绝对路径

    >>> abspath('./')  # doctest: +SKIP
    """
    return os.path.abspath(path)


def is_writable(path):
    """
    判定路径是否可写

    :param path: 路径
    :return: 是否可写

    >>> is_writable('./')  # doctest: +SKIP
    """
    if not os.path.exists(path):
        return False

    # If we're on a posix system, check its permissions.
    if hasattr(os, "getuid"):
        statdata = os.stat(path)
        perm = stat.S_IMODE(statdata.st_mode)
        # is it world-writable?
        if perm & 0o002:
            return True
        # do we own it?
        elif statdata.st_uid == os.getuid() and (perm & 0o200):
            return True
        # are we in a group that can write to it?
        elif (statdata.st_gid in [os.getgid()] + os.getgroups()) and (perm & 0o020):
            return True
        # otherwise, we can't write to it.
        else:
            return False
    return True


def is_file(path: str) -> bool:
    """
    判断是否是个文件，如果是文件夹或不存在则返回False

    :param path: 文件路径
    :return: 该文件是否存在
    """
    if os.path.isfile(path):
        return True
    return False


def is_folder(path: str) -> bool:
    """
    判断是否是个文件夹，如果是文件或不存在则返回False
    TODO 此方法路径名大小写不敏感。如果已有路径'./A/b',is_folder('./a/b')得到True

    :param path: 路径
    :return: 该路径是否是个文件夹
    """
    if os.path.isdir(path):
        return True
    return False


def is_file_exist(file: str) -> bool:
    """
    判断文件是否存在

    :param file: 文件名
    :return: 文件是否存在
    """
    return os.path.exists(file)


def is_file_hidden(file: str) -> bool:
    """
    目前仅能识别以.开始的隐藏文件 TODO 用文件名来判断会有遗漏

    :param file: 文件名
    :return: 文件是否是隐藏文件
    """
    path, filename = os.path.split(file)
    if filename[0] == '.':
        return True
    return False


def get_file(
        path: str,
        skip_hidden: bool = True,
        skip_folder: bool = False,
        show_folder: bool = False,
        absolute: bool = False,
) -> Iterator[str]:
    """
    遍历path下的所有文件（不包括文件夹）, 此方法读大文件很慢
    如果path不是文件夹，则直接返回。

    :param path: 待遍历的路径
    :param skip_hidden: 是否忽略隐藏文件，True表示忽略隐藏文件
    :param skip_folder: 是否遍历子文件夹，True表示不遍历字文件夹
    :param show_folder: 是否显示文件夹，False表示不显示
    :param absolute: 是否使用绝对路径，False表示不使用绝对路径
    :return: 一个返回文件名的迭代器

    >>> from aitool import dump_lines
    >>> dump_lines([], './demo/A/2.txt')
    './demo/A/2.txt'
    >>> dump_lines([], './demo/1.txt')
    './demo/1.txt'
    >>> sorted(list(get_file('./demo')))
    ['./demo/1.txt', './demo/A/2.txt']
    >>> sorted(list(get_file('./demo', skip_folder=True)))
    ['./demo/1.txt']
    >>> sorted(list(get_file('./demo', show_folder=True)))
    ['./demo/1.txt', './demo/A', './demo/A/2.txt']
    """
    # for root, ds, fs in iter_tool:
    if is_folder(path):
        for obj in os.scandir(path):
            file_path = obj.path
            if skip_hidden and is_file_hidden(file_path):
                continue
            if is_folder(file_path):
                if skip_folder:
                    continue
                yield from get_file(path=file_path, skip_hidden=skip_hidden, skip_folder=skip_folder, absolute=absolute)
            if absolute:
                yield os.path.abspath(file_path)
            else:
                if is_folder(file_path) and not show_folder:
                    continue
                yield file_path
    else:
        if absolute:
            yield os.path.abspath(path)
        else:
            yield path


def add_python_path(
        root_path: str,
        recursive: bool = True,
        show: bool = False,
) -> List[str]:
    """
    将某路径下的所有python文件的绝对路径加到系统变量python_path

    用于处理ModuleNotFoundError问题
    通常只需要在对应文件开头加上，然后直接应该需要的包，而无需在意其所在的文件路径
    （需要确保项目里没有同名的python文件）

    :param root_path: 根路径
    :param recursive: 是否递归添加所有子路径
    :param show: 输出提示信息
    :return: 已添加到系统变量python_path中的路径

    >>> add_python_path('./', recursive=False)  # doctest: +ELLIPSIS
    [...]
    """
    python_path = set()
    if show:
        print('DEAL PATH: ', os.path.abspath(root_path))

    if recursive:
        name_single = defaultdict(list)
        for abs_path in get_file(root_path, absolute=True):
            if abs_path[-3:] == '.py':
                basename = os.path.basename(abs_path)
                name_single[basename].append(abs_path)
                python_path.add(os.path.dirname(abs_path))
        for k in name_single.keys():
            if len(name_single[k]) > 1:
                print('WARNING: name {} presents multiple times {}'.format(k, name_single[k]))
    else:
        python_path.add(os.path.abspath(root_path))

    for pth in python_path:
        sys.path.append(pth)
        if show:
            print('ADD PYTHON PATH: ', pth)

    return list(python_path)


def make_dir(dir_path: str, file=False) -> str:
    """
    创建文件夹。如果文件夹已存在则略过。

    :param dir_path: 路径
    :param file: 是否为文件，如果是文件将抽取其文件夹路径
    :return: 文件夹路径

    >>> make_dir('./demo_1')
    './demo_1'
    >>> make_dir('./demo_2/demo_3/demo.txt', file=True)
    './demo_2/demo_3'
    """
    if file:
        path, _ = os.path.split(dir_path)
    else:
        path = dir_path
    if path and not os.path.exists(path):
        os.makedirs(path)
    return path


def dump_json(
        obj: Any,
        file: str,
        formatting: bool = False,
        ensure_ascii: bool = False,
        format_postfix: bool = True,
        **kwargs,
) -> str:
    """
    写入json文件

    :param obj: 任意对象
    :param file: 存入文件
    :param formatting: dump with data-interchange format
    :param ensure_ascii: ensure ascii or not
    :param format_postfix: rename file name with tail .json
    :param kwargs: dict-formatted parameters
    :return: NoReturn

    >>> dump_json(['demo',1], './demo.json')
    './demo.json'
    """
    if format_postfix:
        if file[-5:] != '.json':
            print('rename file name with tail .json')
            file = file + '.json'
    make_dir(file, file=True)
    kwargs['ensure_ascii'] = ensure_ascii
    if formatting:
        kwargs['sort_keys'] = True
        kwargs['indent'] = 4
        kwargs['separators'] = (',', ':')
    with open(file, 'w', encoding='utf-8') as fw:
        json.dump(obj, fw, **kwargs)
    return file


def load_json(file: str, **kwargs,) -> Any:
    """
    加载json文件

    :param file: 文件路径
    :param kwargs: json.load的参数
    :return: 文件内容

    >>> dump_json(['demo',1], './demo.json')
    './demo.json'
    >>> print(load_json('./demo.json'))
    ['demo', 1]
    """
    if not os.path.isfile(file):
        print('incorrect file path')
        raise FileExistsError
    with open(file, 'r', encoding='utf-8') as fr:
        return json.load(fr, **kwargs,)


def dump_pickle(
        obj: Any,
        file: str,
        format_postfix: bool = True,
        **kwargs,
) -> str:
    """
    写入pickle文件

    :param obj: 任意对象
    :param file: 文件路径
    :param format_postfix: 修正文件路径的后缀名
    :param kwargs: pickle.dump的参数
    :return: 文件路径

    >>> dump_pickle(['demo',1, {'A': (2,3)}], './demo.pkl')
    './demo.pkl'
    """
    if format_postfix:
        if file[-4:] != '.pkl':
            print('rename file name with tail .pkl')
            file = file + '.pkl'
    make_dir(file, file=True)
    with open(file, 'wb') as fw:
        pickle.dump(obj, fw, **kwargs)
    return file


def load_pickle(file: str, **kwargs) -> Any:
    """
    加载pickle文件

    :param file: 文件路径
    :param kwargs: pickle.load的参数
    :return: 文件内容

    >>> dump_pickle(['demo',1, {'A': (2,3)}], './demo.pkl')
    './demo.pkl'
    >>> print(load_pickle('./demo.pkl'))
    ['demo', 1, {'A': (2, 3)}]
    """
    if not os.path.isfile(file):
        print('incorrect file path')
        raise Exception
    with open(file, 'rb') as fr:
        return pickle.load(fr, **kwargs)


def dump_lines(
        data: List[Any],
        file: str,
) -> str:
    """
    按行写入文本文件

    :param data: 数据
    :param file: 文件路径
    :return: 文件路径

    >>> dump_lines(['A', 2, 'B'], './demo.txt')
    './demo.txt'
    """
    make_dir(file, file=True)
    with open(file, 'w', encoding='utf8') as fout:
        for d in data:
            print(d, file=fout)
    return file


class Accessor:
    """
    用于打开文件
    """
    def __init__(self, file: str, open_method: str = 'fileinput') -> NoReturn:
        self.file = file
        self.iterator = None
        if open_method == 'open':
            self.iterator = open(self.file, 'r', encoding='utf8')
        if open_method == 'fileinput':
            self.iterator = fileinput.input([self.file])

    def __enter__(self) -> Iterator:
        return self.iterator

    def get_iterator(self) -> Iterator:
        return self.iterator

    def close(self) -> NoReturn:
        if self.iterator:
            self.iterator.close()

    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        self.close()


def repeat(item: Any) -> Any:
    """
    原样返回输入，用于作为Callable参数的默认值
    """
    return item


def load_line(
        file: str,
        separator: Union[None, str] = None,
        max_split: int = -1,
        deduplication: bool = False,
        line_processor: Callable = repeat,
        open_method: str = 'open',
        limit: int = -1,
) -> Iterator:
    """
    按行读入文件，会去掉每行末尾的换行符。返回一个迭代器。

    :param file: 文件路径
    :param separator: 用separator切分每行内容，None表示不做切分
    :param max_split: 控制separator的切分次数，-1表示不限制次数
    :param line_processor: 一个函数，对separator的结果做处理
    :param deduplication: 若为True，将不输出重复的行
    :param open_method: 指定打开文件的方法, 默认'open'，可指定为'fileinput'
    :param limit: 仅读前limit行
    :return: 文件每行的内容

    >>> dump_lines(['A', 2, 'B'], 'demo.txt')
    'demo.txt'
    >>> for line in load_line('demo.txt'):
    ...     print(line)
    A
    2
    B
    """
    cache = Deduplication()

    def inner_line_process(_file_iterator):
        count = 0
        for line in _file_iterator:
            if deduplication and cache.is_duplication(line):
                continue
            item = line.rstrip('\n\r')
            if separator:
                item = item.split(separator, max_split)
            count += 1
            if limit != -1 and count > limit:
                break
            yield line_processor(item)

    with Accessor(file, open_method=open_method) as file_iterator:
        yield from inner_line_process(file_iterator)


def load_byte(
        file: str,
        size: int = 10,
) -> bytes:
    """
    按字节读文件

    :param file: 文件路径
    :param size: 每次读的字节数，用于读大文件
    :return: 读到的字节
    """
    with open(file, 'rb') as file:
        for chunk in iter(lambda: file.read(size), b''):
            yield chunk


def load_lines(
        file: str,
        separator: Union[None, str] = None,
        separator_time: int = -1,
        form: str = None,
        deduplication: bool = False,
) -> Union[list, dict, set]:
    """
    读入文本文件。

    :param file: 文件路径
    :param separator: 对每行文本按分隔符进行切分
    :param separator_time: 每行切分的次数上限
    :param form: 输出的格式
    :param deduplication: 去重
    :return: 文件内容

    >>> dump_lines(['A 1', 'B 2 3'], './demo.txt')
    './demo.txt'
    >>> print(load_lines('./demo.txt'))
    ['A 1', 'B 2 3']
    >>> print(load_lines('./demo.txt', separator=' '))
    [['A', '1'], ['B', '2', '3']]
    >>> print(load_lines('./demo.txt', separator=' ', form='dict'))
    dict格式用每行的第一个元素作为key, 其后的元素的列表作为value。如果一行中不包含多个元素会报错。如果有相同的第一个元素会发生覆盖。
    {'A': '1', 'B': ['2', '3']}
    """
    data = []
    cache = Deduplication()
    with open(file, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            if deduplication and cache.is_duplication(line):
                continue
            item = line.rstrip('\n\r')
            if separator:
                if separator_time == -1:
                    item = item.split(separator)
                else:
                    item = item.split(separator, separator_time)
            data.append(item)
    if form == 'set':
        data = set(data)
    if form == 'dict':
        print('dict格式用每行的第一个元素作为key, 其后的元素的列表作为value。'
              '如果一行中不包含多个元素会报错。'
              '如果有相同的第一个元素会发生覆盖。')
        data = {item[0]: item[1:] if len(item) > 2 else item[1] for item in data}
    return data


MAX_LENGTH_XLSX = 1048576


def dump_panda(
        data: Union[List[Any], pd.DataFrame, Dict],
        file: str,
        file_format: str,
        format_postfix: bool = True,
        **kwargs,
) -> str:
    """
    用pandas.to_excel或pandas.to_csv将数据写入到文件中。

    :param data: 数据
    :param file: 文件路径
    :param file_format: 文件的类型
    :param format_postfix:
    :param kwargs:
    :return: 文件路径

    >>> dump_panda([1,2,3], './demo_dump_panda_1.xlsx', 'excel')
    WARNING: default set header=False
    './demo_dump_panda_1.xlsx'

    >>> dump_panda([1,2,3], './demo_dump_panda_2.csv', 'csv')
    WARNING: default set header=False
    './demo_dump_panda_2.csv'

    >>> dump_excel({'A':[[1,2,3]], 'B':[1,2,3]}, 'tmp_4.xlsx')  # 多sheet
    WARNING: default set header=False
    'tmp_4.xlsx'

    >>> demo_data = pd.DataFrame(data=['Apple','Banana'], columns=['Fruits'])
    >>> dump_panda(demo_data, './demo_dump_panda_3.xlsx', 'excel')
    WARNING: default set header=False
    './demo_dump_panda_3.xlsx'
    >>> dump_panda(demo_data, './demo_dump_panda_4.csv', 'csv')
    WARNING: default set header=False
    './demo_dump_panda_4.csv'

    >>> t = pd.DataFrame(data=[['Apple', 5], ['Banana', 10]], columns=['Fruits', 'Quantity'], index=[1, 2])
    >>> t.values.tolist()  # DataFrame转list
    [['Apple', 5], ['Banana', 10]]
    >>> t.columns.values.tolist()  # 获取全部列名
    ['Fruits', 'Quantity']
    >>> t[['Fruits']].values.tolist()  # DataFrame选特定列名的数据
    [['Apple'], ['Banana']]
    >>> dump_excel(t, 'tmp_1.xlsx', index=True)
    WARNING: default set header=False
    'tmp_1.xlsx'
    >>> dump_excel(t, 'tmp_2.xlsx', header=True)
    'tmp_2.xlsx'
    >>> dump_excel(t, 'tmp_3.xlsx', header=['Foods', 'Value'])  # 修改表头
    'tmp_3.xlsx'
    """
    if format_postfix:
        if file_format == 'excel':
            if file[-5:] != '.xlsx':
                print('rename file name with tail .xlsx')
                file = file + '.xlsx'
        if file_format == 'csv':
            if file[-4:] != '.csv':
                print('rename file name with tail .csv')
                file = file + '.csv'
    make_dir(file, file=True)

    if 'header' not in kwargs:
        print('WARNING: default set header=False')
        kwargs['header'] = False
    if 'index' not in kwargs:
        kwargs['index'] = False

    if file_format == 'excel':
        if 'engine' not in kwargs:
            kwargs['engine'] = 'xlsxwriter'
        if isinstance(data, dict):
            # 处理多表 TODO 目前多表模式不支持超长自动分割
            writer = pd.ExcelWriter(file, engine=kwargs['engine'])
            for sheet_name, sheet_data in data.items():
                df = pd.DataFrame(sheet_data)
                df.to_excel(writer, sheet_name=sheet_name, **kwargs)
            writer.save()
        else:
            # 处理单表
            if len(data) < MAX_LENGTH_XLSX - 100:
                df = pd.DataFrame(data)
                df.to_excel(file, **kwargs)
            else:
                piece_num = 0
                while data:
                    piece_data = data[:MAX_LENGTH_XLSX - 100]
                    piece_file = file + '_piece_' + str(piece_num) + '.xlsx'
                    data = data[MAX_LENGTH_XLSX - 100:]
                    selected_kwargs, _ = split_dict(kwargs, inspect.getfullargspec(pd.DataFrame).args)
                    df = pd.DataFrame(piece_data)
                    df.to_excel(piece_file, **kwargs)
                    piece_num += 1
    if file_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(file, **kwargs)
    return file


dump_csv = functools.partial(dump_panda, file_format='csv')
dump_excel = functools.partial(dump_panda, file_format='excel')


def load_excel(*args, value=True, all_sheet=False, concat=False, to_list=False, **kwargs) \
        -> Union[DataFrame, ndarray, List, Dict]:
    """
    读excel文件

    :param args: 需要读取的文件
    :param value: 仅输出dataframe的value部分
    :param all_sheet: 是否取所有sheet里的数据，默认为否，只取第一个sheet
    :param concat: 是否将所有sheet连接在一起
    :param to_list: 将dataframe的value部分从np转为list
    :param kwargs: pd.read_excel的参数
    :return: 读取的数据

    >>> dump_excel([['name', 'score'], ['A', 1], ['B', 2]], './demo.xlsx')
    WARNING: default set header=False
    './demo.xlsx'
    >>> load_excel('./demo.xlsx')
    array([['A', 1],
           ['B', 2]], dtype=object)
    >>> load_excel('./demo.xlsx', value=False)
      name  score
    0    A      1
    1    B      2
    >>> load_excel('./demo.xlsx', to_list=True)
    [['A', 1], ['B', 2]]
    """
    if concat:
        to_list = True
    if to_list:
        value = True

    if args[0][-4:] == '.xls':
        kwargs['engine'] = 'xlrd' if 'engine' not in kwargs else kwargs['engine']
    else:
        kwargs['engine'] = 'openpyxl' if 'engine' not in kwargs else kwargs['engine']
    kwargs['keep_default_na'] = False if 'keep_default_na' not in kwargs else kwargs['keep_default_na']

    # 对多个sheet
    if all_sheet and 'sheet_name' not in kwargs:
        kwargs['sheet_name'] = None
    multi_sheet = False
    if 'sheet_name' in kwargs and (kwargs['sheet_name'] is None or type(kwargs['sheet_name']) in (list, set)):
        multi_sheet = True

    data = np.array([])
    try:
        df = pd.read_excel(*args, **kwargs)
        if value:
            if multi_sheet:
                for _name, _df in df.items():
                    df[_name] = df[_name].values
                data = df
            else:
                data = df.values
        else:
            data = df
    except ValueError as err:
        print(err)

    if to_list:
        def _to_list(_data):
            _data_list = _data.tolist()
            if not isinstance(_data_list, list):
                _data_list = [_data_list]
            return _data_list

        if multi_sheet:
            if concat:
                concat_data = []
                for _name, _df in data.items():
                    concat_data.extend(_to_list(data[_name]))
                return concat_data
            else:
                for _name, _df in data.items():
                    data[_name] = _to_list(data[_name])
                return data
        else:
            return _to_list(data)

    return data


def load_csv(*args, to_list=False, **kwargs) -> Union[ndarray, Any]:
    """
    读取csv文件

    :param args: 需要读取的文件
    :param to_list: 将输出结果从np转为list
    :param kwargs: pd.read_csv的参数
    :return: 读取的数据

    >>> dump_csv([['name', 'score'], ['A', 1], ['B', 2]], './demo.csv')
    WARNING: default set header=False
    './demo.csv'
    >>> load_csv('./demo.csv')
    array([['A', 1],
           ['B', 2]], dtype=object)
    >>> load_csv('./demo.csv', to_list=True)
    [['A', 1], ['B', 2]]
    """
    kwargs['keep_default_na'] = False if 'keep_default_na' not in kwargs else kwargs['keep_default_na']

    df = pd.read_csv(*args, **kwargs)
    data = df.values
    if to_list:
        return data.tolist()
    return data


def dozip(src: str, tgt: str = '') -> NoReturn:
    """
    zip a file or a director.

    :param src: a file or a director
    :param tgt: Optional, the output file
    :return: NoReturn
    """
    warnings.warn("dozip即将废弃，因为："
                  "1、引入额外的库zipfile不便维护，"
                  "2、用os指令或subprocess.check_output来重写此函数兼容性更好", DeprecationWarning)

    try:
        import zipfile
    except ModuleNotFoundError:
        pip_install('zipfile')
        import zipfile

    # if tgt is Empty, then name the zipped file with a suffix .zip and save in the same director of src file/dir
    if not tgt:
        src_path, src_name = os.path.split(os.path.normpath(src))
        tgt = os.path.join(src_path, src_name+'.zip')
    # if tgt is a director, then name the zipped file with a suffix .zip and save in the director tgt
    _, tgt_name = os.path.split(tgt)
    if '.' not in tgt_name:
        src_path, src_name = os.path.split(os.path.normpath(src))
        tgt = os.path.join(tgt, src_name+'.zip')
    make_dir(tgt, file=True)
    z = zipfile.ZipFile(tgt, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(src):
        f_path = dir_path.replace(src, '')
        f_path = f_path and f_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path+filename)
    z.close()


def unzip(src: str, tgt: str = '') -> NoReturn:
    """
    unzip a .zip file

    :param src: a zipped file
    :param tgt: Optional, the output file or dir
    :return: NoReturn
    """
    warnings.warn("unzip即将废弃，因为："
                  "1、引入额外的库zipfile不便维护，"
                  "2、用os指令或subprocess.check_output来重写此函数兼容性更好", DeprecationWarning)
    try:
        import zipfile
    except ModuleNotFoundError:
        pip_install('zipfile')
        import zipfile

    if not tgt:
        tgt, _ = os.path.split(os.path.normpath(src))
    make_dir(tgt, file=True)
    r = zipfile.is_zipfile(src)
    if r:
        fz = zipfile.ZipFile(src, 'r')
        for file in fz.namelist():
            fz.extract(file, tgt)
    else:
        print('This is not a zip file')


def split_path(file_path: str) -> Tuple[str, str, Any, Any]:
    """
    切分文件路径为：所属文件夹、文件全名、文件名、后缀。
    如果输入是文件夹，则不会切分。

    :param file_path: 文件路径
    :return: 所属文件夹、文件全名、文件名、后缀

    >>> split_path('/root/demo/book.2023.txt')
    ('/root/demo', 'book.2023.txt', 'book.2023', '.txt')
    >>> split_path('/root/demo/')   # 输入文件夹路径
    ('/root/demo', '', '', '')
    """
    dir_name, full_file_name = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(full_file_name)
    return dir_name, full_file_name, file_name, file_ext


def get_file_etime(path: str, **kwargs) -> Iterator[Tuple[str, float]]:
    """
    获取文件或目录下所有文件的创建时间

    :param path: 文件夹或文件的路径
    :param kwargs: 传递给get_file的参数
    :return: 文件名，创建时间

    >>> dump_lines([], './demo/A/2.txt')
    './demo/A/2.txt'
    >>> dump_lines([], './demo/1.txt')
    './demo/1.txt'
    >>> sorted(list(get_file_etime('./demo')))  # doctest: +ELLIPSIS
    [('./demo/1.txt', ...), ('./demo/A/2.txt', ...)]
    >>> sorted(list(get_file_etime('./demo/1.txt')))  # doctest: +ELLIPSIS
    [('./demo/1.txt', ...)]
    """
    for file in get_file(path, **kwargs):
        yield file, os.path.getmtime(file)


def get_new_file(folder: str, **kwargs) -> List[str]:
    """
    获取目录下的所有文件，并按创建时间排序，新建的文件排在前面。

    :param folder: 目录
    :param kwargs: 传递给get_file_etime的参数
    :return: 按创建时间排序的文件，新的在前旧的在后

    >>> dump_lines([], './demo/A/2.txt')
    './demo/A/2.txt'
    >>> dump_lines([], './demo/1.txt')
    './demo/1.txt'
    >>> sorted(list(get_new_file('./demo')))
    ['./demo/1.txt', './demo/A/2.txt']
    """
    # 忽略目录
    if not is_folder(folder):
        raise ValueError('输入的目录路径无效')
    fet = list(get_file_etime(folder, **kwargs))
    fet.sort(key=lambda f: f[1], reverse=True)
    return [f[0] for f in fet]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
