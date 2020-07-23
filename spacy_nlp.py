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


def find_sub_sent(doc, tags):
    if len(doc) <= 1:
        return ["(" + str(token.dep_) + " " + str(token.text) + "/" + str(token.tag_) + ")" for token in doc]
    elif len(set(tags) & set(cluse_tags)) == 0:
        return ["(" + str(token.dep_) + " " + str(token.text) + "/" + str(token.tag_) + ")" for token in doc]
    else:
        pos = []
        for j in range(len(doc)):
            if doc[j].dep_ in cluse_tags:
                doc[j].dep_ = "predicate"
                start = doc[j].left_edge.i
                end = doc[j].right_edge.i + 1
                span = doc[start:end]
                tags = [token.dep_ for token in span]
                result_sune_sent = find_sub_sent(span, tags)
                pos.append((result_sune_sent, start, end))

        # add
        result = []
        k = 0
        for j in range(len(doc)):
            tag = 0
            for pos_index in pos:
                result_sune_sent, start, end = pos_index
                if start < j < end:
                    continue
                elif j == start:
                    tag = 1
                else:
                    tag = 2

            if tag == 1:
                result.append("(cluase\n")
                result.append("\n".join(pos[k][0]))
                result.append(")\n")
                k += 1

            if tag == 2:
                if doc[j].dep_ == "ROOT":
                    doc[j].dep_ = "predicate"
                result.append(("(" + doc[j].dep_ + " " + doc[j].text + "/" + doc[j].tag_ + ")" + "\n"))

        return result


from spacy.tokenizer import Tokenizer

# def custom_tokenizer(nlp):
#     return Tokenizer(nlp.vocab, rules=None,
#                                 prefix_search=None,
#                                 suffix_search=None,
#                                 infix_finditer=None,
#                                 token_match=None)

en_nlp = spacy.load("en_core_web_sm")
# en_nlp.tokenizer = custom_tokenizer(en_nlp)

sentence = 'It is the virus, 2019 novel coronavirus that has breaks out worldwide.'
sentence = 'He reckons the current account deficit will narrow to only 1.8 billion in September .'
sentence = 'Mary saw that Bob saw Lily yesterday.'
sentence = "woman:Would you like some vegetable dumplings for brakfast ?"
sentence = "He/She was shy when starting his/her first day in Grade 7 ."
sentence = "It 's three dolllars and | seventy-five cents .."

with open("./online_clean_texts.txt") as f:
    texts = f.readlines()
    indx = 0
    # for sent in texts:
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



        # # 递归,转化为主谓宾的形式
        # cluse_tags = ["ccomp"]
        #
        # result = find_sub_sent(doc, tags)
        # text = "(S" + "\n"
        # text += "".join(result)
        # text += ")"
        # print(text)
        # tree_text = Tree.fromstring(str(text))
        # plot_model(tree_text, "hello.test")
