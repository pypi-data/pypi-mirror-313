# -*- coding: UTF-8 -*-
from transformers import AutoModelForImageClassification, TrainingArguments, Trainer
from datasets import load_dataset
dataset = load_dataset("imagefolder", data_files="/mnt/bn/mlxlabzw/xiangyuejia/porn/baseline_porn_1027.zip")
labels = dataset["train"].features["label"].names
splits = dataset["train"].train_test_split(test_size=0.1)
p = 1