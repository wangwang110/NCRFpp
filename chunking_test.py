# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

"""

chunking 也叫 shallow parser，是介于词性标注和完全解析树之间的一种方法.
从任务上看与NER相似，
可以使用基于规则的方法和基于机器学习的方法
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import nltk
from graphviz import Digraph
# 安装graphviz软件和安装graphviz的python模块
# https://pypi.org/project/graphviz/
from nltk.tree import Tree
# https://www.nltk.org/_modules/nltk/tree.html


# 2. 基于机器学习的方法（最大熵分类器）
# https://nickcdryan.com/2017/02/13/shallow-parsing-for-entity-recognition-with-nltk-and-machine-learning/
# 输入有两种形式，一是原始的文本，二是原始文本+词性标注（准确率相比前者会高很多,如下所示）

def tags_since_dt(sentence, i):
    tags = set()
    for word, pos in sentence[:i]:
        if pos == 'DT':
            tags = set()
        else:
            tags.add(pos)
    return '+'.join(sorted(tags))


def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "&lt;START&gt;", "&lt;START&gt;"
    else:
        prevword, prevpos = sentence[i - 1]
    if i == len(sentence) - 1:
        nextword, nextpos = "&lt;END&gt;", "&lt;END&gt;"
    else:
        nextword, nextpos = sentence[i + 1]
    return {"pos": pos,
            "word": word,
            "prevpos": prevpos,
            "nextpos": nextpos,
            "prevword": prevword,
            "nextword": nextword,
            "prevpos+pos": "%s+%s" % (prevpos, pos),
            "pos+nextpos": "%s+%s" % (pos, nextpos),
            "prevpos+pos+nextpos": "%s+%s+%s" % (prevpos, pos, nextpos),
            "prevword+word+nextword": "%s+%s+%s" % (prevword, word, nextword),
            "tags-since-dt": tags_since_dt(sentence, i)}


class ConsecutiveNPChunkTagger(nltk.TaggerI):

    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train(
            train_set, algorithm='IIS', trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)


class ConsecutiveNPChunker(nltk.ChunkParserI):

    def __init__(self, train_sents):
        tagged_sents = [[((w, t), c) for (w, t, c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        # 词->词性->chunk标签
        # iob_tagged = tree2conlltags(chunked_sentence)
        # chunk_tree = conlltags2tree(iob_tagged)
        # len(conll2000.chunked_sents())  # 10948
        # len(conll2000.chunked_words())  # 166433
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w, t, c) for ((w, t), c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)

"===================================================================================="


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


# 保存模型
import pickle
chunker = pickle.load(open("chunker.bin", "rb"))
# 'It is the 2019 novel coronavirus that has breaks out worldwide.'
sentence = 'He reckons the current account deficit will narrow to only 1.8 billion in September .'
# sentence = "We saw the yellow dog"
sentence = "woman:Would you like some vegetable dumplings for brakfast ?"
test_sent_words = nltk.word_tokenize(sentence)
test_sent_pos = nltk.pos_tag(test_sent_words)
test_sent = [(word, pos) for word, pos in zip(test_sent_words, test_sent_pos)]
text = chunker.parse(test_sent_pos)
print(text)

tree_text = Tree.fromstring(str(text))

plot_model(tree_text, "hello.chunk")



