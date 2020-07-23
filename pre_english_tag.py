# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import re
from tqdm import tqdm

# 训练集
path = "./all_data_see.txt"
path_out = "./all_see_tag.txt"
path_out_text = "./all_see_text.txt"
path_test = "./test_see_text.txt"

# 测试集
# path = "./tag_see_data_vip.txt"
# path_out = "./test_see_tag.txt"
# path_out_text = "./test_see_text.txt"

with open(path, "r", encoding="utf-8") as f, open(path_out, "w", encoding="utf-8") as f1, \
        open(path_test, "r") as f_test, open(path_out_text, "w") as f2:
    i = 0
    tag = 0
    all_texts = []
    unique = set()
    tmp_texts = []
    test_data = [text.strip() for text in f_test.readlines()]
    for line in tqdm(f.readlines()):
        line = line.strip()
        if line != "":
            tmp_texts.append(line.strip())
            tag = 1
        if line == "" and tag == 1:
            if tmp_texts[0] not in unique and tmp_texts[0] not in test_data:
                i += 1
                all_texts.append(tmp_texts)
                unique.add(tmp_texts[0])
            tmp_texts = []
            tag = 0
    print(i)

    for texts in all_texts:
        tmp_list = []
        for text in texts:
            if u"倒装句" in text or u"被移位" in text or "独立结构" in text or "位置被提前" in text:
                tmp_words = re.split("\s{1,}", text.strip())
                text = " ".join(tmp_words[:-1])
            if u"语" in text or u"插入" in text or u"句式" in text:
                text = re.sub("(?<!同)位语", "同位语", text)
                text = re.sub("直接宾语", "宾语", text)
                text = re.sub("先行形式宾语", "宾语", text)
                words = re.split("\s{1,}", text.strip())
                if str(words[-1]).endswith("状语从句"):
                    words[-1] = "状语从句"
                if str(words[-1]).endswith("定语从句"):
                    words[-1] = "定语从句"
                if str(words[-1]).endswith("后置定语"):
                    words[-1] = "定语"
                if str(words[-1]).endswith("补足语") or str(words[-1]).endswith("补语"):
                    words[-1] = "补足语"
                if str(words[-1]).endswith("先行主语"):
                    words[-1] = "主语"
                if str(words[-1]).endswith("形式主语"):
                    words[-1] = "主语"
                if str(words[-1]).endswith("插入"):
                    words[-1] = "插入语"
                if len(words[:-3]) < 2 and str(words[-1]).endswith("从句"):
                    continue
                if str(words[-1]).endswith("句子状语") and len(words[:-3]) < 2:
                    continue
                if str(words[-1]) == "主语":
                    all_words = texts[0].strip().split(" ")
                    next_id = int(words[-3]) + 1
                    if next_id < len(all_words) and all_words[next_id] == ":":
                        continue

                tmp_list.append(
                    " ".join(words[:-3]) + "\t" + str(words[-3]) + "\t" + str(words[-2]) + "\t" + str(words[-1]) + "\n")

        res_list = sorted(set(tmp_list), key=lambda s: int(s.split("\t")[1]))
        # 排除掉不是句子, 没有谓语的
        tmp_tag = 0
        try:
            for res in res_list:
                if res.strip().split("\t")[3] == u"谓语":
                    tmp_tag = 1
                    break
                else:
                    continue
        except:
            print(texts[0].strip())
            continue
        if tmp_tag == 0 or "don 't" in texts[0].strip() or "Don 't" in texts[0].strip():
            continue

        texts[0] = re.sub("\s{2,}", " ", texts[0])
        f1.write(texts[0].strip() + "\n")
        f2.write(texts[0].strip() + "\n")

        # 开始位置相同，只保留位置长的
        # 开始位置，结束位置都相同，全删掉
        num = len(res_list)
        remove_id = []
        for i in range(num):
            if i + 1 < num and int(res_list[i].split("\t")[1]) == int(res_list[i + 1].split("\t")[1]):
                if int(res_list[i].split("\t")[2]) > int(res_list[i + 1].split("\t")[2]):
                    remove_id.append(i + 1)
                else:
                    remove_id.append(i)
            if i + 1 < num and int(res_list[i].split("\t")[1]) == int(res_list[i + 1].split("\t")[1]) and \
                    int(res_list[i].split("\t")[2]) == int(res_list[i + 1].split("\t")[2]):
                remove_id.append(i + 1)
                remove_id.append(i)
        #

        for i in range(num):
            if i in remove_id:
                continue
            res = res_list[i]
            f1.write(res.strip() + "\n")

        f1.write("\n\n")
