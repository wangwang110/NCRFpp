# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import re
from tqdm import tqdm

"""
序列标注的结果与原来的标注做对比
"""

path = "./data/tets.out"
path_1 = "./test_see_tag.txt"
path_out = "./compare.txt"

with open(path, "r", encoding="utf-8") as f, open(path_1, "r", encoding="utf-8") as f1, \
        open(path_out, "w", encoding="utf-8") as f2:
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

    # num = len(all_texts)
    for texts, texts_model in zip(all_texts, all_texts_model):
        tmp_list = []
        for text in texts:
            f2.write(text.strip() + "\n")
        f2.write("====================================\n")
        for text in texts_model:
            f2.write(text.strip() + "\n")
        #
        f2.write("\n\n")
