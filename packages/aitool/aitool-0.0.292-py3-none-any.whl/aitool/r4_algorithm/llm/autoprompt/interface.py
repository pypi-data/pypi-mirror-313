# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk


class PlaceholderText(tk.Text):
    def __init__(self, master=None, placeholder="请输入", placeholder_color="grey", text_color="black", **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.text_color = text_color

        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)

        self._display_placeholder()

    def _display_placeholder(self):
        """Display the placeholder text."""
        self.insert("1.0", self.placeholder)
        self.config(fg=self.placeholder_color)

    def _focus_in(self, event=None):
        """Handle focus in event."""
        if self._is_placeholder():
            self.delete("1.0", tk.END)
            self.config(fg=self.text_color)

    def set_text(self, text):
        self.delete("1.0", tk.END)
        self.config(fg=self.text_color)
        self.insert("1.0", text)

    def _focus_out(self, event):
        """Handle focus out event."""
        if not self.get("1.0", tk.END).strip():
            self._display_placeholder()

    def _is_placeholder(self):
        """Check if the current text is the placeholder."""
        return self.get("1.0", tk.END).strip() == self.placeholder

    def get_text(self):
        """Get the actual user input text, excluding placeholder."""
        if self._is_placeholder():
            return ""
        else:
            return self.get("1.0", tk.END).strip()


class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="请输入", placeholder_color='grey', text_color='black', *args,
                 **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.text_color = text_color

        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _clear_placeholder(self, event=None):
        if self['fg'] == self.placeholder_color:
            self.delete(0, tk.END)
            self.config(fg=self.text_color)

    def clear_placeholder(self):
        self._clear_placeholder()

    def _add_placeholder(self, event=None):
        if not self.get():
            self.config(fg=self.placeholder_color)
            self.insert(0, self.placeholder)

    def get(self):
        current_text = super().get()
        if current_text == self.placeholder and self['fg'] == self.placeholder_color:
            return ""
        else:
            return current_text


class LabeledCaseEntry(tk.Frame):
    def __init__(self, parent, has_check=False, auto_prompt_app=None):
        super().__init__(parent)
        self.has_check = has_check
        self.auto_prompt_app = auto_prompt_app
        self.input_label = tk.Label(self, text="输入:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5)
        self.input_entry = PlaceholderEntry(self, width=15, placeholder="无")
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)
        self.output_label = tk.Label(self, text="输出:")
        self.output_label.grid(row=0, column=2, padx=5, pady=5)
        self.output_entry = PlaceholderEntry(self, width=40, placeholder="无")
        self.output_entry.grid(row=0, column=3, padx=5, pady=5)
        self.label_label = tk.Label(self, text="标注:")
        self.label_label.grid(row=0, column=4, padx=5, pady=5)
        self.label_entry = PlaceholderEntry(self, width=10, placeholder="无")
        self.label_entry.grid(row=0, column=5, padx=5, pady=5)
        self.remark_label = tk.Label(self, text="备注:")
        self.remark_label.grid(row=0, column=6, padx=5, pady=5)
        self.remark_entry = PlaceholderEntry(self, width=10, placeholder="无")
        self.remark_entry.grid(row=0, column=7, padx=5, pady=5)
        if self.has_check:
            self.labeled_var = tk.IntVar()
            self.labeled_check = tk.Checkbutton(self, text="已标注", variable=self.labeled_var, command=self.move)
            self.labeled_check.grid(row=0, column=8, padx=5, pady=5)

    def move(self):
        case_input = '' if self.input_entry.get() == '空' else self.input_entry.get()
        case_output = '' if self.output_entry.get() == '空' else self.output_entry.get()
        case_label = '' if self.label_entry.get() == '空' else self.label_entry.get()
        case_comment = '' if self.remark_entry.get() == '空' else self.remark_entry.get()
        labeled_case = (case_output, case_label, case_input, case_comment)
        self.auto_prompt_app.add_labeled_case(labeled_case)

    def set_case(self, labeled_case):
        case_output, case_label, case_input, case_comment = labeled_case
        if case_input:
            self.input_entry.clear_placeholder()
            self.input_entry.insert(0, case_input)
        if case_output:
            self.output_entry.clear_placeholder()
            self.output_entry.insert(0, case_output)
        if case_label:
            self.label_entry.clear_placeholder()
            self.label_entry.insert(0, case_label)
        if case_comment:
            self.remark_entry.clear_placeholder()
            self.remark_entry.insert(0, case_comment)


