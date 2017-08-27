from collections import defaultdict
from numpy import interp
import re
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from sklearn.metrics import mean_squared_error
from math import sqrt

class Hybrid:

    def get_tokens(self,sentence):

        string = sentence.lower()
        temp = re.split("\W", string)
        tokens = []
        for i in temp:
            if len(i) > 2:
                if i not in stopwords.words('english') :
                    tokens.append(i)
        return tokens

    def get_all_synonyms(self,tokens):
        temp = []
        for i in tokens:
            for synset in wn.synsets(i):
                for syn in synset.lemma_names():
                    #print "------------",syn
                    temp.append(syn)
                #print "======================================"
        return list(set(temp))

    def make_dictionary(self,tokens):
        # print "----------"
        d_dict = defaultdict(lambda: 0)
        for i in tokens:
            if i not in stopwords.words('english'):
            # print i
                d_dict[i] += 1
        # print len(d_dict)
        return d_dict

    def find_probability(self , word, teacher_d, total_count):

        val = teacher_d[word]
        if val == 0 :
            synms = self.get_all_synonyms([word])
            max = 0
            for i in synms:
                val = teacher_d[i];
                if val > max:
                    max = val
            val = max
        val *= 1.0
        prob = val / total_count

        #print "Probability = ",prob,"Total = ",total,"value = ",val
        return prob

    def calculate_similarity(self, actual_ans, student_ans, max_score):

        tokens_1 = self.get_tokens(actual_ans)
        tokens_2 = self.get_tokens(student_ans)

        synonyms_1 = self.get_all_synonyms(tokens_1);
        synonyms_2 = self.get_all_synonyms(tokens_2);

        teacher_dict = self.make_dictionary(synonyms_1)
        student_dict = self.make_dictionary(tokens_2)

        similarity = 0
        for key, val in student_dict.iteritems():
            p = self.find_probability(key, teacher_dict, len(tokens_1))
            similarity += p
            #print similarity

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