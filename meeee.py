from flask import Flask,render_template, request, jsonify, redirect, Response
import csv
from MAIN import *
from main2 import *
from method1 import *
import method1 as tss
from Textual_Similarity_System import TSS
import json
#import ONH
app = Flask(__name__)
Semantic_Similarity = TSS()
my_answers=[]
answerscores=[]

marks=[]

arr=[]
arr2=[]
marks2=[]
counter=0

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'fawad' and request.form['password'] == 'fawad':
            return render_template('Student.html')
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            print "invalid"
        else:
            return render_template('admin.html')
    return render_template('login.html', error=error)#setpaper3

@app.route('/form',methods=['GET', 'POST'] )
def form():
    return render_template('form.html')

@app.route('/register',methods=['GET', 'POST'] )
def reg():
    return render_template('register.html')

@app.route('/admin',methods=['GET', 'POST'] )
def admin():
    return render_template('admin.html', methods = ["Method1", "Method2","Method3"])

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
        my_method = request.json['method']
        print "^^^^^^^^^^^^", my_method
        ques1  = json_data['q1']
        ques2 = json_data['q2']
        score11= semantic_similarity(ques1,ques2,False)
        print score11
        score22=interp(score11, [0, 1], [0, 5])
        p = Get_POS_TAG(ques1)
        q = Get_POS_TAG(ques2)
        n, v, adj, a, num = make_lists(p)
        n1, v1, adj1, a1, num1 = make_lists(q)

        path2 = r'/home/fawad/Desktop/fawadkhan/project/static/data/age2.csv'
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
        #x=ONH.Calculate_Similarity(ques1,ques2)
        # print "x = "+x
        all_methods = ["POS","One Hot Encodding","Bag of words","Hybrid"]
        m = all_methods.index(my_method)+1
        print "m : ", m, ", type : ", type(m)
        o=Semantic_Similarity.Calculate_Similarity(ques1,ques2,5,m)
        print "o = ",o
        x=format(round(o,2))
        return jsonify(score=x, message='inserted successfully')

    except Exception,e:
        print e.message
        return jsonify(status='OK', message='insertion failed')

@app.route('/display_Tree', methods=['GET', 'POST'])
def display_Tree():
    return render_template('checktree.html')

@app.route('/Student')
def Student_page():
    return render_template('Student.html',my_answers=my_answers,answerscores=answerscores)

@app.route('/Teacher')
def Teacher_page():
    return render_template('admin.html',my_answers=my_answers,answerscores=answerscores)

@app.route('/addCA')
def CA_subj():
    return render_template('ca.html')

@app.route('/AboutUs', methods=['GET', 'POST'])
def AboutUS():
    return render_template('about.html')

@app.route('/AboutUs2', methods=['GET', 'POST'])
def AboutUS2():
    return render_template('about2.html')

@app.route('/display_Answer', methods=['GET', 'POST'])
def display_Answer():
    return render_template('AttemptPaper.html', my_answers=my_answers)

@app.route('/display_Result', methods=['GET', 'POST'])
def display_Result():
    print "marks2= ",marks2
    return render_template('Result.html', my_answers=my_answers,answerscores=answerscores,marks=marks,marks2=marks2,counter=counter,totalscore=totalscore,obtained_marks=obtained_marks,scores=scores,answersnew=answersnew,answerscores2=answerscores2)

@app.route('/display_ResultAdmin', methods=['GET', 'POST'])
def display_ResultAdmin():
    return render_template('ResultAdmin.html', my_answers=my_answers,answerscores=answerscores,marks=marks)

@app.route('/display_Paper', methods=['GET', 'POST'])
def display_Paper():
    return render_template('ViewPaper.html', my_answers=my_answers,answerscores=answerscores,questions=questions,counter=counter,arr=arr,arr3=arr3)
arr3=[]

@app.route('/setpaper', methods=['GET','POST'])
def setpaper():
    return render_template('setpaper3.html',arr=arr,arr2=arr2,my_answers=my_answers,questions=questions,marks2=marks2)

@app.route('/postValue2' , methods=['GET', 'POST'])
def postValue2():
    try:
        arr = request.json['arr']
        arr2= request.json['arr2']
        global counter
        counter = request.json['counter']
        counter2 = request.json['counter2']
        #marks2=[]
        marks2.append(5)
        marks2.append(5)
        marks2.append(5)
        marks2.append(5)

        print "Array  :", arr
        print "counter : ", counter
        print "Array2  :", arr2
        print "counter2 : ", counter2
        exam_name='MID_TERM'
        my_answers=arr
        Semantic_Similarity.Create_Paper(arr, arr2, marks2, exam_name)
        for i in range(0,counter):
            arr3.append(arr[i])

        q1=arr[0]
        q2=arr[1]
        #arr3.append(q1)
        #arr3.append(q2)
        data = json.loads(arr)
        print "data= ",data['u']
        print "arr3",arr3
        return jsonify(message='yes')
    except Exception,e:
        return jsonify(message='no')

main=0
@app.route('/AttemptPaper', methods=['GET', 'POST'])
def AttemptPaper():
    global main
    if (main==0):
        main=1
        return render_template('AttemptPaper2.html', my_answers=my_answers,counter=counter,answerscores=answerscores,marks=marks,marks2=marks2,arr=arr,questions=questions,arr2=arr2,arr3=arr3,main=main)
        main=1
    else:
        return render_template('noattempt.html')

totalscore=0
scores=0
obtained_marks=[]
questions=[]
answersnew=[]
answerscores2=[]
@app.route('/addStudent3',methods=['GET','POST'])

def Student3():
    global main
    if (main==0):
        try:
            json_data=request.json['info2']
            global totalscore
            global scores
            for i in range(0,counter):
                new_answer='q'+str(i)
                ques11 = json_data[new_answer]
                print ques11
                answersnew.append(ques11)
                totalscore=totalscore+5
            exam_name = "Final_Exam"
            exam_name += ".csv"
            print "fawad"
            path="/home/fawad/Desktop/fawadkhan/project/MID_TERM.csv"
            q_id=[]

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
            obtained_marks = Semantic_Similarity.Evaluate_Paper(questions, answersnew, exam_name, 2)
            print "+++++++++++", obtained_marks

            for i in range(0,counter):
                x=obtained_marks[i]
                x=format(round(x,2))
                answerscores.append(x)
            print "done"
            for i in range(0,counter):
                scores=scores+obtained_marks[i]
            scores = format(round(scores, 2))
            #global main
            #main=0
            return jsonify(message='yes')
        except Exception,e:
            return jsonify(status='OK', message='insertion failed')
    else:
        return render_template('noattempt.html')

@app.route('/Sample')
def Sample():
    return render_template('SamplePaper.html')
m=0
@app.route('/tableresult')
def tableresult():
    return render_template('tableresult.html', my_answers=my_answers,answerscores=answerscores,marks=marks,marks2=marks2,counter=counter,totalscore=totalscore,obtained_marks=obtained_marks,scores=scores,answersnew=answersnew,answerscores2=answerscores2,m=m)

if __name__ == "__main__":
    app.run(host='127.0.0.1')
