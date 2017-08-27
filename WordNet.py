from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from numpy import interp
import math
from itertools import product
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt

class One_Hot_Encoding:
    def __init__(self):
        self.score=0

    def tokenize(self, sent):
        words = nltk.word_tokenize(sent.lower())

        # words_1 = [PorterStemmer().stem_word(word) for word in words_1]
        # words_2 = [PorterStemmer().stem_word(word) for word in words_2]

        wnl = WordNetLemmatizer()

        words = [wnl.lemmatize(word) for word in words if word not in stopwords.words('english')]

        return words

    def union(self, words_1, words_2):
        all_items = set(words_1).union(set(words_2))
        return all_items

    def vectorize(self, all_items, words):
        vector = []
        for word in all_items:
            if word not in words:
                try:
                    s1 = wn.synsets(word)
                    ss1 = s1[0]
                except IndexError:
                    # print "error: ", word
                    pass

                score = []
                for w in all_items:
                    try:
                        s2 = wn.synsets(w)
                        ss2 = s2[0]
                        sims = []
                        for sense1, sense2 in product(s1, s2):
                            d = wn.path_similarity(sense1, sense2)
                            sims.append(d)
                        if len(sims) > 0:
                            if min(sims) != None:
                                score.append(min(sims))

                    except IndexError:
                        # print "error: ", w
                        pass
                    except UnboundLocalError:
                        pass
                # print word, " : ", score
                if len(score) > 1:
                    vector.append(sorted(score)[-2])
                else:
                    vector.append(0)

            else:
                vector.append(1)
        return vector

    def cosine_similarity(self, v1, v2):
        "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i];
            y = v2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        return sumxy / math.sqrt(sumxx * sumyy)

    def compute_score(self, v1, v2, max_marks):
        score = interp(self.cosine_similarity(v1, v2), [0, 1], [0, max_marks])
        return score

    def calculate_similarity(self, sent1, sent2, max_marks):
        words_1 = self.tokenize(sent1)
        words_2 = self.tokenize(sent2)
        all_items = self.union(words_1, words_2)
        v1 = self.vectorize(all_items, words_2)
        v2 = self.vectorize(all_items, words_1)
        score = self.compute_score(v1, v2, max_marks)
        return score

    def rms_ca(self,answers , scores , target_answer , max_score):

        error = []
        predicted = []
        count = 0
        for answer , score in zip (answers , scores):
            count+=1
            print count
            x = self.calculate_similarity(target_answer , answer , max_score)
            predicted.append(x)
            error.append(x - score)

        rms = sqrt(mean_squared_error(scores, predicted))
        plt.scatter([i for i in range(len(error))], error)
        plt.suptitle('One Hot Encoding ', fontsize=20)
        plt.show()
        return rms