import gensim
import numpy as np
from scipy import spatial
from numpy import interp
import re
from nltk.corpus import stopwords
from sklearn.metrics import mean_squared_error
from math import sqrt

class Google_Word2Vec:
    def __init__(self):
        self.model = gensim.models.Word2Vec.load_word2vec_format('../../Google/GoogleNews-vectors-negative300.bin.gz',
                                                                 binary=True)

    def Sentence_Vector(self,words1):
        final_vector = 0
        for a in words1:
            try:
                v1 = self.model[a]
            except:
                v1 = np.zeros(300)
            final_vector = np.add(final_vector, v1)
        return (final_vector / len(words1))

    def Preprocess_Sentence(self,sentence):

        # sentence = sentence.replace(",", "'")
        sentence = re.sub('[^ 0-9a-zA-Z]+', ' ', sentence)
        try:
            words = [word.lower() for word in sentence.split() if
                     word not in stopwords.words('english') and len(word) >= 2]
            # nwords=[stemmer.stem(word) for word in words]
            return np.array(words)
        except Exception, e:
            print "++++++++\n+\n++++++ EXCEPTION OCCURED \n\n+++++++\n\n++++++++++++++"
            print "To Convert was :: ", sentence
            print str(e)
            return words


    def calculate_similarity(self, actual_ans, student_ans, max_score):
        teacher = self.Preprocess_Sentence(actual_ans)
        student = self.Preprocess_Sentence(student_ans)

        student_Vec = self.Sentence_Vector(student)
        teacher_Vec= self.Sentence_Vector(teacher)

        sim = [interp(1 - spatial.distance.cosine(student_Vec, teacher_Vec), [0, 1], [0, max_score])]
        score = sim[0]
        return score

    def calculate_rms(self,answers,scores,target_answer , max_score):
        error = []
        predicted = []
        for answer , score in zip (answers , scores):
            x = self.calculate_similarity(target_answer , answer , max_score)
            predicted.append(x)
            error.append(x - score)

        rms = sqrt(mean_squared_error(scores, predicted))

        return rms



