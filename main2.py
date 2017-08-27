from __future__ import division
import numpy as np
import pandas as pd
#import tools as t
#from nltk.corpus import stopwords
from nltk.stem.porter import *
import tools as t
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import sys
import math

stopwords=t.read_txt_file("english.stop")

from nltk.stem import WordNetLemmatizer
from numpy import interp

import math
def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

from itertools import product

def Word_2_Vec(sent1, sent2):
    words_1 = nltk.word_tokenize(sent1.lower())
    words_2 = nltk.word_tokenize(sent2.lower())

    #words_1 = [PorterStemmer().stem_word(word) for word in words_1]
    #words_2 = [PorterStemmer().stem_word(word) for word in words_2]

    wnl = WordNetLemmatizer()

    words_1 = [wnl.lemmatize(word) for word in words_1 if word not in stopwords]
    words_2 = [wnl.lemmatize(word) for word in words_2 if word not in stopwords]

    #print words_1
    #print words_2

    all_items = set(words_1).union(set(words_2))
    #print "-----------------------------All Items-----------------------------------"
    #print all_items

    v1 = []
    v2 = []

    for word in all_items:
        if word not in words_1:
            try:
                s1 = wn.synsets(word)
                ss1 = s1[0]
            except IndexError:
                #print "error: ", word
                pass

            score = []
            for w in all_items:
                    try:
                        s2 = wn.synsets(w)
                        ss2 = s2[0]
                        sims = []
                        for sense1, sense2 in product(s1, s2):
                            d = wn.wup_similarity(sense1, sense2)
                            sims.append(d)
                        if len(sims) > 0:
                            if min(sims) != None:
                                score.append(min(sims))

                    except IndexError:
                        #print "error: ", w
                        pass
                    except UnboundLocalError:
                        pass
            #print word, " : ", score
            if len(score) > 1:
                if sorted(score)[-2] > 0.5:
                    v1.append(sorted(score)[-2])
                else:
                    v1.append(0)
            else:
                v1.append(0)

        else:
            v1.append(1)

    for word in all_items:
        if word not in words_2:
            try:
                s1 = wn.synsets(word)
                ss1 = s1[0]
            except IndexError:
                #print "error: ", word
                pass
            score = []
            for w in all_items:
                    try:
                        s2 = wn.synsets(w)
                        ss2 = s2[0]
                        sims = []
                        for sense1, sense2 in product(s1, s2):
                            d = wn.wup_similarity(sense1, sense2)
                            sims.append(d)
                        if len(sims) > 0:
                            if min(sims) != None:
                                score.append(min(sims))

                    except IndexError:
                        #print "error: ", w
                        pass
                    except UnboundLocalError:
                        pass
            #print word, " : ", score
            if len(score) > 1:
                if sorted(score)[-2] > 0.5:
                    v2.append(sorted(score)[-2])
                else:
                    v2.append(0)
            else:
                v2.append(0)

        else:
            v2.append(1)

    #print "-------------------Vector 1----------------------"
    #print v1
    #print "-------------------Vector 2----------------------"
    #print v2
    #print "Cosine Similarity: ", cosine_similarity(v1, v2)
    score = interp(cosine_similarity(v1, v2), [0,1], [0,5])
    return score

sent1 = "Amgen shares gained 93 cents, or 1.45 percent, to $65.05 in afternoon trading on Nasdaq."
sent2 = "Shares of Allergan were up 14 cents at $78.40 in late trading on the New York Stock Exchange."

#print Word_2_Vec(sent1, sent2)