# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

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


path = "./LAL-Parser/tmp_picture/"
path_dep = "./LAL-Parser/tmp_picture_dep/"
with open("./output_synconst_2.txt") as f, \
        open("./output_syndephead_2.txt") as f1, \
        open("./output_syndeplabel_2.txt") as f2:
    indx = 0
    new_indx = 0
    for r, s, t in zip(f.readlines(), f1.readlines(), f2.readlines()):
        words = ["S"]
        try:
            tree_text = Tree.fromstring(r)
            words.extend(tree_text.leaves())

            print(tree_text)
            print("\n\n\n")
            indx += 1
            plot_model(tree_text, path + "sent.cons" + str(indx))
            # start_li = s.strip().strip("[").strip("]").strip().split(",")
            # labels = t.strip().strip("[").strip("]").strip().split(",")
            # li_dep = [(label.strip().strip("'").strip(), start, end) for label, start, end in
            #           zip(labels, start_li, range(1, len(words)+1),
            #               )
            #           ]
            # plot_model_dep(words, li_dep, path + "sent.dep" + str(indx))
        except:
            print("cons error:",  " ".join(words))
            indx += 1

        try:
            new_indx += 1
            # plot_model(tree_text, path + "sent.cons" + str(indx))
            start_li = s.strip().strip("[").strip("]").strip().split(",")
            labels = t.strip().strip("[").strip("]").strip().split(",")
            li_dep = [(label.strip().strip("'").strip(), start, end) for label, start, end in
                      zip(labels, start_li, range(1, len(words) + 1),
                          )
                      ]
            plot_model_dep(words, li_dep, path_dep + "sent.cons_dep" + str(indx))
        except:
            new_indx += 1
            print("dep error:", " ".join(words))
