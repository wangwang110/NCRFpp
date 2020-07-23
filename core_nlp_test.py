# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from graphviz import Digraph
from nltk.tree import Tree
from stanfordcorenlp import StanfordCoreNLP
import spacy
from spacy.tokenizer import Tokenizer


# 按照空格分句，会不会和corenlp又不一致了
def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, rules=None,
                     prefix_search=None,
                     suffix_search=None,
                     infix_finditer=None,
                     token_match=None)


spacy_nlp = spacy.load("en_core_web_sm")
spacy_nlp.tokenizer = custom_tokenizer(spacy_nlp)


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
            g.node(root, " ".join(node[0:]))
            g.edge(keep_root, root)
        else:
            root = str(int(root) + 1)
            g.node(root, node.label())
            g.edge(inc, root)
            _sub_plot(g, node, root)


def find_sub_tree(tree):
    result = ""
    # corenlp 会把特殊疑问词和它引导的句子作为两个部分
    merge = []
    for i in range(len(tree) - 1):
        if not isinstance(tree[i], Tree) or not isinstance(tree[i + 1], Tree):
            continue
        if tree[i].label().startswith("WH") \
                and tree[i + 1].label().startswith("S"):
            index = i + 1
            for node in tree[i + 1]:
                print(node)
                tree.insert(index, node)
                index += 1
            merge.append(index)

        if tree[i].label() in ["IN"] \
                and tree[i + 1].label().startswith("S"):
            index = i + 1
            for node in tree[i + 1]:
                print(node)
                tree.insert(index, node)
                index += 1
            merge.append(index)

    for idx in merge:
        del tree[idx]

    # 拿出来，从句不进行下一部的解析

    for node in tree:
        # if node.label() in sentences_tags:
        #     result += "(" + str(node.label())
        #     result += find_sub_tree(node)
        #     result += ")"
        if node.label() in sentences_tags:
            tag = 0
            for item in node:
                if "(S" in str(item):
                    tag = 1
                    break
            if tag == 0:
                result += "(" + str(node.label()) + " "
                result += str("_".join(node.leaves()))
                result += ")"
            else:
                result += "(" + str(node.label())
                result += find_sub_tree(node)
                result += ")"
        elif len(node) == 1:
            result += "(" + str(node.label()) + " "
            result += str("_".join(node.leaves()))
            result += ")"
        elif node.label() in ["NP", "NP-TMP"] and "(S" not in str(node) and "(VP" not in str(node) \
                and "(PP" not in str(node):
            result += "(" + str(node.label()) + " "
            result += str("_".join(node.leaves()))
            result += ")"
        elif node.label() in ["WHNP", "PP"]:
            result += "(" + str(node.label()) + " "
            result += str("_".join(node.leaves()))
            result += ")"
        else:
            result += find_sub_tree(node)
    return result


def merge_same_node(node):
    if len(node) <= 1:
        return str(node)
    else:
        num = len(node)
        merge = []
        result = "(" + node.label()
        for i in range(num - 1):
            if not isinstance(node[i], Tree) or not isinstance(node[i + 1], Tree):
                continue
            # 相邻的谓语合并
            if node[i].label() in ["VB", "VBD", "VBZ", "VBN", "VBG"] \
                    and node[i + 1].label() in ["VB", "VBD", "VBZ", "VBN", "VBG"]:
                merge.append(i)
                node[i + 1].set_label("VB")
                node[i + 1][0] = node[i][0] + "_" + node[i + 1][0]
            if node[i].label() in ["IN"] \
                    and node[i + 1].label() in ["IN"]:
                merge.append(i)
                node[i + 1].set_label("VB")
                node[i + 1][0] = node[i][0] + "_" + node[i + 1][0]

        for j in range(num):
            if j in merge:
                del node[j]
        for j in range(len(node)):
            result += merge_same_node(node[j])
        result += ")"
    return result


