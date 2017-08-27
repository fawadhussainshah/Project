from POS_Analyzer import POS_Analyzer
from WordNet import One_Hot_Encoding
from Question_class import Question
from BagOfWords import BagOfWords
from Hybrid import Hybrid
from Google import Google_Word2Vec


import csv
class TSS:

    def __init__(self):
        self.method_1 = POS_Analyzer()
        self.method_2 = One_Hot_Encoding()
        self.method_3 = BagOfWords(1)
        self.method_4 = Hybrid()
#        self.method_5 = Google_Word2Vec()


    def Calculate_Similarity(self, sent1 , sent2 , max_score , option):

        if option == 1:
            score1, tagged_1, tagged_2 = self.method_1.calculate_similarity(sent1, sent2, max_score)
            #return score1 , tagged_1 , tagged_2
            return score1

        elif option == 2:
            score2 = self.method_2.calculate_similarity(sent1, sent2, max_score)
            return score2

        elif option == 3:
            score3= self.method_3.calculate_similarity(sent1, sent2, max_score)
            return score3
        elif option ==4:
            score4= self.method_4.calculate_similarity(sent1,sent2,max_score)
            return score4
      #  elif option ==5:
        #    score5= self.method_5.calculate_similarity(sent1,sent2,max_score)
         #   return score5
        else:
            print "Error.....!!!!  Invalid Option Selected"
            return -1

    def Create_Paper(self , question_list, answer_list , marks_list , paper_name):


        Questions = []
        id = 0 ;
        for question,answer,marks in zip(question_list , answer_list , marks_list):
            id +=1
            q = Question(id ,question , answer , marks)
            Questions.append(q)
        paper_name+=".csv"
        writer = csv.writer(open(paper_name, "wb"))
        for question in Questions:
            line = question.to_comma_seperated_String()
            #print "Writting to File : ",line
            writer.writerow(line.split(","))
        print "create_paper"

    def Evaluate_Paper(self,question_list, answer_list , paper_name , option):
        Questions = []
        #Get All the Questions and Target Answers from the Paper File
        filename =paper_name
        filename+=".csv"
        #path = "/home/fawad/Desktop/project/Final_Exam.csv"
        path = "/home/fawad/Desktop/fawadkhan/project/MID_TERM1 (copy).csv"
        path1=paper_name
        print "marha"
        with open(path1) as f:
            reader = csv.reader(f)
            for row in reader:
                q_id=row[0]
                question=row[1]
                answer=row[2]
                score=float (row[3])
                new_Question = Question(q_id,question,answer,score)
                Questions.append(new_Question)
        marks_list = []
        print score
        print "marha2"
        for question, answer in zip(question_list, answer_list):
            for q in Questions:
                if q.question== question:
                    if option == 1 :
                        #marks,t1,t2 = self.Calculate_Similarity(answer, q.answer, q.score, option)
                        marks= self.Calculate_Similarity(answer, q.answer, q.score, option)
                    elif option ==2 :
                        marks = self.Calculate_Similarity(answer, q.answer, q.score, option)
                    elif option ==3 :
                        marks = self.Calculate_Similarity(answer, q.answer, q.score, option)
                    elif option ==4 :
                        marks = self.Calculate_Similarity(answer, q.answer, q.score, option)
                    marks_list.append(marks)
                    break
        print "evaluate_paper"
        return marks_list

