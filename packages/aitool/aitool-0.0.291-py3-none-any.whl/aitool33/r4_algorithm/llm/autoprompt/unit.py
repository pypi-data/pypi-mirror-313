# -*- coding: UTF-8 -*-
import math
from collections import defaultdict, Counter
from random import sample, randint, shuffle
from time import sleep, time, gmtime, strftime
from typing import List, Tuple, Any, Dict, Callable

from tqdm import tqdm

from aitool import ngram_sim, split_punctuation, is_punctuation, infer_doubao, Record

Input = str
Output = str
Label = str
Comment = str
InputIdx = 2
OutputIdx = 0
LabelIdx = 1
CommentIdx = 3
Prompt = str

LabeledCase = Tuple[Output, Label, Input, Comment]
Generation = 'generation'
Classification = 'classification'


class UndefinedTask(Exception):
    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return '未定义的任务类型'


class AutoPrompt:
    def __init__(
            self,
            task: str,
            dataset: List[LabeledCase] = None,
            label_good: str = None,
            label_bad: str = None,
            window_size: int = 5,
            beam_size: int = 2,
            derive_time: int = 2,
            iteration: int = 2,
            target_inputs: List[Input] = None,
            target_size: int = 100,
            split_subtask: bool = False,    # split_subtask = True 还需要多实验各种极端情况, 默认还是设置False
            auto_task_kind: bool = True,    # task_kind is None 时有效
            task_kind: str = None,
            name: str = '',
            llm_interface: Callable = infer_doubao,
    ):
        """
        自动优化prompt
        :param task: 任务描述
        :param dataset: 已标注数据
        :param label_good: 优质数据的标签
        :param label_bad: 低质数据的标签
        :param window_size: 迭代过程中数据集里的case数量
        :param beam_size: 寻找举报最优解的窗口
        :param derive_time: 求梯度的次数
        :param iteration: 迭代轮次
        :param target_inputs: case级别的输入信息
        :param target_size: 生成数据的量
        :param split_subtask: 是否划分子任务
        :param auto_task_kind: 自动判断任务类型
        :param task_kind: 任务类型
        :param name: 任务名
        :param llm_interface: 调用大模型接口
        """
        self.task = task
        self.dataset = dataset if dataset is not None else []
        self.label_good = label_good if label_good is not None else 'good'
        self.label_bad = label_bad if label_bad is not None else 'bad'
        self.window_size = window_size
        self.beam_size = beam_size
        self.derive_time = derive_time
        self.iteration = iteration
        self.target_inputs = target_inputs if target_inputs is not None else ['']
        self.target_size = target_size
        self.split_subtask = split_subtask
        self.auto_task_kind = auto_task_kind
        self.task_kind = task_kind
        self.task_name = name
        self.llm_interface = llm_interface
        self.record = Record(name=self.task_name)
        self.note_params()

        self.output_limited = False
        self.all_allowed_outputs = []
        self.good_case = []
        self.inspector_prompt = None
        self.subtasks = []
        self.subdatasets = []
        self.all_final_prompts = []
        self.prompt2case = {}
        self.prompt2gradient = defaultdict(list)
        self.output_prompts = []
        self.output_case_texts = []
        self.output_case_inputs = []

        # 分类任务专属
        self.is_multi_label = False
        self.split_punctuation = ','  # 多分类任务用来拼接label的符号
        self.validate_cases = []
        self.validate_inputs = []
        self.prompt2precision = {}
        self.prompt2wrong_cases_str = {}

    def work(self) -> Tuple[List[Prompt], List[Input], List[Output]]:
        if self.task_kind is not None:
            self.auto_task_kind = False
        if self.auto_task_kind:
            self.get_task_kind()

        self.get_output_limitation()
        self.get_classification_type()

        if self.split_subtask:
            self.get_subtasks()
            self.get_subdatasets()
        else:
            self.subtasks = [self.task]
            self.subdatasets = [self.dataset]
        self.time_estimate()

        self.good_cases = self.pick_dataset(self.dataset, self.label_good, len(self.dataset))

        if self.task_kind == Generation:
            # 检查器（用于分类和修正），在全部数据上获取，不针对子任务
            self.inspector_prompt = self.get_inspector_prompt()
            self.record.note(('inspector_prompt_init', self.inspector_prompt))
            self.rewrite_inspector_prompt()
            self.record.note(('inspector_prompt_rewrite', self.inspector_prompt))
        elif self.task_kind == Classification:
            # 分类任务不支持 subtask
            assert self.split_subtask is False
            # 分类任务从全量数据中筛选出一个评测集。TODO 优先保证正负样本均衡，然后在案input占比分配case
            self.validate_cases, _ = self.split_dataset(self.good_cases, self.window_size, balance_idx=OutputIdx)
            shuffle(self.validate_cases)
            self.validate_inputs = [case[InputIdx] for case in self.validate_cases]
        else:
            raise UndefinedTask

        # 迭代prompt
        for subtask, subdataset in zip(self.subtasks, self.subdatasets):
            prompt_init = self.task2prompt(subtask, subdataset)
            self.record.note(('subtask', subtask))
            self.record.note(('subdataset', subdataset))
            self.record.note(('prompt_init', prompt_init))
            self.all_final_prompts.append(self.beam_search(subtask, prompt_init, subdataset, self.iteration))

        # 批量生成数据
        self.infer_inputs()

        self.record.note(('output_prompts', self.output_prompts))
        self.record.note(('output_case_inputs', self.output_case_inputs))
        self.record.note(('output_case_texts', self.output_case_texts))
        self.record.finish()
        return self.output_prompts, self.output_case_inputs, self.output_case_texts

    def get_task_kind(self):
        records = [
            [
                """请判断下列【任务】的任务类型是生成任务还是分类任务。直接输出“是生成任务。”或“是分类任务。”，不要输出分析过程，直接输出任务类型即可。\n\n【任务：】\n{}\n\n【任务类型：】""",
                [self.task], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        if '分类任务' in rst:
            self.task_kind = Classification
        elif '生成任务' in rst:
            self.task_kind = Generation
        else:
            self.task_kind = Generation
        self.record.note(('get_task_kind', rst))
        self.record.note(('get_task_kind', self.task_kind))

    def get_output_limitation(self):
        output_cases_str = '\n'.join([case[OutputIdx] for case in self.dataset][:10])
        template = """请结合【任务输出示例】判断【任务】的输出是否为有限的集合。如果是，则写出该任务所有可能输出的集合，集合中的元素用“,”分隔。如果不是或难以判断，则写出一个空集。\n以下是一些示例：\n【示例任务：】\n生成一句打招呼的话\n【所有可能输出的集合：】\n{}\n\n【示例任务：】\n依据输入数据输出它的类别标签\n【所有可能输出的集合：】\n{}\n\n【示例任务：】\n处罚力度按月来计算，最小的月数是3，最大是7。请判断应该处以几个月的处罚最合适。\n【所有可能输出的集合：】\n{3, 4, 5, 6, 7}\n\n【示例任务：】\n请判断输入的类别。类别分为：A1、A5、C2、None。 \n【所有可能输出的集合：】\n{A1, A5, C2, None}\n\n【示例任务：】\n对于用户的输入需要回答“对”或“不对”，并给出理由。\n【所有可能输出的集合：】\n{}\n\n【示例任务：】\n判断分析过程是否正确，生成判断的结果，仅输出“对”、“不对”、“不知道”，不要输出原因。\n【所有可能输出的集合：】\n{对, 不对, 不知道}\n\n【示例任务：】\n对文章进行分类，如果文章体现出作者高兴的情绪就输出高兴，如果体现出愤怒的情绪就输出愤怒，其他情况输出平静。\n【所有可能输出的集合：】\n{高兴, 愤怒, 平静}\n\n【示例任务：】\n对文章进行分类，如果文章体现出作者高兴的情绪就输出高兴，如果体现出愤怒的情绪就输出愤怒。如果不属于这两种情况，就输出最匹配的一个情绪词。\n【所有可能输出的集合：】\n{}\n\n请输出下述【任务】的【所有可能输出的集合】\n【任务：】\n""" + self.task + """\n\n【所有可能输出的集合：】"""
        rst = self.call_llm(template)
        task_output_set = [_.strip() for _ in rst.replace('{', '').replace('}', '').split(',')]
        dataset_output_set = set([case[OutputIdx] for case in self.dataset])

        self.output_limited = False
        self.all_allowed_outputs = {}
        if len(task_output_set) > 0:
            is_all_contain = True
            # 处理多分类的包含情况。 TODO 目前只支持符号分割的拼接方式
            for case_output in dataset_output_set:
                if case_output in task_output_set:
                    continue
                for item in [_.strip() for _ in split_punctuation(case_output)]:
                    if len(item) > 0 and item not in task_output_set:
                        is_all_contain = False
                        break
                if not is_all_contain:
                    break
            if is_all_contain:
                self.output_limited = True
                self.all_allowed_outputs = task_output_set
        self.record.note(('output_limited', self.output_limited))
        self.record.note(('all_allowed_outputs', self.all_allowed_outputs))

    def get_output_limitation_str(self):
        if not self.output_limited:
            return ''
        allowed_outputs_str = '、'.join(self.all_allowed_outputs)
        text = '不允许输出额外的推理过程，输出的必须为这些内容中的一个或多个：{}。即使是缺少信息无法判断或与所有可选的输出内容都无关，也只能输出这些内容中的一个或多个：{}。'.format(allowed_outputs_str, allowed_outputs_str)
        return text

    def get_classification_type(self):
        if self.task_kind != Classification:
            self.is_multi_label = False
            return

        output_cases_str = '\n'.join([case[OutputIdx] for case in self.dataset][:10])
        records = [
            [
                """请基于下列【任务描述】和【样例输出数据】判断该任务是否是多标签分类任务，即一个样例的输出里可以包含1个或多个类别标签。判断结果直接输出“是多标签分类任务。”或“不是。”，不要输出分析过程。\n\n【任务描述：】\n{}\n\n【样例输出数据（每行为1个样例的输出）：】\n{}\n\n【判断结果：】""",
                [self.task, output_cases_str], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        if '不是' in rst:
            self.is_multi_label = False
        elif '是多标签分类任务' in rst:
            self.is_multi_label = True
            self.get_split_punctuation()
        else:
            self.is_multi_label = False
        self.record.note(('is_multi_label', self.is_multi_label))

    def get_split_punctuation(self):
        all_output_str = ''.join([case[OutputIdx] for case in self.dataset])
        punctuations = Counter([_ for _ in all_output_str if is_punctuation(_)])
        most_common = punctuations.most_common()
        if len(most_common) > 0:
            self.split_punctuation = most_common[0][0]

    def infer_inputs(self):
        # 批量生成数据
        task_size = math.ceil(self.target_size / len(self.subtasks))  # 平分要生成的数据量
        for final_prompts, subdataset in zip(self.all_final_prompts, self.subdatasets):
            prompt = final_prompts[0]
            self.output_prompts.append(prompt)
            if self.task_kind == Generation:
                cases = self.get_cases(
                    prompt,
                    task_size,
                    self.target_inputs,
                    dataset=subdataset,
                    use_inspector_rewrite=True,
                    use_allowed_outputs=True,
                )
            elif self.task_kind == Classification:
                cases = self.get_cases(
                    prompt,
                    task_size,
                    self.target_inputs,
                    do_variety=False,
                    num_consistent=True,
                    use_allowed_outputs=True,
                )
            else:
                raise UndefinedTask
            for case in cases:
                self.output_case_inputs.append(case[2])
                self.output_case_texts.append(case[0])

    @staticmethod
    def description():
        description = """AutoPrompt包括2个模块，支持多模块生成/分类任务：
1、自动优化prompt：模拟人工调优prompt的过程，得到一个较好的prompt。
2、批量生成物料：LLM批量调用模块 + 多样性增强模块 + 低质数据清洗/改写模块”。
        """
        return description

    def rewrite_inspector_prompt(self):
        records = [
            [
                """修改分类任务的【原prompt】,要求保持原本的信息不缺失，并将其输出格式修改为：“\n【分类结果】\n（该分类prompt原本的结果，即是否符合要求）。\n【修正后的输入】\n（如果不合符要求就额外输出修正后的输入，使其符合要求。如果已经符合要求，则输出“无需修正”）”。\n\n【原prompt:】\n{}\n\n【修改输出格式后的prompt:】\n""",
                [self.inspector_prompt], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        self.inspector_prompt = self.call_llm(template)

    def get_inspector_prompt(self) -> str:
        case_good = self.pick_dataset(self.dataset, self.label_good, len(self.dataset))
        case_bad = self.pick_dataset(self.dataset, self.label_bad, len(self.dataset))
        task = self.generation2classification_task(self.task, self.label_good, self.label_bad)
        dataset = self.generation2classification_dataset(case_good + case_bad)
        inspector_prompt = ''
        if len(case_good) >= 5 and len(case_bad) >= 5:
            ap = AutoPrompt(
                task,
                dataset,
                self.label_good,
                self.label_bad,
                window_size=20,
                beam_size=2,
                derive_time=1,
                iteration=2,
                target_inputs=[],
                target_size=0,
                split_subtask=False,
                task_kind='classification',
            )
            output_prompts, output_input, output_text = ap.work()
            inspector_prompt = output_prompts[0]
        return inspector_prompt

    @staticmethod
    def generation2classification_dataset(dataset: List[LabeledCase]) -> List[LabeledCase]:
        dataset_new = []
        for case in dataset:
            c_output, c_label, c_input, c_comment = case
            if len(c_input) > 0:
                new_input = 'input: ' + c_input + '\noutput: ' + c_output
            else:
                new_input = c_output
            dataset_new.append((c_label, 'good', new_input, c_comment))
        return dataset_new

    @staticmethod
    def generation2classification_task(task: str, label_good: str, label_bad: str) -> str:
        records = [
            [
                """依据生成任务的【任务描述:】\n{}\n\n已生成了一些数据，请判定生成的数据是否符合上述生成任务的要求。如果符合要求就输出“{}”,如果不符合要求就输出“{}”""",
                [task, label_good, label_bad], """第一版"""],
        ]
        task = records[-1][0].format(*records[-1][1])
        return task

    @staticmethod
    def aggregate_dataset(dataset: List[LabeledCase], target_idx: int = InputIdx) -> Dict:
        # 按target_id列汇总数据
        target2cases = defaultdict(list)
        for labeled_case in dataset:
            target = labeled_case[target_idx]
            target2cases[target].append(labeled_case)
        return target2cases

    def time_estimate(self):
        """预估耗时。不包含已用于做子任务划分的时间"""
        second_per_call = 4.95  # 平均调用一次大模型的时间(秒)
        case_per_call = 1.17       # 平均调用一次大模型获得的case数量

        # 生成新的prompt调用llm的次数。每个都先算梯度，再生产，再清洗
        time_propose = 3 * self.beam_size * self.derive_time * self.iteration
        # 计算每个prompt的样例数据调用llm的次数。初始有 self.beam_size 个 prompt。每轮迭代新获得self.beam_size * self.derive_time 个 prompt
        # 每份样例数据要包含 self.window_size 个数据，生成数据后额外需要清洗一次格式
        time_get_cases = (self.beam_size * self.derive_time * self.iteration + self.beam_size) * (self.window_size / case_per_call + 1)
        # 两两对比计算分数调用llm的次数
        if self.task_kind == Generation:
            time_rank_score = (self.beam_size * self.derive_time + self.beam_size) ^ 2
        elif self.task_kind == Classification:
            time_rank_score = 0
        else:
            raise UndefinedTask
        # 推理过程调用llm的次数。
        time_inference = self.target_size / case_per_call
        # 总的调用llm的次数。
        time_whole = time_propose + time_get_cases + time_rank_score + time_inference
        # 总耗时（小时）
        hour_estimated = time_whole * second_per_call * len(self.subtasks)
        self.record.note(('预估耗时', '{}'.format(strftime("%H:%M:%S", gmtime(hour_estimated)))))

    def note_params(self):
        members = dir(self)
        filtered_members = [m for m in members if not m.startswith('__')]
        for member in filtered_members:
            value = getattr(self, member)
            if callable(value):
                continue
            self.record.note(('参数 :: {}'.format(member), value))

    def call_llm(self, prompt: str, llm: str = 'doubao') -> str:
        """
        调用大模型生成结果
        :param prompt:
        :param llm:
        :return:
        """
        try_time = 3
        sleep_second = [0, 120, 60, 30]
        if len(sleep_second) <= try_time:
            raise ValueError('len sleep_second is less than or equal try_time')
        while try_time > 0:
            try:
                self.record.note(('>>> call_llm', prompt))
                if llm == 'doubao':
                    rst = self.llm_interface([prompt])
                else:
                    raise ValueError('llm:'.format(llm))
                self.record.note(('>>> rst_llm', rst))
                return rst
            except Exception as e:
                print(e)
                sleep(sleep_second[try_time])
                try_time -= 1
        return ''

    def merge_rst(self, llm_rsts: List[str]) -> str:
        """
        汇总多个大模型的结果 TODO
        """
        self.record.note(('>>> call_llm', llm_rsts))
        return ''

    def variety_prompt(
            self,
            prompt: str,
            dataset: List[LabeledCase],
            use_example: bool = True,
            multi_gen: bool = False,
    ) -> str:
        """基于规则对prompt进行多样性修饰"""
        additional_prompt = ''

        # 用good_dataset做多样性
        if use_example:
            good_dataset = self.pick_dataset(dataset, self.label_good, self.window_size)

            if len(good_dataset) > 0:
                example_str = self.get_example_str(good_dataset, min_num=2)
                additional_prompt += example_str

        # 一次调用生成多个case
        if multi_gen:
            additional_prompt += '请生成{}条数据，不同数据之间用换行符进行分割。'.format(randint(5, 10))

        # 寻找合适的插入位置
        if len(additional_prompt) > 0:
            splits = prompt.rsplit('【', maxsplit=1)
            if len(splits) == 2:
                spl, spr = splits
            else:
                spl, spr = '', prompt
            new_prompt = spl + additional_prompt + spr
        else:
            new_prompt = prompt
        return new_prompt

    def task2subtask(self, task: str) -> List[str]:
        records = [
            [
                """请判断【任务描述】是否包含多个并列的目标或领域，如果有请拆分出多个子任务，并用换行符分割不同的子任务。每个子任务都需要保留【任务描述】的其他所有任务要求、限制条件、格式要求等信息。\n【任务描述:】\n{}\n【子任务:】\n""",
                [task, ], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)

        subtask = []
        for raw_subtask in rst.split('\n'):
            raw_subtask = raw_subtask.strip()
            sim = ngram_sim(raw_subtask, task, 3)
            if sim < 0.5:
                continue
            subtask.append(raw_subtask)

        if len(subtask) == 0:
            subtask = [task]
        return subtask

    def get_subdataset(self, task: str, clean_space: bool = True) -> List[LabeledCase]:
        string2case = {}
        all_string = []
        for case in self.dataset:
            c_str = case[0]
            if clean_space:
                c_str = c_str.replace(' ', '')
            string2case[c_str] = case
            all_string.append(c_str)

        records = [
            [
                """请判断【数据集】中的哪些任务属于【子任务】，并用换行符分割不同的数据。\n【数据集:】\n{}\n【子任务:】\n{}\n【属于该子任务的数据:】\n""",
                [all_string, task], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        substring = []
        for r in rst.split('\n'):
            r = r.strip()
            r = r.replace(' ', '')
            substring.append(r)
        subdataset = []
        for c_str in substring:
            if c_str in string2case:
                subdataset.append(string2case[c_str])
            else:
                print('c_str not in string2case', c_str)
                sim_rank = []
                for p_str in all_string:
                    sim = ngram_sim(c_str, p_str, 3)
                    sim_rank.append([p_str, sim])
                sim_rank = sorted(sim_rank, key=lambda x: x[1], reverse=True)
                if sim_rank[0][1] > 0.92:
                    subdataset.append(string2case[sim_rank[0][0]])
        return subdataset

    def task2prompt(
            self,
            task: str,
            dataset: List[LabeledCase],
            use_rule: bool = True,
            use_llm: bool = True,
            use_example: bool = True,
    ) -> List[str]:
        """
        将用户自然语言的任务描述转写为prompt
        :param task:
        :param dataset:
        :param use_rule:
        :param use_llm:
        :param use_example:
        :return:
        """
        raw_prompt = []

        example_str = ''
        output_format_str = ''
        output_limitation_str = self.get_output_limitation_str()

        if use_example:
            # 附加少量（3~4个）示例
            if self.task_kind == Generation:
                example_cases, _ = self.split_dataset(self.good_cases, randint(3, 4), balance_idx=InputIdx)
            elif self.task_kind == Classification:
                example_cases, _ = self.split_dataset(self.good_cases, randint(3, 4), balance_idx=OutputIdx)
            else:
                raise UndefinedTask
            shuffle(example_cases)
            example_str = self.get_example_str(example_cases, use_all=True)
            output_format_str = self.get_output_format_str(task, example_str)

        if self.task_kind == Generation:
            if use_rule:
                records = [
                    [[
                        """依据【任务描述】生成数据。生成的多条数据之间用换行符分割。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【生成的数据:】\n""",
                    ], [task], """第一版"""],
                ]
                for platform in records[-1][0]:
                    template = platform.format(*records[-1][1])
                    prompt = template.replace('$示例数据$', example_str).replace('$输出格式$', output_format_str).replace('$输出限制$', output_limitation_str)
                    raw_prompt.append(prompt)
            if use_llm:
                records = [
                    [[
                        """请将【任务描述】改写为数据生成任务的【prompt】。\n一个prompt需要精练地说明生成任务的背景、生成目标、限制条件、示例、输出格式。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【prompt:】\n""",
                        """请基于以下【任务描述】生成一个数据生成任务的【prompt】。生成的【prompt】应包括：生成任务的背景、生成目标、限制条件、示例、输出格式。$示例数据$\n$输出限制$\n$输出格式$\n【任务描述:】\n{}\n【prompt:】\n""",
                    ], [task], """第一版"""],
                ]
                for platform in records[-1][0]:
                    template = platform.format(*records[-1][1])
                    template = template.replace('$示例数据$', example_str).replace('$输出格式$', output_format_str).replace('$输出限制$', output_limitation_str)
                    prompt = self.call_llm(template)
                    raw_prompt.append(prompt)
        elif self.task_kind == Classification:
            if use_rule:
                records = [
                    [[
                        """分类任务：\n{}\n。$示例数据$\n$输出限制$\n$输出格式$\n【以下是待分类的数据:】\n""",
                    ], [task], """第一版"""],
                ]
                for platform in records[-1][0]:
                    template = platform.format(*records[-1][1])
                    template = template.replace('$示例数据$', example_str).replace('$输出格式$', output_format_str).replace('$输出限制$', output_limitation_str)
                    raw_prompt.append(template)
        else:
            raise UndefinedTask

        cleaned_prompt = []
        for prompt in raw_prompt:
            cleaned_prompt.append(self.clean_prompt(prompt))
        return cleaned_prompt

    def get_output_format_str(self, task, example_str):
        records = [
            [
                """请分析【任务】的【示例数据】，然后结出这个任务的【输出格式】。\n\n【任务：】\n{}\n\n【示例数据：】\n{}\n\n【输出格式：】\n""",
                [task, example_str], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        return rst

    def get_example_str(
            self,
            dataset,
            min_num: int = 1,
            max_num: int = 10,
            add_header: bool = True,
            use_all: bool = False,
    ) -> str:
        example_case = ''
        if len(dataset) >= 1:
            if add_header > 0:
                example_case += '\n【示例数据:】\n'
            data_texts = self.get_texts(dataset)
            example_case += self.sampled_string(data_texts, min_num, max_num, use_all=use_all) + '\n'
        return example_case

    @staticmethod
    def sampled_string(texts, min_num: int, max_num: int, use_all: bool):
        if use_all:
            sampled_texts = texts
        else:
            min_num = min(min_num, len(texts))
            max_num = min(max_num, len(texts))
            sampled_texts = sample(texts, randint(min_num, max_num))
        return '\n'.join(sampled_texts)

    def get_output(self, prompt: str, target_input: str = None) -> str:
        """
        用大模型基于prompt生成数据
        :param prompt:
        :param target_input:
        :return:
        """
        if target_input is None or target_input == '':
            rst = self.call_llm(prompt)
        else:
            rst = self.call_llm(prompt + '输入：\n{}\n输出：\n'.format(target_input))
        return rst

    def rewrite_output(self, input_case: str, output_case: str):
        ans = self.get_cases(
            self.inspector_prompt,
            1,
            [self.get_text((output_case, '', input_case, ''))],
            do_variety=False,
        )
        rw = ''
        rst = ans[0][0].split('【修正后的输入】', 1)
        if len(rst) == 2:
            if '无需修正' not in rw:
                rw = rst[1]
        sim = ngram_sim(output_case, rw, 3)
        if sim >= 0.4:
            return rw
        self.record.note(('>>> rewrite_input', self.get_text((output_case, '', input_case, ''))))
        self.record.note(('>>> rewrite_output', ans))
        self.record.note(('>>> rewrite_text', output_case))
        return output_case

    def get_cases(
            self,
            prompt: str,
            size: int,
            inputs: List[str],
            dataset: List[LabeledCase] = None,
            do_variety=True,
            use_example: bool = True,   # do_variety=True时才有效
            multi_gen: bool = False,    # do_variety=True时才有效
            delete_same: bool = True,
            clean=False,
            num_consistent: bool = False,
            use_inspector_rewrite: bool = False,
            use_allowed_outputs: bool = False,  # 使用allowed_outputs纠正输出
    ) -> List[LabeledCase]:
        """
        批量生成case, 添加多样性（示例、输出数量等），并对结果去重
        如果是生成任务不允许delete_same、clean、multi_gen
        """
        if self.task_kind == Classification:
            multi_gen = False
            delete_same = False
            clean = False
            num_consistent = True

        if len(inputs) == 0:
            inputs = ['']
        distribute = self.average_split(size, len(inputs))

        cases = []
        all_try_times = 0
        for input_case, input_size in zip(inputs, distribute):
            rst = []
            try_times_max = input_size // 0.9 + 1
            try_times = 0
            while len(rst) < input_size:
                if try_times >= try_times_max:
                    break
                try_times += 1
                all_try_times += 1

                if do_variety:
                    if dataset is None:
                        raise ValueError('need provide dataset if do_variety ')
                    prompt_new = self.variety_prompt(prompt, dataset, use_example=use_example, multi_gen=multi_gen)
                else:
                    prompt_new = prompt

                outputs = self.get_output(prompt_new, target_input=input_case).split('\n')

                for output in outputs:
                    output = output.strip()
                    if delete_same:
                        if output in rst:
                            continue
                    if len(output) == 0:
                        continue
                    rst.append(output)

                if num_consistent:
                    # 分类任务必须严格生成input_size个结果，如果过多就截断，如果过少就补''
                    if len(rst) < input_size:
                        rst += [''] * (input_size - len(rst))
                    else:
                        rst = rst[:input_size]

                if clean:
                    if len(rst) >= input_size:  # 在积累了一定量级数据后才执行
                        # TODO 量太大时要分批处理, 没去没有启用这个流程
                        outputs_cleaned = self.clean_case(prompt, '\n'.join(rst))
                        rst = list(set(outputs_cleaned))

            for output in rst:
                if use_inspector_rewrite and self.inspector_prompt is not None:
                    output = self.rewrite_output(input_case, output)
                if use_allowed_outputs:
                    output = self.get_allowed_output(output)
                cases.append((output, '', input_case, ''))

            self.record.note(('[part] get cases try times', try_times))
            self.record.note(('[part] get case num', len(rst)))

        self.record.note(('[whole] get cases try times', all_try_times))
        self.record.note(('[whole] get case num', len(cases)))
        self.record.note(('inference_prompt', prompt))
        self.record.note(('inference_cases', cases))
        return cases

    @staticmethod
    def get_best_label(text, labels) -> tuple[str, float]:
        label_score = []
        for label in labels:
            label_score.append([label, ngram_sim(text, label, 3)])
        shuffle(label_score)    # 在分值全一样时增加随机性
        label_score.sort(key=lambda x: x[1], reverse=True)
        return label_score[0][0], label_score[0][1]

    def get_allowed_output(self, ori_output: str) -> str:
        # 对于多标签分类任务，仅支持通过符号连接多个标签的情况
        # 如果标签本身含有标点符合，则会被错误识别为多个标签
        if not self.output_limited:
            return ori_output
        if ori_output in self.all_allowed_outputs:
            return ori_output

        if not self.is_multi_label:
            best_label, best_score = self.get_best_label(ori_output, self.all_allowed_outputs)
            return best_label
        else:
            # 找多标签分类任务用来拼接的符号
            punctuations = list(set([_ for _ in ori_output if is_punctuation(_)]))

            ori_output_parts = split_punctuation(ori_output)
            fix_output_parts = []
            for part in ori_output_parts:
                best_label, best_score = self.get_best_label(part, self.all_allowed_outputs)
                if best_score > 0.1:
                    fix_output_parts.append(best_label)
            if len(fix_output_parts) == 0:
                fix_output_parts = sample(self.all_allowed_outputs, 1)

            fix_output_parts = list(set(fix_output_parts))
            fix_output = self.split_punctuation.join(fix_output_parts)
            return fix_output

    @staticmethod
    def average_split(ball_num, box_num, size: List[int] = None):
        if box_num == 0:
            raise ValueError('box_num cannot be zero')
        if size is not None:
            assert len(size) == box_num

        if size is None or min(size) > (ball_num // box_num + 1):
            # 如果box_size的最小值大于ball_num // box_num + 1
            base_num = ball_num // box_num
            distribute = [base_num] * box_num
            remainder = ball_num - base_num * box_num
            # 尽量均匀地采样：不重复
            fifo = [idx for idx in range(box_num)]
            shuffle(fifo)
            for idx in range(remainder):
                distribute[fifo[idx]] += 1
        else:
            fifo = []
            for idx, size in enumerate(size):
                fifo.extend([idx] * size)
            shuffle(fifo)
            distribute = [0] * box_num
            for idx in fifo[:box_num]:
                distribute[idx] += 1
        return distribute

    def clean_case(self, prompt: str, cases: str) -> List[str]:
        """
        清洗大模型基于prompt生成的数据，去掉冗余的格式信息，用回车分割case
        TODO: 这个方案里不支持case中包含回车
        :param prompt:
        :param cases:
        :return:
        """
        records = [
            [
                """下列【原始数据】中包含多条为【任务】生成的数据，请过滤掉冗余的格式信息和背景描述，然后输出其中生成的数据（每行一条数据）。\n【任务:】\n{}\n【原始数据:】\n{}\n【清洗后的数据:】\n""",
                [prompt, cases], """第一版"""],
        ]
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        rst = [line for line in rst.split('\n') if len(line) > 0]
        return rst

    @staticmethod
    def pick_dataset(dataset: List[LabeledCase], sign: str, num: int, target_idx: int = LabelIdx) -> list[LabeledCase]:
        """
        基于结构化的标注数据dataset(输出，标签，输入，备注)，从target_idx例里选出和sign标签一样的数据里抽样num个
        TODO 目前只考虑good label
        :param dataset:
        :param sign:
        :param num:
        :param target_idx:
        :return:
        """
        matched_data = []
        for data in dataset:
            if data[target_idx] == sign:
                matched_data.append(data)

        if num is None:
            return matched_data

        # 全随机采样
        chosen_case = sample(matched_data, min(num, len(matched_data)))
        return chosen_case

    def split_dataset(self, dataset: List[LabeledCase], length: int, balance_idx=None) -> Tuple[list[LabeledCase], list[LabeledCase]]:
        # 将数据集切分成两份
        length = min(len(dataset), length)

        tag2cases = defaultdict(list)
        if balance_idx is None:
            tag2cases[''] = dataset
        else:
            for case in dataset:
                tag2cases[case[balance_idx]].append(case)
        dataset_1 = []
        dataset_2 = []
        tags = list(tag2cases.keys())
        tag_size = [len(tag2cases[tag]) for tag in tags]
        tag2num = self.average_split(length, len(tags), size=tag_size)
        for tag, num in zip(tags, tag2num):
            if num == 0:
                continue
            sub_dataset = tag2cases[tag]
            selected_idx = sample(list(range(len(sub_dataset))), num)
            sub_dataset_1 = []
            sub_dataset_2 = []
            for idx, case in enumerate(sub_dataset):
                if idx in selected_idx:
                    sub_dataset_1.append(case)
                else:
                    sub_dataset_2.append(case)
            dataset_1.extend(sub_dataset_1)
            dataset_2.extend(sub_dataset_2)
        return dataset_1, dataset_2

    @staticmethod
    def get_text(case: LabeledCase) -> str:
        if case[InputIdx] == '':
            one_str = case[OutputIdx]
        else:
            one_str = '输入：\n{}\n输出：\n{}\n'.format(case[InputIdx], case[OutputIdx])
        if case[CommentIdx] != '':
            one_str += '备注：\n{}\n'.format(case[CommentIdx])
        return one_str

    def get_texts(self, cases: List[LabeledCase]) -> List[str]:
        """Todo 没使用，待修改以便统一"""
        texts = []
        for case in cases:
            one_str = self.get_text(case)
            texts.append(one_str)
        return texts

    def analysis_case2good(
            self,
            case_new: List[LabeledCase],
            case_good: List[LabeledCase],
            task: str,
            wrong_cases_str: str = '',
    ) -> str:
        """
        分析旧的生成数据和人工标注的优质数据之间的差异，并总结出需要对旧生成数据做什么修改
        :param case_new:
        :param case_good:
        :param task:
        :param wrong_cases_str:
        :return:
        """
        case_new = self.get_example_str(case_new, add_header=False, use_all=True)
        case_good = self.get_example_str(case_good, add_header=False, use_all=True)
        if len(case_new) == 0:
            raise ValueError('cases is empty')
        if len(case_good) > 0:
            if self.task_kind == Generation:
                records = [
                    [
                        """请总结出【生成数据】和【优质数据】的差别，包括语言风格、用词风格、情绪特点、内容重心、其他角度等，并总结出需要对【生成数据】做什么【修改】才能使其更接近【优质数据】。【历史生成数据：】\n{}\n【优质数据：】\n{}\n【修改：】\n""",
                        [case_new, case_good],
                        """1、很容易受列出的细节点的影响，导致分析不了它们之外的项的特点和强行分析每个项的特点，2、不容易拆解出哪些是需要做的修改"""],
                    [
                        """请观察【生成数据】和【优质数据】，总结出【优质数据的特点】。【历史生成数据：】\n{}\n【优质数据：】\n{}\n【优质数据的特点：】\n""",
                        [case_new, case_good], """不做对比分析，只总结优质数据的特点，以及不限度分析角度"""],
                    [
                        """基于【数据生成任务:】{}\n请对比观察【当前数据】和【优质数据】，总结出【优质数据的特点】。\n【当前数据：】\n{}\n【优质数据：】\n{}\n【优质数据的特点：】\n""",
                        [task, case_new, case_good], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind == Classification:
                records = [
                    [
                        """基于分类任务的【任务描述:】{}\n请对比观察【当前分类结果】和【标准答案】，总结出需要补充的【分类判断标准】。\n【当前分类结果：】\n{}\n【标准答案：】\n{}\n$错误数据$总结出的【分类判断标准：】\n""",
                        [task, case_new, case_good], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
                if wrong_cases_str is not None and len(wrong_cases_str) > 0:
                    template = template.replace('$错误数据$', '【错误分析：】\n' + wrong_cases_str + '\n')
                else:
                    template = template.replace('$错误数据$', '')
            else:
                raise UndefinedTask
        else:
            if self.task_kind == Generation:
                records = [
                    [
                        """基于【数据生成任务:】{}\n请观察【当前数据】，总结出【当前数据的待改进点】。\n【当前数据：】\n{}\n【当前数据的待改进点：】\n""",
                        [task, case_new], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind == Classification:
                records = [
                    [
                        """基于分类任务的【任务描述:】{}\n请观察【当前分类结果】，总结出需要补充的【分类判断标准】。\n【当前分类结果：】\n{}\n需要补充的【分类判断标准：】\n""",
                        [task, case_new], """提供task做背景知识"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            else:
                raise UndefinedTask
        rst = self.call_llm(template)
        return rst

    def clean_prompt(self, prompt):
        """清洗prompt里面不合适的内容"""
        if self.task_kind == Generation:
            records = [
                [
                    """请对【原prompt】进行修改，并输出【修正后的prompt】。prompt里不应该出现“已有历史数据”、“相比优质数据”、“原prompt”等类似的表达，因为一个prompt应该是独立且完整的不依赖任何其他任务的结果。在保持【原prompt】的信息不遗漏的情况下整理其格式，不要遗漏原prompt里任何信息，按任务背景、数据要求、示例分析、输出格式的结构进行组织。直接输出修正后的prompt，不要输出修改过程。\n【原prompt：】\n{}\n【修正后的prompt：】\n""",
                    [prompt], """第一版"""],
            ]
        elif self.task_kind == Classification:
            records = [
                [
                    """请对【原prompt】进行修改，并输出【修正后的prompt】。prompt里不应该出现“已有历史数据”、“相比标准答案”、“原prompt”等类似的表达，因为一个prompt应该是独立且完整的不依赖任何其他任务的结果。在保持【原prompt】的信息不遗漏的情况下整理其格式，不要遗漏原prompt里任何信息，按任务的背景、分类标准、限制条件、示例数据、输出格式的结构进行组织。直接输出修正后的prompt，不要输出修改过程。\n【原prompt：】\n{}\n【修正后的prompt：】\n""",
                    [prompt], """第一版"""],
            ]
        else:
            raise UndefinedTask
        template = records[-1][0].format(*records[-1][1])
        rst = self.call_llm(template)
        return rst

    def update_prompt(
            self,
            prompt: str,
            propose: str,
            case_old: List[LabeledCase],
            case_good: List[LabeledCase],
            wrong_cases_str: str = None,
    ) -> str:
        """
        基于propose优化prompt
        :param prompt:
        :param propose:
        :param case_old:
        :param case_good:
        :param wrong_cases_str:
        :return:

        TODO 生成结果里的badcase，对于修改建议需要再清洗一下
        改写后的prompt：xxx
        背景：已生成一些关于赞美、祝福、励志、正能量主题的【历史数据】，但与【优质数据】相比存在不足。
        示例：【优质数据】中的“积极向上永不言弃”，简单直接地表达了励志主题，这就是我们想要达到的风格。
        """
        case_old = self.get_example_str(case_old, add_header=False, use_all=True)
        case_good = self.get_example_str(case_good, add_header=False, use_all=True)

        if len(case_good) > 0:
            if self.task_kind == Generation:
                records = [
                    [
                        """请参考【修改意见】，对【prompt】进行改写。【改写后的prompt】需要基于【修改意见】进行修改，并精练地说明生成任务的背景、生成目标、限制条件、输出格式、示例数据。\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [propose, prompt], """第一版"""],
                    [
                        """【历史数据】是由【prompt】生成，和【优质数据】对比起来还有一些不足。为了生成和【优质数据】更接近的数据，需要参考【历史数据】、【优质数据】和【修改意见】对【prompt】进行改写，并输出【改写后的prompt】，注意改写后的prompt不应该包含文本“历史数据”，“优质数据”，注意改写后的prompt是一个独立且完整的任务描述。改写后的prompt应精练地说明生成任务的背景、生成目标、限制条件、示例数据、输出格式。。\n【历史数据:】\n{}\n【优质数据:】\n{}\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [case_old, case_good, propose, prompt], """第一版"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind == Classification:
                records = [
                    [
                        """【历史分类结果：】是由用分类任务的【原prompt】生成的，和【标准答案】对比起来还有一些不足。为了让分类结果更加精准，需要参考【分类结果】、【标准答案】和【修改意见】对【原prompt】进行优化，并输出【优化后的prompt】，注意优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。优化后的prompt应说明分类任务的背景、分类标准、限制条件、示例数据、输出格式。优化后的prompt应尽量包含修改意见里的总结出的要点，只要原prompt里面没有对子任务分别做要求，那么就应尽量去掉修改意见里总结出的要点的适用范围限制，使这些要点能应用到增个任务的生成中。\n【历史分类结果:】\n{}\n【标准答案:】\n{}\n$错误数据$【修改意见:】\n{}\n【prompt:】\n{}\n【优化后的prompt:】\n""",
                        [case_old, case_good, propose, prompt], """第一版"""],
                ]
                template = records[-1][0].format(*records[-1][1])
                if wrong_cases_str is not None and len(wrong_cases_str) > 0:
                    template = template.replace('$错误数据$', '【错误分析：】\n' + wrong_cases_str + '\n')
                else:
                    template = template.replace('$错误数据$', '')
            else:
                raise UndefinedTask
        else:
            if self.task_kind == Generation:
                records = [
                    [
                        """【历史数据】是由【prompt】生成。为了生成质量更好的数据，需要参考【历史数据】和【修改意见】对【prompt】进行改写，并输出【改写后的prompt】。【改写后的prompt】应精练地说明生成任务的背景、生成目标、限制条件、示例数据、输出格式。\n【历史数据:】\n{}\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [case_old, propose, prompt], """第一版"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            elif self.task_kind == Classification:
                records = [
                    [
                        """【当前分类结果】是用分类任务的【prompt】生成的。为了生成质量更好的数据，需要参考【当前分类结果】和【修改意见】对【prompt】进行优化，并输出【优化后的prompt】。【优化后的prompt不应该包含文本“历史分类结果”，“标准答案”等字样，优化后的prompt依然是一个独立且完整的任务描述。【优化后的prompt】应说明分类任务的背景、分类标准、限制条件、示例数据、输出格式。\n【历史数据:】\n{}\n【修改意见:】\n{}\n【prompt:】\n{}\n【改写后的prompt:】\n""",
                        [case_old, propose, prompt], """第一版"""],
                ]
                template = records[-1][0].format(*records[-1][1])
            else:
                raise UndefinedTask
        rst = self.call_llm(template)
        rst = self.clean_prompt(rst)
        return rst

    def verify(self, case_old: List[str], case_new: List[str], case_good: List[str], task: str) -> Tuple[str, int]:
        """

        :param case_old:
        :param case_new:
        :param case_good:
        :param task:
        :return:
        """
        case_old = sample(case_old, min(len(case_old), self.window_size))
        case_new = sample(case_new, min(len(case_new), self.window_size))
        if len(case_good) > 0:
            case_good = sample(case_good, min(len(case_good), self.window_size))
            records = [
                [
                    """请判断【数据集1】和【数据集2】中哪个数据集和【优质数据集】里的数据风格更相似，给出【分析结论】回答“数据集1更相似”或“数据集2更相似”。\n【数据集1:】\n{}\n【数据集2:】\n{}\n【优质数据集:】\n{}\n【分析结论：】\n""",
                    [case_old, case_new, case_good], """第一版"""],
                [
                    """对于数据生成任务：\n{}\n请判断生成的【数据集1】和【数据集2】中哪个数据集和【优质数据集】里的数据风格更相似，给出【分析结论】回答“数据集1更相似”或“数据集2更相似”。\n【数据集1:】\n{}\n【数据集2:】\n{}\n【优质数据集:】\n{}\n【分析结论：】\n""",
                    [task, case_old, case_new, case_good], """第一版"""],
            ]
            template = records[-1][0].format(*records[-1][1])
        else:
            records = [
                [
                    """对于数据【生成任务】：\n{}\n请判断生成的【数据集1】和【数据集2】中哪个数据集更符合【生成任务】的要求。给出【分析结论】回答“数据集1更相似”或“数据集2更相似”。\n【数据集1:】\n{}\n【数据集2:】\n{}\n【分析结论：】\n""",
                    [task, case_old, case_new], """第一版"""],
            ]
            template = records[-1][0].format(*records[-1][1])

        rst = self.call_llm(template)
        rst = rst.replace(' ', '').replace('一', '1').replace('二', '2')
        if '数据集1更相似' in rst:
            rst_signal = 1
        elif '数据集2更相似' in rst:
            rst_signal = 2
        else:
            rst_signal = 0
        return rst, rst_signal

    def get_subtasks(self):
        self.subtasks = self.task2subtask(self.task)

    def get_subdatasets(self):  # TODO 分类容易出错，考虑多做基础之后取交集
        def intersection(dataset1, dataset2):
            rst = []
            str2case = {}
            for case in dataset1 + dataset2:
                str2case[case[0]] = case
            text1 = [case[0] for case in dataset1]
            text2 = [case[0] for case in dataset2]

            text_inter = list(set(text1) & set(text2))
            text_chosen = []
            if len(text_inter) == 0:
                if len(text1) > 0 or len(text2) > 0:
                    text_chosen = list(set(text1) | set(text2))
            else:
                text_chosen = text_inter

            for text in text_chosen:
                rst.append(str2case[text])
            return rst

        subdatasets = []
        for subtask in self.subtasks:
            # 计算2次子集，提高可性度。如果无法获取到有效的子集则用全量数据。
            rst_1 = self.get_subdataset(subtask)
            rst_2 = self.get_subdataset(subtask)
            rst_intersection = intersection(rst_1, rst_2)
            if len(rst_intersection) > 0:
                subdatasets.append(rst_intersection)
            else:
                subdatasets.append(subtask)
        self.subdatasets = subdatasets
        assert len(self.subtasks) == len(self.subdatasets)

    def verify_data(self, prompt: str, size: int, inputs: List[str]) -> None:
        # 基于prompt生成数据
        if prompt in self.prompt2case:
            return
        cases = self.get_cases(prompt, size, inputs, do_variety=False)
       
        self.record.note(('prompt', prompt))
        if len(cases) > 0:
            self.prompt2case[prompt] = cases
            self.record.note(('cases generated', cases))
        else:
            self.record.note(('cases generated Fail', ''))

    def gradient_and_update(self, prompt: str, dataset: List[LabeledCase], task: str):
        # 计算梯度并更新prompt
        if prompt not in self.prompt2case:
            return []

        if self.task_kind == Generation:
            # 对于生成任务，每次求梯度时都随机采样一批数据作为验证集
            self.record.note(('prompt', prompt))
            # 采样好的数据
            validate = self.pick_dataset(dataset, self.label_good, self.window_size)
            # 采样差的数据
            pass
        elif self.task_kind == Classification:
            # 对于分类任务，总是使用同一个验证集
            validate = self.validate_cases
        else:
            raise UndefinedTask

        new_prompts = []
        for _ in range(self.derive_time):
            # 分析差异
            if self.task_kind == Classification:
                right_cases, wrong_cases, wrong_outputs = self.check_response(self.prompt2case[prompt], validate)
                self.prompt2wrong_cases_str[prompt] = self.get_wrong_cases_str(wrong_cases, wrong_outputs)
            wrong_cases_str = ''
            if prompt in self.prompt2wrong_cases_str:
                wrong_cases_str = self.prompt2wrong_cases_str[prompt]

            # 基于task做分析，以免受到错误迭代后的prompt的干扰
            propose = self.analysis_case2good(self.prompt2case[prompt], validate, task, wrong_cases_str=wrong_cases_str)
            self.prompt2gradient[prompt].append(propose)

            # 更新prompt
            prompt_updated = self.update_prompt(prompt, propose, self.prompt2case[prompt], validate, wrong_cases_str=wrong_cases_str)
            new_prompts.append(prompt_updated)
            self.record.note(('propose', propose))
            self.record.note(('prompt_updated', prompt_updated))
        return new_prompts

    def check_response(self, respond_cases, validate_cases):
        right_cases, wrong_cases, wrong_outputs = [], [], []
        for respond_case, validate_case in zip(respond_cases, validate_cases):
            assert respond_case[InputIdx] == validate_case[InputIdx]
            respond_reformat = self.get_reformat_text(respond_case[OutputIdx])
            validate_reformat = self.get_reformat_text(validate_case[OutputIdx])
            if respond_reformat == validate_reformat:
                right_cases.append(validate_case)
            else:
                wrong_cases.append(validate_case)
                wrong_outputs.append(respond_case[OutputIdx])
        return right_cases, wrong_cases, wrong_outputs

    @staticmethod
    def get_wrong_cases_str(wrong_cases, wrong_outputs):
        rst = []
        for case, output in zip(wrong_cases, wrong_outputs):
            one_str = '对于输入：\n{}\n正确输出是：\n{}\n但却给出了以下错误输出：\n{}\n'.format(case[InputIdx], case[OutputIdx], output)
            if case[CommentIdx] != '':
                one_str += '备注：\n{}\n'.format(case[CommentIdx])
            rst.append(one_str)
        return '\n'.join(rst)

    def get_rank_score(self, prompts: List[str], dataset: List[LabeledCase], task: str):
        checked_prompts = []
        for prompt in prompts:
            if prompt in self.prompt2case:
                checked_prompts.append(prompt)

        prompt2score = defaultdict(float)
        if self.task_kind == Generation:
            # 计算相对分数
            for prompt_1 in tqdm(checked_prompts, desc='get rank score'):
                for prompt_2 in checked_prompts:
                    if prompt_1 == prompt_2:
                        good = self.get_texts(self.pick_dataset(dataset, self.label_good, self.window_size))
                        self.record.note(('good', good))
                        verify_rst, verify_signal = self.verify(self.prompt2case[prompt_1], self.prompt2case[prompt_2],
                                                                good, task)
                        self.record.note(('verify_rst', verify_rst))
                        self.record.note(('verify_signal', verify_signal))
                        if verify_signal == 1:
                            prompt2score[prompt_1] += 1
                        elif verify_signal == 2:
                            prompt2score[prompt_2] += 1
                        else:
                            pass
        elif self.task_kind == Classification:
            # 计算绝对分数
            for prompt in tqdm(checked_prompts, desc='get rank score'):
                prompt2score[prompt] = self.get_prompt_precision(prompt)
        else:
            raise ValueError("unexpected task", self.task_kind)
        prompt_score = [[k, v] for k, v in prompt2score.items()]
        prompt_score.sort(key=lambda x: x[1], reverse=True)
        return prompt_score

    def get_prompt_precision(self, prompt, is_lenient=False) -> float:
        """is_lenient == True 时为宽松的统计模式，在分类结果不完全正确的情况下会酌情给分，以便做更精准的排序"""
        if prompt in self.prompt2precision:
            return self.prompt2precision[prompt]
        cand_cases = self.prompt2case[prompt]
        return self.get_precision(cand_cases, self.validate_cases, is_lenient=is_lenient)

    @staticmethod
    def get_reformat_text(text):
        # 假设输出里的多分类的结果用标点符合分隔，且不重复
        return ''.join(sorted(split_punctuation(text)))

    def get_precision(self, cases1: List[LabeledCase], cases2: List[LabeledCase], is_lenient: bool = False) -> float:
        assert len(cases1) == len(cases2)
        right_count = 0
        for case1, case2 in zip(cases1, cases2):
            output1 = case1[OutputIdx]
            output2 = case2[OutputIdx]
            output1_reformat = self.get_reformat_text(output1)
            output2_reformat = self.get_reformat_text(output2)
            if output1_reformat == output2_reformat:
                right_count += 1
            elif is_lenient:
                right_count += ngram_sim(output1_reformat, output2_reformat)

        precision = right_count / len(cases1)
        return precision

    def beam_search(self, task: str, prompts: List[str], dataset: List[LabeledCase], iteration: int) -> List[str]:
        """
        beam_search 循环
        :param task: 任务表述
        :param prompts: beam_size个候选prompt
        :param dataset: 标注数据
        :param iteration: 剩余的迭代轮次
        :return:
        """
        if iteration == 0:
            for prompt in prompts:
                self.record.note(('final_prompts', prompt))
                if prompt in self.prompt2case:
                    self.record.note(('final_case', self.prompt2case[prompt]))
            return prompts

        explored_prompt = []  # 梯度更新后的prompt
        if self.task_kind == Generation:
            input2dataset = self.aggregate_dataset(dataset)
            inputs = list(input2dataset.keys())
            window_size = self.window_size
        elif self.task_kind == Classification:
            inputs = self.validate_inputs
            window_size = len(self.validate_inputs)
        else:
            raise ValueError("unexpected task", self.task_kind)
        for prompt in prompts:
            self.verify_data(prompt, window_size, inputs)  # 为prompt生成数据
            new_prompts = self.gradient_and_update(prompt, dataset, task)  # 得到新的prompt
            explored_prompt.extend(new_prompts)
        for prompt in explored_prompt:
            self.verify_data(prompt, window_size, inputs)
        prompt_score = self.get_rank_score(prompts + explored_prompt, dataset, task)
        prompt_selected = [prompt for prompt, score in prompt_score[:self.beam_size]]
        self.record.note(('explored_prompt', explored_prompt))
        for prompt, score in prompt_score:
            self.record.note(('In Rank Prompt', prompt))
            self.record.note(('In Rank Score', score))
        self.record.note(('prompt_selected', prompt_selected))
        return self.beam_search(task, prompt_selected, dataset, iteration - 1)
