# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

"""
@author: lishihang
@software: PyCharm
@file: TreeVis.py
@time: 2018/11/29 22:20
"""

from graphviz import Digraph
# 安装graphviz软件和安装graphviz的python模块
# https://pypi.org/project/graphviz/
from nltk.tree import Tree
# https://www.nltk.org/_modules/nltk/tree.html

from stanfordcorenlp import StanfordCoreNLP


def plot_model(tree, name):
    # g = Digraph()  #默认保存成文件
    g = Digraph("G", filename=name, format='png', strict=False)
    first_label = text.label()
    g.node("0", first_label)
    _sub_plot(g, tree, "0")
    g.view()


root = "0"


def _sub_plot(g, tree, inc):
    global root
    for node in tree:
        if not isinstance(node[0], Tree):
            root = str(int(root) + 1)
            g.node(root, node.label())
            g.edge(inc, root)
            # 加上叶子节点
            keep_root = root
            root = str(int(root) + 1)
            g.node(root, node[0])
            g.edge(keep_root, root)
        else:
            root = str(int(root) + 1)
            g.node(root, node.label())
            g.edge(inc, root)
            _sub_plot(g, node, root)


text = "(s (NP Mary) (VP (V saw) (NP Bob)))"
sentence = 'It is the virus, 2019 novel coronavirus that has breaks out worldwide.'
with StanfordCoreNLP(r'/container_data/sentence_parser/stanford-corenlp-full-2018-10-05', lang='en') as nlp:
    #  Tree.fromstring(nlp.parse(sentence)).draw() # 无法安装tkiner
    print(nlp.parse(sentence))
    print(nlp.dependency_parse(sentence))
    # tmp_text = nlp.parse(sentence).replace("\n", " ")
    # import re
    #
    # tmp_text = re.sub("\s{2,}", " ", tmp_text)
    # print(tmp_text)
    text = Tree.fromstring(nlp.parse(sentence))

plot_model(text, "hello.depend")
