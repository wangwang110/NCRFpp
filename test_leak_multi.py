# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

# from fairseq_GEC import distance
# from fairseq_GEC.errant.scripts import toolbox, align_text, cat_rules
# from nltk.stem.lancaster import LancasterStemmer
import spacy
import time

# tag_map = toolbox.loadTagMap("./fairseq_GEC/errant/resources/en-ptb_map")
# category_map = toolbox.loadCategoryMap("./fairseq_GEC/errant/resources/grammar_category_map")
# stemmer = LancasterStemmer()
#
# detect_dicts = distance.WORDS

nlp = spacy.load("en")
src_text = """If you had not helped me,I would have been drowned."""
trg_text = """If you had not helped me , I would have been drowned ."""


def get_tag_parser_all(sents):
    all_list = []
    # for sent in sents:
    #     all_list.append(nlp(sent))
    for sent in nlp.pipe(sents, n_threads=2):
        all_list.append(sent)
    return all_list


# def test():
#     tmp = get_tag_parser_all([src_text, trg_text], nlp)
#     # 这一个就已经有错误了
#     # auto_edits = align_text.getAutoAlignedEdits(tmp[0], tmp[1], nlp, "DL")
#     # for auto_edit in auto_edits:
#     #     # Give each edit an automatic error type.
#     #     cat = cat_rules.autoTypeEdit(auto_edit, tmp[0], tmp[1],
#     #                                  detect_dicts, tag_map, nlp, stemmer)
#     #     auto_edit[2] = cat
#     print(tmp)
#
#     output_dict = {
#         "status": 0,
#         "msg": u"纠错完成",
#         "data": {"spell_errors": [], "grammar_errors": []}
#     }
#     time.sleep(1)
#
#     return output_dict

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=30)

    all_data = []
    for i in range(100):
        all_data.append([src_text, trg_text])

    for t in range(10000):
        for tmp_data in executor.map(get_tag_parser_all, all_data):
            print(tmp_data)
        print("==============================")