class AutoPromptApp:
    def __init__(self, labeled_cases, generated_cases, output_prompt, inputs, time_estimate):
        self.root = tk.Tk()
        self.root.title("AutoPrompt物料生成方案")
        self.labeled_cases = labeled_cases
        self.generated_cases = generated_cases
        self.output_prompt = output_prompt
        self.inputs = inputs
        self.time_estimate = time_estimate
        self.labeled_cases_shown = []
        self.generated_cases_shown = []

        self.data_frame_1 = tk.Frame(self.root)
        self.data_frame_1.pack(padx=15, pady=5, fill='x')
        self.task_label_1 = tk.Label(self.data_frame_1, text="任务描述:")
        self.task_label_1.pack(side=tk.LEFT)
        self.task_entry_1 = PlaceholderText(self.data_frame_1, width=150, height=5, placeholder='请输入任务描述，例如：请围绕给定的主题输出一句冷笑话。')
        self.task_entry_1.pack(side=tk.LEFT)
        # self.task_entry_1.insert('1.0', "请输入任务描述")
        self.scrollbar_1 = tk.Scrollbar(self.data_frame_1, command=self.task_entry_1.yview)
        self.scrollbar_1.pack(side='right', fill='y')
        self.task_entry_1.config(yscrollcommand=self.scrollbar_1.set)

        self.data_frame_2 = tk.Frame(self.root)
        self.data_frame_2.pack(padx=15, pady=5, fill='x')
        self.task_label_2 = tk.Label(self.data_frame_2, text="生成数量:")
        self.task_label_2.pack(side=tk.LEFT)
        self.task_entry_2 = tk.Entry(self.data_frame_2, width=20)
        self.task_entry_2.pack(side=tk.LEFT)
        self.task_entry_2.insert(0, "50")

        self.data_frame_3 = tk.Frame(self.root)
        self.data_frame_3.pack(padx=15, pady=5, fill='x')
        self.task_label_3 = tk.Label(self.data_frame_3, text="额外输入:")
        self.task_label_3.pack(side=tk.LEFT)
        self.task_entry_3 = PlaceholderText(self.data_frame_3, width=150, height=5, placeholder='（单次生成的输入，每行为一个输出，选填，可空）例如：\n以吃饭为主题\n以蜗牛为主题')
        self.task_entry_3.pack(side=tk.LEFT)
        # self.task_entry_3.insert('1.0', "（选填）case级输入，可空")
        self.scrollbar_3 = tk.Scrollbar(self.data_frame_3, command=self.task_entry_3.yview)
        self.scrollbar_3.pack(side='right', fill='y')
        self.task_entry_3.config(yscrollcommand=self.scrollbar_3.set)

        # Labeled Data Section
        self.data_frame_4 = tk.Frame(self.root)
        self.data_frame_4.pack(padx=5, pady=5, fill='x')
        self.data_frame_5 = tk.Frame(self.data_frame_4)
        self.data_frame_5.pack(side=tk.LEFT)
        self.task_label_5 = tk.Label(self.data_frame_5, text="标注数据:")
        self.task_label_5.pack(padx=0, pady=0)
        self.add_button_5 = tk.Button(self.data_frame_5, text="添加一条", command=self.add_labeled_case)
        self.add_button_5.pack(padx=0, pady=0)
        self.add_button_5 = tk.Button(self.data_frame_5, text="批量导入", command=self.add_labeled_cases)
        self.add_button_5.pack(padx=0, pady=0)
        self.canvas_6 = tk.Canvas(self.data_frame_4, height=130)  # 设置Frame的固定高度
        self.scrollbar_6 = ttk.Scrollbar(self.data_frame_4, orient="vertical", command=self.canvas_6.yview)
        self.scrollable_frame_6 = ttk.Frame(self.canvas_6)
        self.scrollable_frame_6.bind("<Configure>", lambda e: self.canvas_6.configure(scrollregion=self.canvas_6.bbox("all")))
        self.canvas_6.create_window((0, 0), window=self.scrollable_frame_6, anchor="nw")
        self.canvas_6.configure(yscrollcommand=self.scrollbar_6.set)
        self.canvas_6.pack(side=tk.LEFT, expand=True, fill='both')
        self.scrollbar_6.pack(side="right", fill="y")

        # Generate Button
        self.data_frame_7 = tk.Frame(self.root)
        self.data_frame_7.pack(padx=5, pady=5, fill='x')
        self.generate_button_7 = tk.Button(self.data_frame_7, text="生成数据", command=self.start_running)
        self.generate_button_7.pack(padx=5, pady=5)

        # output prompt
        self.data_frame_11 = tk.Frame(self.root)
        self.data_frame_11.pack(padx=20, pady=5, fill='x')
        self.task_label_11 = tk.Label(self.data_frame_11, text="Prompt:")
        self.task_label_11.pack(side=tk.LEFT)
        self.task_entry_11 = PlaceholderText(self.data_frame_11, width=150, height=12, placeholder='本方案包括2个模块：\n1、自动优化prompt：模拟人工调优prompt的过程，得到一个较好的prompt。\n2、批量生成物料：LLM批量调用模块 + 多样性增强模块 + 低质数据清洗/改写模块”。')
        self.task_entry_11.pack(side=tk.LEFT)
        self.scrollbar_11 = tk.Scrollbar(self.data_frame_11, command=self.task_entry_11.yview)
        self.scrollbar_11.pack(side='right', fill='y')
        self.task_entry_11.config(yscrollcommand=self.scrollbar_11.set)

        # Labeled Data Section
        self.data_frame_8 = tk.Frame(self.root)
        self.data_frame_8.pack(padx=5, pady=5, fill='x')
        self.data_frame_9 = tk.Frame(self.data_frame_8)
        self.data_frame_9.pack(side=tk.LEFT)
        self.task_label_9 = tk.Label(self.data_frame_9, text="生成结果:")
        self.task_label_9.pack(padx=15, pady=0)
        self.add_button_9 = tk.Button(self.data_frame_9, text="批量导出", command=self.add_labeled_cases)
        self.add_button_9.pack(padx=0, pady=0)
        self.canvas_10 = tk.Canvas(self.data_frame_8, height=130)  # 设置Frame的固定高度
        self.scrollbar_10 = ttk.Scrollbar(self.data_frame_8, orient="vertical", command=self.canvas_10.yview)
        self.scrollable_frame_10 = ttk.Frame(self.canvas_10)
        self.scrollable_frame_10.bind("<Configure>", lambda e: self.canvas_10.configure(scrollregion=self.canvas_10.bbox("all")))
        self.canvas_10.create_window((0, 0), window=self.scrollable_frame_10, anchor="nw")
        self.canvas_10.configure(yscrollcommand=self.scrollbar_10.set)
        self.canvas_10.pack(side=tk.LEFT, expand=True, fill='both')
        self.scrollbar_10.pack(side="right", fill="y")

    def run(self):
        self.root.mainloop()

    def add_labeled_case(self, labeled_case=None):
        labeled_case_entry = LabeledCaseEntry(self.scrollable_frame_6)
        labeled_case_entry.pack(fill=tk.X)
        if labeled_case is not None:
            labeled_case_entry.set_case(labeled_case)
        self.labeled_cases_shown.append(labeled_case_entry)

    def add_labeled_cases(self):
        for case in self.labeled_cases:
            self.add_labeled_case(case)

    def add_generated_case(self, labeled_case=None):
        labeled_case_entry = LabeledCaseEntry(self.scrollable_frame_10, has_check=True, auto_prompt_app=self)
        labeled_case_entry.pack(fill=tk.X)
        if labeled_case is not None:
            labeled_case_entry.set_case(labeled_case)
        self.labeled_cases_shown.append(labeled_case_entry)

    def set_output_prompt(self):
        self.task_entry_11.set_text(self.output_prompt)

    def add_generated_cases(self):
        for case in self.generated_cases:
            self.add_generated_case(case)

    def start_running(self):
        # TODO 目前还没有实际关联算法模块
        # 创建和显示模态窗口
        modal_window = tk.Toplevel(self.root)
        modal_window.title("运行中...")

        # 窗口居中
        window_width = 300
        window_height = 100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        modal_window.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")
        # 提示文本
        label = tk.Label(modal_window, text="请等待，预计{}分钟".format(self.time_estimate))
        label.pack(pady=10)
        # 进度条
        progress = ttk.Progressbar(modal_window, mode='determinate', length=200)
        progress.pack(pady=10)

        duration = 1  # 秒
        interval = 100  # 更新间隔100毫秒
        steps = duration * 1000 // interval  # 分成多少步
        progress_step = 100 / steps

        def update_progress(value):
            if value < 100:
                value += progress_step
                progress['value'] = value
                self.root.after(interval, update_progress, value)
            else:
                modal_window.destroy()
                self.add_generated_cases()
                self.set_output_prompt()

        update_progress(0)


if __name__ == "__main__":
    manual_task = ''
    labeled_cases = [
    ]
    output_prompt = """"""
    generated_cases = [
    ]
    app = AutoPromptApp(labeled_cases, generated_cases, output_prompt)
    app.run()
