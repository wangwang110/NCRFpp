# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from graphviz import Digraph
# 安装graphviz软件和安装graphviz的python模块
# https://pypi.org/project/graphviz/
from nltk.tree import Tree
# https://www.nltk.org/_modules/nltk/tree.html

# from stanfordcorenlp import StanfordCoreNLP


# https://github.com/Lynten/stanford-corenlp cornlp的python接口，可以以两种方式调用


def plot_model_dep(li_word, li_dep, name):
    # g = Digraph()  #默认保存成文件
    g = Digraph("G", filename=name, format='png', strict=False)
    for dep in li_dep:
        start = int(dep[1])
        end = int(dep[2])
        g.node(name=li_word[start] + str(start), label=li_word[start], color='red')
        # name是唯一标识
        g.node(name=li_word[end] + str(end), label=li_word[end], color='blue')
        g.edge(li_word[start] + str(start), li_word[end] + str(end), dep[0])
    g.view()


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
sentence = 'It is the 2019 novel coronavirus that has breaks out worldwide.'
sentence = "He reckons the current account deficit will narrow to only 1.8 billion in September ."
sentence = 'Mary saw that Bob saw Lily yesterday.'
sentence = "woman:Would you like some vegetable dumplings for brakfast ?"
save_path = "./tmp_picture/"
# with StanfordCoreNLP(r'/container_data/sentence_parser/stanford-corenlp-full-2018-10-05', lang='en') as nlp:
path = "./LAL-Parser/tmp_picture/"
with open("./LAL-Parser/output_synconst_2.txt") as f:
    texts = f.readlines()
    indx = 0
    for result in texts:
        # words = ["S"]
        # words.extend(nlp.word_tokenize(sentence))
        # result = nlp.parse(sentence)
        # print(words)
        # words.append("S")
        # print(nlp.dependency_parse(sentence))
        # text_list = nlp.dependency_parse(sentence)
        tree_text = Tree.fromstring(result)
        print(tree_text)
        print("\n\n\n")
        indx += 1
        plot_model(tree_text, save_path + "sent.cons" + str(indx))
        # plot_model_dep(words, text_list, "hello.dep")
