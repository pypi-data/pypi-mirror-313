# -*- coding: UTF-8 -*-
# 每个模块仅依赖同r或低r模块函数
# 在行备注中备注依赖的同r函数，以避免循环导入
# 在行备注中备注依赖的第三方包，包名前额外添加符号*或+以区分于同r函数，以便检查不合理的依赖关系
# *符号表示可选，不写入requirements.txt。+符号会写入
# 不标出[标准库](https://docs.python.org/zh-cn/3.8/library/index.html)

# in-package data path
from aitool.r3_datasets import PATH as DATA_PATH
# web data path
from aitool.config import DATASET_WEB as WEB_PATH, USER_CONFIG

# r0_standard
# 仅依赖python标准库
from aitool.r0_standard.retry import retry
from aitool.r0_standard.time_op import exe_time, timeout, format_time, timestamp, get_lastday_timestamp
from aitool.r0_standard.print_op import print_color, print_red, print_green, print_yellow, print_blue
from aitool.r0_standard.dict_op import split_dict
from aitool.r0_standard.random_op import weight_random, random_base64
from aitool.r0_standard.scoring import apr
from aitool.r0_standard.security import encrypt_md5
from aitool.r0_standard.path import get_user_root_path, get_current_path
from aitool.r0_standard.singleton import singleton, Singleton
from aitool.r0_standard.string_op import is_contain, get_str, is_contains_english, cut_until_char, delete_char, \
    is_contains_figure, is_contains_chinese, rate_chinese, is_all_chinese, get_chinese, is_no_symbol, \
    find_all_position, get_ngram, get_ngrams, ngrams_permutation, token_hit, filter_keyword
from aitool.r0_standard.deduplication import Deduplication, deduplicate  # encrypt_md5
from aitool.r0_standard.cache import cache, get_cache, Cache  # get_str
from aitool.r0_standard.re_op import replace_text, split_char, split_punctuation  # Cache

# BASIC FUNCTION
from aitool.r1_basic.pip_tool import pip_install_by_os, pip_install_by_main, pip_install  # +pip
from aitool.r1_basic.distribution import standard, normalize, cross_entropy, scale_array, get_cos_similar  # +numpy
from aitool.r1_basic.file import dozip, unzip, abspath, split_path, dump_json, load_json, dump_pickle, load_pickle, \
    dump_lines, load_byte, load_line, load_lines, dump_excel, load_excel, dump_csv, load_csv, get_file_etime, \
    get_new_file, is_writable, is_file_exist, is_file, is_folder, make_dir, is_file_hidden, get_file, \
    add_python_path  # pip_install, +numpy, +pandas
from aitool.r1_basic.format_data import flatten, html2text, content2text, split_part, get_pair, np2list, \
    get_most_item, dict2ranked_list  # *bs4, *lxml, +numpy
from aitool.r1_basic.multi import pool_map, pool_starmap, multi_map, get_functions, multi  # +multiprocess
from aitool.r1_basic.shell import shell, mkdir, shell_cp, shell_mv, cp, mv, install_conda, activate_env, \
    create_env  # is_folder, is_file
from aitool.r1_basic.download import download_file, get_download_dir, get_aitool_data, prepare_data, calculate_md5, \
    check_md5, DownloadMethod, ProcessMethod, extract_archive  # split_path, +requests
from aitool.r1_basic.conda import init_env
from aitool.r1_basic.log_tool import get_log, Record  # dump_lines

# ARITHMETIC FUNCTION
from aitool.r2_structure.arithmetic.dfs_search import Node, dfs, ranked_permutation

# NLP FUNCTION
from aitool.r4_algorithm.basic.split_sentence import split_sentence
from aitool.r4_algorithm.basic.conditional_probability import conditional_probability
from aitool.r4_algorithm.basic.phoneticize import get_pinyin
from aitool.r4_algorithm.basic.ngram_tf_idf import get_ngram_tf, get_ngram_idf
from aitool.r4_algorithm.basic.word import has_family_name, is_common_word, is_stop_word, \
    is_relationship_title, delete_age_describe, is_black_name, clean_role, clean_alias, delete_nested_text, \
    select_nested_text, is_sub_ip, get_core_ip, get_common_word, get_stop_word, get_relationship_title, \
    get_punctuation, is_punctuation, is_nick_name
from aitool.r4_algorithm.basic.noise import add_random_token, delete_random_token, replace_random_token, \
    random_token_permutation, add_noise
from aitool.r4_algorithm.basic.similar import term_similar, term_similar_bag
from aitool.r4_algorithm.nlp.sentiment_analysis.dict_match import Sentiment
from aitool.r4_algorithm.nlp.sentiment_analysis.text_similar import load_word2vec, cos_sim, VectorSim, vector_sim, char_sim, \
    de_sim, generate_offline_sim, ngram_sim
from aitool.r4_algorithm.chatgpt.chatgpt import chatgpt
from aitool.r4_algorithm.graph.paris.objects.Entity import Entity
from aitool.r4_algorithm.graph.paris.objects.Relation import Relation
from aitool.r4_algorithm.graph.paris.objects.KG import KG
from aitool.r4_algorithm.graph.paris.objects.KGs import KGs
from aitool.r4_algorithm.graph.paris.tool.dataloader import construct_kg
from aitool.r4_algorithm.graph.paris.examples.core_example import alignment
from aitool.r4_algorithm.interface.mt_google import translate, recognize_language
from aitool.r4_algorithm.interface.doubao import infer_doubao
from aitool.r4_algorithm.llm.infer.baichuan import infer_baichuan
from aitool.r4_algorithm.llm.autoprompt.unit import AutoPrompt
from aitool.r4_algorithm.llm.autoprompt.interface import AutoPromptApp
