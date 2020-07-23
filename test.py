# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import spacy
from nltk import Tree
from spacy import displacy

from graphviz import Digraph
# 安装graphviz软件和安装graphviz的python模块
# https://pypi.org/project/graphviz/
from nltk.tree import Tree


def plot_model_dep(li_word, li_dep, name):
    # g = Digraph()  #默认保存成文件
    g = Digraph("G", filename=name, format='png', strict=False)
    for dep in li_dep:
        start = int(dep[1])
        end = int(dep[2])
        g.node(name=li_word[start] + str(start), label=li_word[start], color='red')
        # name 是唯一标识这个节点的
        g.node(name=li_word[end] + str(end), label=li_word[end], color='blue')
        g.edge(li_word[start] + str(start), li_word[end] + str(end), dep[0])
    g.view()


en_nlp = spacy.load("en_core_web_sm")


texts = ["The fruit and vegetables are healthy ","What is the next letter in this sequnence?"]
indx = 0
for sentence in texts:
    doc = en_nlp(sentence)
    # displacy.serve(doc, style='dep') spacy自带的可视化工具，浏览器中打开

    spacy_dep_parser = []
    words = ["S"]
    tags = []
    root_id = 0
    # for chunk in doc.noun_chunks:
    #     print(chunk)

    for token in doc:
        words.append(str(token))
        tags.append(token.dep_)
        if token.head.i == token.i:
            token.dep_ = "predicate"
            spacy_dep_parser.append((token.dep_, 0, token.i + 1))
        else:
            spacy_dep_parser.append((token.dep_, token.head.i + 1, token.i + 1))

        print(token.text, token.i + 1, token.dep_, token.head.text, token.head.i + 1)

    print(words)
    indx += 1
    try:
        plot_model_dep(words, spacy_dep_parser, "spacy.cons_dep" + str(indx))
    except:
        print(sentence)
        continue
