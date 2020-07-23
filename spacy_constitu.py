# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from graphviz import Digraph
from nltk.tree import Tree
from stanfordcorenlp import StanfordCoreNLP
import spacy
from benepar.spacy_plugin import BeneparComponent
from spacy.tokenizer import Tokenizer

"""
通过数据查看依赖树的解析情况
"""


# 按照空格分句，会不会和corenlp又不一致了
# def custom_tokenizer(nlp):
#     return Tokenizer(nlp.vocab, rules=None,
#                      prefix_search=None,
#                      suffix_search=None,
#                      infix_finditer=None,
#                      token_match=None)


spacy_nlp = spacy.load("en_core_web_sm")
# spacy_nlp.tokenizer = custom_tokenizer(spacy_nlp)
spacy_nlp.add_pipe(BeneparComponent("benepar_en2"))


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

path = "./save_picture/"

with open("./online_clean_texts.txt") as f:
    texts = f.readlines()
    indx = 0
    for sentence in texts:
        doc = spacy_nlp(sentence)
        sent = list(doc.sents)[0]
        indx += 1
        print(sent._.parse_string)
        try:
            tree_text = Tree.fromstring(sent._.parse_string)
            plot_model(tree_text, path + "sent.cons"+str(indx))
        except:
            print(sentence)
            continue
        # print(sent._.parse_string)
        # print(sent._.labels)
        # print(list(sent._.children))
