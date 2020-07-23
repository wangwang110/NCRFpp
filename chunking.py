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
import pprint
import re


# 1. 基于规则的方法需要自己，定义chunking的文法，并且需要注意嵌套

def preprocess(doc):
    sentences = nltk.sent_tokenize(doc)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


sentence = "The blogger taught the reader to chunk"
sentence = preprocess(sentence)
print(sentence)

grammar = "NP: {<DT>?<JJ>*<NN>}"
NPChunker = nltk.RegexpParser(grammar)
result = NPChunker.parse(sentence[0])
print(result)


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


"""
下载数据，没有验证集合--nltk.download("conll2000")
只有NP PP VP三种类型, 训练
"""

from nltk.corpus import conll2000

train_sents = conll2000.chunked_sents('train.txt')
chunked_sentence = conll2000.chunked_sents()[0]
# print(train_sents[0])
test_sents = conll2000.chunked_sents('test.txt')
chunker = ConsecutiveNPChunker(train_sents)
print(chunker.evaluate(test_sents))

sentence = 'It is the 2019 novel coronavirus that has breaks out worldwide.'
test_sent_words = nltk.word_tokenize(sentence)
test_sent_pos = nltk.pos_tag(test_sent_words)
test_sent = [(word, pos) for word, pos in zip(test_sent_words, test_sent_pos)]
print(chunker.parse(test_sent_pos))

# 保存模型
import pickle
pickle.dump(chunker, open("chunker.bin", "wb"))
# 下次使用直接加载 chunker = pickle.load(open("chunker.bin", "rb"))

