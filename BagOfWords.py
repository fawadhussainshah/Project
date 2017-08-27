from collections import defaultdict
from numpy import interp
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt


class BagOfWords:

    def __init__(self, ngrams):
        self.ngrams = ngrams

    def get_ngrams(self,sentence):

        n = self.ngrams
        vectorizer = CountVectorizer(ngram_range=(1, n), token_pattern=r'\b\w+\b', min_df=1)
        analyze = vectorizer.build_analyzer()
        #print sentence
        #exit()
        ngrams = analyze(sentence)
        return  ngrams

    def get_tokens(self,sentence):

        string = sentence.lower()
        temp = re.split("\W", string)
        tokens = []
        for i in temp:
            if (len(i) > 2):
                if i not in stopwords.words('english') :
                    tokens.append(i)
        return tokens

    def make_dictionary(self,tokens):
        # print "----------"
        d_dict = defaultdict(lambda: 0)
        for i in tokens:
            if i not in stopwords.words('english'):
            # print i
                d_dict[i] += 1
        # print len(d_dict)
        return d_dict

    def find_probability(self , word, teacher_d, total):

        total_words = len(teacher_d)
        val = teacher_d[word]

        val = val * 1.0
        prob = val / total_words

        #print "Probability = ",prob,"Total = ",total,"value = ",val
        return prob

    def calculate_similarity(self, actual_ans, student_ans, max_score):

        tokens_1 = self.get_ngrams(actual_ans)
        tokens_2 = self.get_ngrams(student_ans)

        teacher_dict = self.make_dictionary(tokens_1)
        student_dict = self.make_dictionary(tokens_2)

        #print "Total Words  = ", len(teacher_dict)

        similarity = 0
        for key, val in student_dict.iteritems():
            p = self.find_probability(key, teacher_dict, len(tokens_1))
            similarity += p


        return interp(similarity, [0.0, 1.0], [0.0, float(max_score)])


    def calculate_rms(self,answers,scores,target_answer , max_score):
        error = []
        predicted = []
        for answer , score in zip (answers , scores):
            x = self.calculate_similarity(target_answer , answer , max_score)
            predicted.append(x)
            error.append(x - score)

        rms = sqrt(mean_squared_error(scores, predicted))

        return rms


