# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree


tagged_text = "[ The/DT cat/NN ] sat/VBD on/IN [ the/DT mat/NN ] [ the/DT dog/NN ] chewed/VBD ./."
gold_chunked_text = tagstr2tree(tagged_text)
# unchunked_text = gold_chunked_text.flatten()
print(gold_chunked_text)

tag_pattern = "<DT>?<JJ>*<NN.*>"
regexp_pattern = tag_pattern2re_pattern(tag_pattern)
print(regexp_pattern)


chunk_rule = ChunkRule("<.*>+", "Chunk everything")
chink_rule = ChinkRule("<VBD|IN|\.>", "Chink on verbs/prepositions")
split_rule = SplitRule("<DT><NN>", "<DT><NN>", "Split successive determiner/noun pairs")

