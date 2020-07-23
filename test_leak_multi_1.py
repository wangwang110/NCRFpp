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
trg_text = """If you had not help me , I would have been drowned ."""
# from utils.gec_utils import not_gramamr_postag

def get_tag_parser_all(sents):
    all_list = []
    # for sent in sents:
    #     all_list.append(nlp(sent))
    for sent in nlp.pipe(sents, n_threads=2):
        all_list.append(sent)
    return all_list

#
# def test(data):
#     src_text, trg_text = data
#     tmp = get_tag_parser_all([src_text, trg_text], nlp)
#     # 这一个就已经有错误了
#     auto_edits = align_text.getAutoAlignedEdits(tmp[0], tmp[1], nlp, "DL")
#     for auto_edit in auto_edits:
#         # Give each edit an automatic error type.
#         cat = cat_rules.autoTypeEdit(auto_edit, tmp[0], tmp[1],
#                                      detect_dicts, tag_map, nlp, stemmer)
#         auto_edit[2] = cat
#     # tmp = not_gramamr_postag(src_text)
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

    # all_data = []
    # for i in range(100):
    #     all_data.append([src_text, trg_text])

    all_data = []
    all_text_1 = [
        "wqewq wqe wq ewq ewq e",
        "dsjkfignvfidvnv jfdfnoijjkmvfk  dsffsdfsdfs dsffsdfsdfs",
        "dsffsdfsdfs dsffsdfsdfs dsffsdfsdfs ",
        "dsffsdfsdfs lonngvjykghkwag",
        "how lonngvjykghkwag have beenyou here?",
        "how lonng have beenyoubeenyou herle?",
        "dsffasl like to ttt learn",
        "[1, 2]",
        "DFdcvfdgfvfbvbdgfbfg",
        "\n\n",
        "###",
        " ",
        "中国",
        "中国 abc",
        "??? uuu",
        "I very 中国 ### like 12233erf ",
        "he is a boy !!!!!!!!!!"
        "Hes likes listen to music .",
        "hello woeld",
        "fireds",
        "dog",
        "aby",
        "Englishhhhhhh",
        "Englishhhhs",
        "if yuu writee a wrong englist sentence should be cheek by softwire auto",
        "if yuu writee a wrong englist sentence should be cheek by softwire auto",
        "if yuu writee a wrong englist sentence should be cheek by softwire auto",
        '''You make some noises,when you are hungry.''',
        '''You make some noises,
        when you are hungry.''',
        '''You make some noises,
          when you are hungry.''',
        '''You make some noises,	when you are hungry.''',
        '''You make some noises,\r\n\twhen you are hungry.''',
        '''You make some noises,\r\nwhen you are hungry.''',
        "You make some noises,when you are hungry.",
        "You make some noises, when you are hungry.",
        '''You make some noises,\nwhen you are hungry.''',
        '''You make some noises,\n   when you are hungry.''',
        "Can you gave more(更多) adice?",
        "I don understand you.",
        "He're a good boy !",
        '''Hello,     I am Jack''',
        '''if yuu writee a wrong englist sentence should be cheek 
                by softwire auto''',
        "how lonng        \nhave been you here?",
        "How               am you ?",
        "Everybody haven't their ？dream and so do I.",
        "  Everybody haven't their ？dream and so do I.",
        "Everybody haven't their ？dream and so do I.   ",
        "how lonng        have  you here?",
        "how lonng        have been you here?how lonng        have been you here?how lonng        have been you here?",
        "  how lonng        have been you here?how lonng        have been you here?how lonng        have been you here?",
        "  how lonng        have been you here?how lonng        have been you here?how lonng        have been you here?  ",
        "I think if I have         a dream,  my life will better. ",
        "  Everybody haven't their dream and so do I. I think if I have a dream, my life will better. My Dream is to be a siger, a famous singer. If you ask me why , I will answer you I love singing, And I love listening to music,Singing can make me happy. If I am sad, I like singing , too . And how can I make my dream come true ? I will listen to music everyday. And I will practising singing every day . And keep on writing song are important, too . That's all about my dream. I sincerely suggest you make it habit to talk to others .",
        " I know you coming to the Beijing in last month .",
        "everybody havet their dream and so do I.          everybody havet their dream and so do I. ",
        "Eat well, stay heathly , and don’t  get fat!",
        "What time it is now?",
        "Some people make your laugh a little louder, your smile a little brighter and your life a little better.",
        "The monkey is very angry .",
        "The monkey is very angry , yesterday.",
        "A fly comes and sits on the end of the man's nose.",
        "Whats are your names?",
        "As you know , I am goig to graduate from my college , So that I need to prepare for an article for that .",
        "everybody havet their dream and so do I everybody havet their dream and so do I everybody havet their dream and so do I everybody havet their dream and so do I everybody havet their dream and so do I. everybody havet their dream and so do I ",
        "In my opinin , Beijing is a wonderful place to spend your holiday and I hope that you can get the change to visit my favorite city .",
        "This hapens five or six times. The monkey is very angry.",
        "What time it is now?",
        "I like to to learn English",
        "I want big apple.",
        "i wnt to eat a apple.",
        "everybody havet their dream and so do I.everybody havet their dream and so do I.everybody havet their dream and so do I. everybody havet their      dream and so do I.",
        "Everybody haven't their？ dream and so do I. I think if I have a dream, my life will better",
        "Everybody haven't their ？dream and so do I.",
        "How am you ?",
        "My Dream is to be a siger, a famous singer.",
        "If you ask me why , I will aswer you I love singing, And I love listening to music,Singing can make me happy.",
        "If I am sad, I like singing , too .",
        "And how can I make my dream come true ？",
        "I will listen! to music everyday.",
        "And I will practising singing every day .",
        "And keep on writing songs are important, too .",
        "That's all about my dream.",
        "I sincerely suggest you make it habit to talk to others .",
        "everybody havet their dream and so do I.everybody havet their dream and so do I.everybody havet their dream and so do I.everybody havet their dream and so do I.",
        "I do liked it very much.",
        " These are phrases we may used in spoken English, but that should not be used in written English as they are incomplet. These are phrases we may used in spoken English, but that should not be used in written English as they are incomplet.",
        '''I recall when I was young oh, I will play and always having fun ,with the neighbours next to me and we’ll play until the setting sun, try to be the best among the others,in a game called the “spider battle” ,it doesn’t matter,who is the best now, those were the days of my past Few years later when I got to school and was late for lesson,all the time,always day dreaming in the class, till I don’t even know the lessons done,then my teacher always told me,never ever be lazy again,what can I do now,what can I say now,those were the days of my past As the days go on and on,I grew up and had my first love,candle light and sandy beach,finally give away my first kiss,mother said I was too young to fall in love and,then I will one day regret ,so love was over,but I do miss her,those were the days of my past Just when I left my high school and, got my first job as a salesman,working hard all day and night,no one there to lend a helping hand,Daddy told me not to worry and,said that I should go on step by step,what can I say now,what can I do now,those were the days of my past Then one day I settled down with the only one I really love,gona small family with two kids that is what I’m always hoping for,but I still remember having fun with all my friends when I was young,I miss my hometown I miss my old friends,those were the days of my past,I miss my hometown I miss my old friends,when will I see them again''',
        "We have taught at this school for a long time.",
        "What time it is now?", '''Module 4 
       Healthy food''',
        "Some people make your laugh a little louder, your smile a little brighter and your life a little better.",
        "firends",
        "friends",
        '''A fly comes and sits on the end of the man's nose''',
        '''Englishhhh''',
        "Whats are your names?",
        "The monkey is very angry.",
        '''she hasn't sent the email yet.''',
        '''You make some noises,when you are hungry.''',
        "We have taught at this school for a long time.",
        "I don understand you.",
        "Do a survey",
        "Some people make your laugh a little louder, your smile a little brighter and your life a little better.",
        "Now match these words.",
        "drink",
        "favorite drink",
        "favourite food and drink",
        "Can you give more(更多) advice?.",
        "Can you give more(更多) advie?.",
        "How many parts(部分） are there?",
        "be a happy and healthy student",
        "Noodles and rice are good for our healthy. ",
        "Label the pictures with the words and expression from the box.",
        "What fod are good for your eyes?",
        "Eat well, stay heathly , and don’t  get fat!",
        "Let enjoy a song about food.",
        """Eat the right food and be healthy
        How to eat well and stay healthy 
        What’re unhealthy food """,
        """Eat the right food and be healthy
        How to eat well and stay healthy 
          What’re unhealthy food """,
        "bread   candies   cola   fish   hamburger  ice cream   noodles   rice   sugar",
        """How many parts(部分） are there?
        What’s the main idea（主要观点） of each part?""",
        "3. Drink ________________________, not _____.",
        "I will to go to diner.",
    ]
    for text in all_text_1:
        all_data.append([str(text), str(text)])

    for t in range(10000):
        for tmp_data in executor.map(get_tag_parser_all, all_data):
            print(tmp_data)
        print("==============================")
