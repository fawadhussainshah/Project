import numpy as np

import math
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.corpus import wordnet as wn

from nltk.tag import pos_tag, map_tag
from numpy import interp
import tools as t
stopwords=t.read_txt_file("english.stop")
def Preprocess_Sentence(sentence):
    # sentence = sentence.replace(",", "'")
    stemmer = PorterStemmer()
    sentence = re.sub('[^ 0-9a-zA-Z]+', ' ', sentence)
    try:
        words = [word.lower() for word in sentence.split() if word not in stopwords and len(word) >= 2]
        # nwords=[stemmer.stem(word) for word in words]
        return np.array(words)
    except Exception, e:
        print "++++++++\n+\n++++++ EXCEPTION OCCURED \n\n+++++++\n\n++++++++++++++"
        print "To Convert was :: ", sentence
        print str(e)
        return words


def Get_POS_TAG(s1):
    W1 = []
    # print "POS Tagging of : ",s1
    wrds = Preprocess_Sentence(s1)
    # print "After Preprocessing : ",wrds
    Tagged_words1 = pos_tag(wrds)
    # print "Tagged Words are :",Tagged_words1
    simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in Tagged_words1]
    return simplifiedTags


def make_lists(sentence):
    ADJ = []
    ADP = []
    ADV = []
    CONJ = []
    DET = []
    NOUN = []
    NUM = []
    PRON = []
    PRT = []
    VERB = []
    for i in sentence:
        if len(i) == 0:
            continue
        # print i
        if i[1] == "ADJ":
            ADJ.append(i[0])

        elif i[1] == "ADP":
            ADP.append(i[0])

        elif i[1] == "ADV":
            ADV.append(i[0])

        elif i[1] == "CONJ":
            CONJ.append(i[0])

        elif i[1] == "DET":
            DET.append(i[0])

        elif i[1] == "NOUN":
            NOUN.append(i[0])

        elif i[1] == "NUM":
            NUM.append(i[0])

        elif i[1] == "PRON":
            PRON.append(i[0])

        elif i[1] == "PRT":
            PRT.append(i[0])

        elif i[1] == "VERB":
            VERB.append(i[0])

    # return ADJ,ADP,ADV,CONJ,DET,NOUN,NUM,PRON,PRT,VERB
    return NOUN, VERB, ADJ, ADV, NUM


def POS_to_List(pos):
    # print "POS TO LIST CALLED with argument length : ",len(pos),type(pos)
    l = []
    for i in pos:
        l.append(i[0])
    return l


def get_best_synset_pair(word_1, word_2):
    """
    Choose the pair with highest path similarity among all pairs.
    Mimics pattern-seeking behavior of humans.
    """
    max_sim = -1.0
    synsets_1 = wn.synsets(word_1)
    synsets_2 = wn.synsets(word_2)
    if len(synsets_1) == 0 or len(synsets_2) == 0:
        # print "Returning None,None for ",word_1,word_2
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
                sim = wn.path_similarity(synset_1, synset_2)
                if sim > max_sim:
                    max_sim = sim
                    best_pair = synset_1, synset_2
        return best_pair


def sigmoid(x):
    try:
        return 1 / (1 + math.exp(-x))
    except:
        print "Sigmoid Error for X = ", x


def word_similarity(w1, w2):
    # print "======================= " , w1 , w2
    # print "Best pairs for : ",w1,w2
    bw1, bw2 = get_best_synset_pair(w1, w2)

    # print "calculating word similarity for ", bw1," and ",bw2

    if (bw1 is None) or (bw2 is None):
        return 0
    sim = bw1.wup_similarity(bw2)
    # if sim > 0.75:
    #    sim=1
    # print "Word Similarity = ",sim
    if sim is None:
        print "Word Similarity : NONE Error :words were :", w1[0], w2[0], "and ", w1, w2, "\n\n"
    return sim


def list_similarity(list1, list2):
    list1 = np.unique(list1)
    list2 = np.unique(list2)

    # print "Unique",list1,list2,"\n"
    if len(list1) == 0 or len(list2) == 0:
        return 0
    if len(list1) == len(list2):
        if (list1 == list2).all():
            return 1
    total = 0;

    # print "\n===================\nList Similarity betweend\n",list1,"\nand\n",list2
    sim = []
    for i in list1:
        max_sim = 0
        for j in list2:
            temp = word_similarity(i, j);
            # print "\t ",i," - ",j," = ",temp
            if temp > max_sim:
                max_sim = temp;
        # if max_sim > 0.7 :
        #    max_sim=1
        sim.append(max_sim)
        # print "Max similarity = ",max_sim
        total += max_sim;
    # print "Similarity list = ",sim
    # print "Average = ",np.average(sim)
    # avg=total/ max( len(list1),len(list2) )
    similarity = np.average(sim)
    # print "Similarity Score = ",similarity,"\n============================"
    return similarity


def Calculate_Similarity(sent_1, sent_2):  # It takes SENTENCE AS INPUT

    words_1 = Get_POS_TAG(sent_1)
    words_2 = Get_POS_TAG(sent_2)
    x1 = make_lists(words_1)
    x2 = make_lists(words_2)

    slist = []
    empty_count = 0
    count = 0
    for i, j in zip(x1, x2):
        count += 1
        if len(i) <= 0 or len(j) <= 0:
            empty_count += 1
            continue
        list_sim = list_similarity(i, j)
        if count == 2:  # For Verb List
            list_sim = list_sim * 2
        slist.append(list_sim)
    similarity = np.sum(slist) / (float(len(x1)) - empty_count)
    # print "Similarity List = ",slist,"Similarity Score = ",similarity,"Empty = ",empty_count
    similarity = (interp(similarity, [0, 1], [0, 5]))
    #return similarity, words_1, words_2
    return similarity
    # return np.average(slist)# , weights=[0.3 , 0.4 , 0.1 , 0.1 , 0.1])

#print Calculate_Similarity("fawad is here","fawad is not here")
#print Calculate_Similarity(s1, s2)
#ques1="Amgen shares gained 93 cents, or 1.45 percent, to $65.05 in afternoon trading on Nasdaq."
#p = Get_POS_TAG(ques1)
#n, v, adj, a, num = make_lists(p)
#print n
#print v
#print adj
#print a
#print num
#import csv
#with open('age3.csv', 'w') as fp:
    #a = csv.writer()
    #for i in n:
       # i += ": Noun"
       # a.writerow(i)