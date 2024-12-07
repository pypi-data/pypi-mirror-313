# encoding:utf-8
"""
Author: feizhihui
Date: 2023-09-14
"""
import nltk
import pandas as pd
# bleu会强制统计ngram1到ngram4的频次， 如果为0则可能溢出，需要添加平滑参数  smoothing_function=smooth.method2
smooth = nltk.translate.bleu_score.SmoothingFunction()
def demo_func():
    # 假设你有参考翻译和候选翻译
    references = [['this', 'is', 'a', 'test']]
    candidate = ['this', 'is', 'a', 'test']
    # 计算BLEU分数
    bleu_score = nltk.translate.bleu_score.sentence_bleu(references, candidate)
    print(bleu_score)
def self_bleu(sentences):
    total_score = 0
    for i in range(len(sentences)):
        sent = list(sentences[i])
        references = sentences[0:i] + sentences[i+1:]
        # references = [[ref] for ref in references]
        bleu_score = nltk.translate.bleu_score.sentence_bleu(references, sent, smoothing_function=smooth.method2)
        total_score += bleu_score
    return total_score/len(sentences)
def get_score(fn):
    sentences = []
    policy_rich_d = {}
    policy_set = set()
    prev_label = None
    with open(fn,"r") as file:
        for line in file:
            line = line.strip().lower()
            cols = line.strip().split("\t")
            if ("label" in line and "output" in line) or ("prompt" in line and "output" in line):
                continue
            label = cols[0] # label 第0列
            text = cols[1] # output 第1列
            if prev_label is None:
                print(label)
            if label==prev_label or prev_label is None:
                sentences.append(list(text))
            else:
                # 如果是新的标签
                print("计算bleu:",len(sentences))
                avg_score = 1 - self_bleu(sentences)
                policy_rich_d[label] = avg_score
                # 考虑重新计算
                sentences = [list(text)]
                policy_set.add(label)
                print(label)
            # next line
            prev_label = label
    print(policy_rich_d)
    richness_score = sum(list(policy_rich_d.values())) / len(policy_rich_d)
    return richness_score
if __name__ == "__main__":
    # demo
    # demo_func()
    from aitool import load_excel, dump_lines
    raw_fn = './chatglm2-bloomz效果标注.xlsx'
    df = load_excel(raw_fn, to_list=True, sheet_name=3)
    text = []
    for line in df:
        p = line[0].replace('\n', '').replace('\t', '')
        o = line[2].replace('\n', '').replace('\t', '')
        text.append(p+'\t'+o)
    fn = "./result_bloom.tsv"
    dump_lines(text, fn)
    # 开始计算
    """
    # 文件格式： policy\toutput\n
    # 计算方法： 按照相同policy内部计算bleu得分，然后多个policy的self-bleu得分取平均值，最后计算多样性得分
    """
    score = get_score(fn)
    print(score)