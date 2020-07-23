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


def plot_model(tree, name):
    # g = Digraph()  #默认保存成文件
    g = Digraph("G", filename=name, format='png', strict=False)
    first_label = tree.label()
    g.node("0", first_label)
    _sub_plot(g, tree, "0")
    g.view()


root = "0"


def _sub_plot(g, tree, inc):
    global root
    for node in tree:
        if not isinstance(node[0], Tree):
            root = str(int(root) + 1)
            if isinstance(node, Tree):
                g.node(root, node.label())
                g.edge(inc, root)
                keep_root = root
            else:
                keep_root = inc
            # 加上叶子节点
            root = str(int(root) + 1)
            g.node(root, " ".join(node[0:]))
            g.edge(keep_root, root)
        else:
            root = str(int(root) + 1)
            g.node(root, node.label())
            g.edge(inc, root)
            _sub_plot(g, node, root)


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




from spacy.tokenizer import Tokenizer

# def custom_tokenizer(nlp):
#     return Tokenizer(nlp.vocab, rules=None,
#                                 prefix_search=None,
#                                 suffix_search=None,
#                                 infix_finditer=None,
#                                 token_match=None)

en_nlp = spacy.load("en_core_web_sm")
# en_nlp.tokenizer = custom_tokenizer(en_nlp)

sentence = 'Do you know what should you do when you meet these big accidents?'
sentence = "What 's the meanings of his art pieces ?"
sentence = "How else can we answer that ?"
sentence = "Take the medicine three times a day , and one tsblet each time ."
sentence = "let's paly with them "
sentence = "he is tried, so he went to bed"
sentence = "what a beautiful girl she is"
sentence = "Q1 : What is the weather like in Sydeny ?"
sentence = "Wang Hua is the only students in our school who will attend the meeting."

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


plot_model_dep(words, spacy_dep_parser, "spacy.cons_dep")

