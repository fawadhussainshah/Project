



class Question:
    def __init__(self,id , question , answer  , score):
        self.id = id
        self.question = question
        self.answer = answer
        self.score = score
    def to_comma_seperated_String(self):
        str = ""
        str += self.id.__str__()
        str += ','
        str += self.question
        str += ','
        str += self.answer
        str += ','
        str += self.score.__str__()
        str += ','

        return str
