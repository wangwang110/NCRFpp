# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import re
from tqdm import tqdm

"""
序列标注的结果与原来的标注做对比

从句造成的嵌套不知道怎么处理

"""

path = "./data/tets.out"
path_1 = "./test_see_tag.txt"
path_out = "./compare_error.txt"
path_out_1 = "./compare_error_out.txt"

name2ids = {u"主语": "SUB", u"谓语": "VOB", u"宾语": "DO", u"间接宾语": "IO", u"介词宾语": "PO",
            u"表语": "ATTR", u"状语": "ADVMOD",
            u"补足语": "OC", u"定语": "AMOD",
            u"插入语": "INTJ", u"同位语": "APPOS", "强调句式": "EMP"}

tag2names = {value: key for key, value in name2ids.items()}

with open(path, "r", encoding="utf-8") as f, open(path_1, "r", encoding="utf-8") as f1, \
        open(path_out, "w", encoding="utf-8") as f2, open(path_out_1, "w", encoding="utf-8") as f3:
    i = 0
    tag = 0
    all_texts = []
    tmp_texts = []
    for line in tqdm(f.readlines()):
        line = line.strip()
        if line != "":
            tmp_texts.append(line.strip())
            tag = 1
        if line == "" and tag == 1:
            i += 1
            all_texts.append(tmp_texts)
            tmp_texts = []
            tag = 0
    print(i)

    # decode model output
    all_predicts = []
    for texts in all_texts:
        tmp_decode_texts = []
        tmp_list = [text.strip().split(" ") for text in texts[1:]]
        words = [item[0] for item in tmp_list]
        tmp_decode_texts.append(" ".join(words))

        last_tag = ""
        start = 0
        end_tag = 0  # 记录实体位置的结束

        # 判断实体结束的条件：标签变了，并且是由BI变到O
        num = len(words)
        for t in range(num):
            item = tmp_list[t]
            compound_tags = item[1].split("-")
            if compound_tags[-1] != last_tag and last_tag != "" and end_tag == 1:
                tmp_decode_texts.append([" ".join(words[start:t]), str(start), str(t), tag2names[last_tag]])
                end_tag = 0
                last_tag = compound_tags[-1]

            if compound_tags[0] == "B":
                start = t
                end_tag = 1
                last_tag = compound_tags[-1]
            elif compound_tags[0] == "I":
                last_tag = compound_tags[-1]
            elif compound_tags[0] == "O":
                last_tag = compound_tags[-1]
                continue

        all_predicts.append(tmp_decode_texts)

    # 以下是标注语料
    j = 0
    tag_model = 0
    all_texts_model = []
    tmp_texts_model = []
    for line in tqdm(f1.readlines()):
        line = line.strip()
        if line != "":
            tmp_texts_model.append(line.strip())
            tag_model = 1
        if line == "" and tag_model == 1:
            j += 1
            all_texts_model.append(tmp_texts_model)
            tmp_texts_model = []
            tag_model = 0
    print(j)

    all_golds = []
    for texts in all_texts_model:
        tmp_decode_texts = []
        tmp_decode_texts.append(texts[0].strip())
        tmp_decode_texts.extend([text.strip().split("\t") for text in texts[1:]])
        all_golds.append(tmp_decode_texts)

    for predict, gold in zip(all_predicts, all_golds):
        save_tag = 0
        for item in predict[1:]:
            if item not in gold[1:]:
                save_tag = 1
                break

        if save_tag == 1:
            f2.write(predict[0] + "\n")
            for item in predict[1:]:
                print(item)
                f2.write(" ".join(item) + "\n")
            f2.write("\n\n")

            # f2.write("======================\n")

            f3.write(gold[0] + "\n")
            for item in gold[1:]:
                f3.write(" ".join(item) + "\n")

            f3.write("\n\n")
