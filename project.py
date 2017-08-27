from flask import Flask,render_template, request, jsonify, redirect, Response
import csv
from MAIN import *
from main2 import *
from method1 import *
import method1 as tss
from Textual_Similarity_System import TSS

app = Flask(__name__)
Semantic_Similarity = TSS()
my_answers=[]
answerscores=[]

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    #return render_template('fawad.html')#Student, admin
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'fawad' and request.form['password'] == 'fawad':
            return render_template('Student.html')
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            print "invalid"
        else:
            return render_template('admin.html')
    return render_template('login.html', error=error)

@app.route('/form',methods=['GET', 'POST'] )
def form():
    return render_template('form.html')

@app.route('/register',methods=['GET', 'POST'] )
def reg():
    return render_template('register.html')

@app.route('/admin',methods=['GET', 'POST'] )
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'fawad' and request.form['password'] == 'fawad':
            return render_template('Student.html')
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            print "invalid"
        else:
            return render_template('admin.html')
    return render_template('login.html', error=error)

@app.route('/add',methods=['POST'])
def login2():
    return render_template('login.html')

@app.route("/addQuestion",methods=['POST'])
def addMachine():
    try:
        json_data = request.json['info']
        ques1  = json_data['q1']
        ques2 = json_data['q2']
        score11= semantic_similarity(ques1,ques2,False)
        print score11
        score22=interp(score11, [0, 1], [0, 5])
        p = Get_POS_TAG(ques1)
        q = Get_POS_TAG(ques2)
        n, v, adj, a, num = make_lists(p)
        n1, v1, adj1, a1, num1 = make_lists(q)
        path2 = r'/home/fawad/Desktop/project/static/data/age2.csv'
        print 'fawad'
        with open(path2, 'w') as csvfile:
            fieldnames = ['name', 'parent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'name': 'Noun', 'parent': 'Sentence'}, )
            writer.writerow({'name': 'Sentence', 'parent': 'null'}, )
            writer.writerow({'name': 'Adjective', 'parent': 'Sentence'})
            writer.writerow({'name': 'Verb', 'parent': 'Sentence'})
            writer.writerow({'name': 'Adverb', 'parent': 'Sentence'})
            for i in n:
                writer.writerow({'name': i, 'parent': 'Noun'})
            for i in v:
                writer.writerow({'name': i, 'parent': 'Verb'})
            for i in adj:
                writer.writerow({'name': i, 'parent': 'Adjective'})
            for i in a:
                writer.writerow({'name': i, 'parent': 'Adverb'})
            for i in n1:
                writer.writerow({'name': i, 'parent': 'Noun'})
            for i in v1:
                writer.writerow({'name': i, 'parent': 'Verb'})
            for i in adj1:
                writer.writerow({'name': i, 'parent': 'Adjective'})
            for i in a1:
                writer.writerow({'name': i, 'parent': 'Adverb'})
        print 'json data : ', json_data
        return jsonify(score=score22, message='inserted successfully')

    except Exception,e:
        return jsonify(status='OK', message='insertion failed')

@app.route('/display_Tree', methods=['GET', 'POST'])
def display_Tree():
    return render_template('checktree.html')

@app.route('/Student')
def Student_page():
    return render_template('Student.html')

@app.route('/Teacher')
def Teacher_page():
    return render_template('admin.html')

@app.route('/addCA')
def CA_subj():
    return render_template('ca.html')

@app.route('/addTeacher',methods=['GET','POST'])
def Teacher():
    try:
        json_data=request.json['info']
        ques1 = json_data['q1']
        ans1  = json_data['a1']
        marks1 = json_data['m1']
        ques2 = json_data['q2']
        ans2  = json_data['a2']
        marks2 = json_data['m2']
        ques3 = json_data['q3']
        ans3  = json_data['a3']
        marks3 = json_data['m3']
        ques4 = json_data['q4']
        ans4  = json_data['a4']
        marks4 = json_data['m4']
        questions= []
        questions.append(ques1)
        questions.append(ques2)
        questions.append(ques3)
        questions.append(ques4)
        my_answers.append(ques1)
        my_answers.append(ques2)
        my_answers.append(ques3)
        my_answers.append(ques4)
        answers=[]
        answers.append(ans1)
        answers.append(ans2)
        answers.append(ans3)
        answers.append(ans4)
        marks=[]
        marks.append(int(marks1))
        marks.append(int(marks2))
        marks.append(int(marks3))
        marks.append(int(marks4))
        exam_name = "Final_Exam"
        Semantic_Similarity.Create_Paper(questions, answers, marks, exam_name)
       # path2 = r'/home/fawad/Downloads/startbootstrap-grayscale-gh-pages/static/data/teacher.csv'
       # with open(path2, 'w') as csvfile:
         #   fieldnames = ['Answer']
          #  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
          #  writer.writeheader()
          #  writer.writerow({'Answer': ques1})
           # writer.writerow({'Answer': ques2})
          #  writer.writerow({'Answer': ques3})
          #  writer.writerow({'Answer': ques4})
            #writer.writerow({'Answer': ques5})
            #writer.writerow({'Answer': ques6})

        print 'json data : ', json_data
        return jsonify(message='inserted successfully')
    except Exception,e:
        return jsonify(status='OK', message='insertion failed')

@app.route('/display_Answer', methods=['GET', 'POST'])
def display_Answer():
    return render_template('AttemptPaper.html', my_answers=my_answers)

@app.route('/display_Result', methods=['GET', 'POST'])
def display_Result():
    return render_template('Result.html', my_answers=my_answers,answerscores=answerscores)

@app.route('/display_ResultAdmin', methods=['GET', 'POST'])
def display_ResultAdmin():
    return render_template('ResultAdmin.html', my_answers=my_answers,answerscores=answerscores)

@app.route('/display_Paper', methods=['GET', 'POST'])
def display_Paper():
    return render_template('ViewPaper.html', my_answers=my_answers,answerscores=answerscores)

@app.route('/addStudent',methods=['GET','POST'])
def Student():
    try:
        json_data=request.json['info']
        ques1 = json_data['q1']
        ques2 = json_data['q2']
        ques3 = json_data['q3']
        ques4 = json_data['q4']
        answers=[]
        answers.append(ques1)
        answers.append(ques2)
        answers.append(ques3)
        answers.append(ques4)
        exam_name = "Final_Exam"
        exam_name += ".csv"
        print "fawad"
        path="/home/fawad/Desktop/project/Final_Exam.csv"
        q_id=[]
        questions=[]
        answerofteacher=[]
        score=[]
        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                q_id.append(row[0])
                questions.append(row[1])
                answerofteacher.append(row[2])
                score.append(float(row[3]))
        print questions
        question1=questions[0]
        question2=questions[1]
        question3=questions[2]
        question4=questions[3]

        obtained_marks = Semantic_Similarity.Evaluate_Paper(questions, answers, exam_name, 1)
        print "+++++++++++", obtained_marks
        score1_ans= obtained_marks[0]
        score2_ans = obtained_marks[1]
        score3_ans = obtained_marks[2]
        score4_ans = obtained_marks[3]
        answerscores.append(score1_ans)
        answerscores.append(score2_ans)
        answerscores.append(score3_ans)
        answerscores.append(score4_ans)
        return jsonify(message='yes')
        #return jsonify(score1=score1_ans,score2=score2_ans,score3=score3_ans,score4=score4_ans,message='inserted successfully')
    except Exception,e:
        return jsonify(status='OK', message='insertion failed')


if __name__ == "__main__":
    app.run(host='127.0.0.1')
