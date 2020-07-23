# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import spacy
from nltk import Tree

en_nlp = spacy.load('en_core_web_sm')

sentence = 'It is the virus, 2019 novel coronavirus that has breaks out worldwide.'

# 1.
doc = en_nlp(sentence)
# 为什么会给自动分句
# def to_nltk_tree(node):
#     if node.n_lefts + node.n_rights > 0:
#         return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
#     else:
#         return node.orth_


def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)


# [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]


import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(sentence)
displacy.serve(doc, style='dep')

