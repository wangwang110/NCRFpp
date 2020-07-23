# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from graphviz import Digraph
# 安装graphviz软件和安装graphviz的python模块
# https://pypi.org/project/graphviz/
# graphviz软件教程
# https://www.jianshu.com/p/6d9bbbbf38b1
# 输出图片中有中文可能会有错,可以使用svg格式
from nltk.tree import Tree
# https://www.nltk.org/_modules/nltk/tree.html

from stanfordcorenlp import StanfordCoreNLP


# https://github.com/Lynten/stanford-corenlp corenlp的python接口，可以以两种方式调用


def plot_model_dep(li_word, li_dep, name):
    # g = Digraph()  #默认保存成文件
    g = Digraph("G", filename=name, format='svg', strict=False)
    for dep in li_dep:
        start = int(dep[1])
        end = int(dep[2])
        g.node(name=li_word[start] + str(start), label=li_word[start], color='red', fontname="FangSong")
        # name是唯一标识
        g.node(name=li_word[end] + str(end), label=li_word[end], color='blue', fontname="FangSong")
        g.edge(li_word[start] + str(start), li_word[end] + str(end), dep[0])
    g.view()


# g = Digraph('测试图片')
# g.node(name='a',color='red')
# g.node(name='b',color='blue')
# g.edge('a','b',color='green')
# g.view()


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


# text = "(s (NP Mary) (VP (V saw) (NP Bob)))"
sentence = 'Mary saw Bob yesterday'
# sentence = 'It is the 2019 novel coronavirus that has breaks out worldwide.'
sentence = "He reckons the current account deficit will narrow to only 1.8 billion in September ."
sentence = 'Mary saw that Bob saw Lily yesterday.'
sentence = u"我之前做的一些课件存储在云课件里了！然后现在在什么也找不到了什么原因呢？"

# en

with StanfordCoreNLP(r'/container_data/sentence_parser/stanford-corenlp-full-2018-10-05', lang='zh') as nlp:
    #  Tree.fromstring(nlp.parse(sentence)).draw() # 无法安装tkiner
    words = ["S"]
    words.extend(nlp.word_tokenize(sentence))
    print(words)
    # words.append("S")
    print(nlp.parse(sentence))
    print(nlp.dependency_parse(sentence))
    text_list = nlp.dependency_parse(sentence)
    tree_text = Tree.fromstring(nlp.parse(sentence))

plot_model(tree_text, "hello.gv")
plot_model_dep(words, text_list, "hello.dep")