def get_tag_spacy(tree):
    for node in tree:
        if not isinstance(node[0], Tree):
            key = node[0].replace("_", " ")
            # if node.label() == "PP":
            #     node.set_label("adverbial_modifier")
            # el
            if key in spans_item:
                # if spans_item[key] in ["subject", "predicate", "dobj"]:
                node.set_label(spans_item[key])
        else:
            tmp_tree = get_tag_spacy(node)
    return tree


"""
1. chunking 利用现有的Constituency parsing获得NP和PP，VP需要继续分开，因为Constituency parsing认为S->NP VP，
却不考虑宾语
2. 根据chunking的结果，利用spacy进行Dependency parsing，从而获得chunking不同部分之间的关系
"""

# sentence = 'Mary saw Bob yesterday'
# sentence = "He reckons the current account deficit will narrow to only 1.8 billion in September ."
# sentence = 'Mary saw that Bob saw Lily yesterday.'
# sentence = "woman:Would you like some vegetable dumplings for brakfast ?"


with StanfordCoreNLP(r'/container_data/sentence_parser/stanford-corenlp-full-2018-10-05', lang='en') as nlp:
    #  Tree.fromstring(nlp.parse(sentence)).draw() # 无法安装tkiner
    tree_texts = []
    # texts = ["Fill in the blanks with the words in the box.thenand practice."]
    with open("./online_clean_texts.txt") as f:
        texts = f.readlines()[:25]
        texts.append("It was on the farm where I worked that I met my girlfriend for the first time .")
        texts.append("Look, think and Complete the sentences.")
        texts.append("I take the bus to school.")
        texts.append("From what aspects does the radio program talk about the Eiffel Tower?")
        texts.append("It 's three dolllars and seventy-five cents .")
        for sentence in texts:
            # words = ["S"]
            # words.extend(nlp.word_tokenize(sentence))
            # 句中若存在句号，默认处理第一句
            # print("================")
            # print(sentence)
            # print(nlp.parse(sentence))
            tree_texts.append(Tree.fromstring(nlp.parse(sentence)))
            # print(nlp.dependency_parse(sentence))
            # text_list = nlp.dependency_parse(sentence)

index = 0
sentences_tags = ["S", "SBAR", "SBARQ", "SINV", "SQ"]
# 句子标签
for tree_text in tree_texts:
    index += 1
    # 1.利用现有的Constituency parsing获得NP和PP
    print("\n\n\n++++++++++++++++++++++++++++++++++")
    print(" ".join(tree_text.leaves()))
    print(tree_text)

    print("============1step获得NP，PP短语===============")

    for node in tree_text:
        if node.label() not in sentences_tags:
            label = "Segmet"
            node.set_label(label)
            #
        label = node.label()
        result = find_sub_tree(node)
        result = "(" + label + result + ")"
        print(result)
        tmp_tree_result = Tree.fromstring(result)
        tree_result = Tree.fromstring(merge_same_node(tmp_tree_result))
        print(tree_result)

    # 2. 根据chunking的结果，利用spacy进行Dependency parsing，从而获得chunking不同部分之间的关系
    print("============2step 获得spacy标签===============")
    chunking = tree_result.leaves()
    print(chunking)

    sent = " ".join(tree_result.leaves()).replace("_", " ")
    spacy_dep_parser = []
    doc = spacy_nlp(sent)
    i = 0
    spans = []
    for text in chunking:
        text = text.replace("_", " ")
        words = [token for token in spacy_nlp(text)]
        spans.append(doc[i:i + len(words)])
        i += len(words)

    spans_item = {}
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)
    for token in doc:
        # if token.head.i == token.i:
        #     token.dep_ = "predicate"
        # if token.dep_ == "nsubj":
        #     token.dep_ = "subject"
        # if token.dep_ == "dobj":
        #     token.dep_ = "object"
        print(token.text, token.i + 1, token.dep_, token.head.text, token.head.i + 1)
        spans_item[token.text] = token.dep_

    final_result = get_tag_spacy(tree_result)
    print(final_result)
    plot_model(final_result, "hello.chunk" + "_" + str(index))
