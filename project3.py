from flask import Flask,render_template, request, jsonify, redirect, Response
import csv

from flask import session
from selenium import  webdriver
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
app.secret_key='fawad'
@app.route('/',methods=['GET', 'POST'])
def hello_world():
    error = None
    if request.method == 'POST':
        session['user'] = request.form['username']
        if request.form['username'] == 'fawad' and request.form['password'] == 'fawad':
            return render_template('Student.html')
        if request.form['username'] != 'admin@gmail.com' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            print "invalid"
        else:
            return render_template('admin.html')
    return render_template('login3.html', error=error)#setpaper3
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user', None)
   return render_template('login3.html')

@app.route('/form',methods=['GET', 'POST'] )
def form():
    return render_template('form.html')

@app.route('/register',methods=['GET', 'POST'] )
def reg():
    return render_template('register.html')

@app.route('/admin',methods=['GET', 'POST'] )
def admin():
    if 'user' in session:
        return render_template('admin.html', methods = ["Method1", "Method2","Method3"])
    return render_template('login3.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    session.pop('user',None)
    if request.method == 'POST':
        session['username'] = request.form['username']
        if request.form['username'] == 'fawad' and request.form['password'] == 'fawad':
            return render_template('Student.html')
        if request.form['username'] != 'admin@gmail.com' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            print "invalid"
        else:
            return render_template('admin.html')
    return render_template('login3.html', error=error)

@app.route('/add',methods=['POST'])
def login2():
    return render_template('login3.html')

@app.route("/addQuestion",methods=['POST'])
def addMachine():
    try:
        json_data = request.json['info']
        my_method = request.json['method']
        print "^^^^^^^^^^^^", my_method
        ques1  = json_data['q1']
        ques2 = json_data['q2']
       # score11= semantic_similarity(ques1,ques2,False)
        #print score11
       # score22=interp(score11, [0, 1], [0, 5])
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
        all_methods = ["POS","One Hot Encodding","Bag of words","Hybrid","Google Word2Vec"]
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
    if 'user' in session:
        #0--------------------
        # profile = webdriver.FirefoxProfile()
        # profile.set_preference("browser.cache.disk.enable", False)
        # profile.set_preference("browser.cache.memory.enable", False)
        # profile.set_preference("browser.cache.offline.enable", False)
        # profile.set_preference("network.http.use-cache", False)
        # driver = webdriver.Firefox(profile)

        return render_template('checktree.html')
    return render_template('login3.html')

@app.route('/Student')
def Student_page():
    return render_template('Student.html',my_answers=my_answers,answerscores=answerscores)

@app.route('/Teacher')
def Teacher_page():
    if 'user' in session:
        return render_template('admin.html',my_answers=my_answers,answerscores=answerscores)
    return render_template('login3.html')
@app.route('/addCA')
def CA_subj():
    return render_template('ca.html')

@app.route('/AboutUs', methods=['GET', 'POST'])
def AboutUS():
    if 'user' in session:
        return render_template('about.html')
    return render_template('login3.html')
@app.route('/AboutUs2', methods=['GET', 'POST'])
def AboutUS2():
    if 'user' in session:
        return render_template('about2.html')
    return render_template('login3.html')
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
    #if 'username' in session:
    return render_template('ViewPaper.html', my_answers=my_answers,answerscores=answerscores,questions=questions,counter=counter,arr=arr,arr3=arr3)
    #render_template('login.html')

arr3=[]

@app.route('/setpaper', methods=['GET','POST'])
def setpaper():
    if 'username' in session:
        return render_template('setpaper3.html',arr=arr,arr2=arr2,my_answers=my_answers,questions=questions,marks2=marks2)
    return render_template('login3.html')

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
        global main
        main=1
        return jsonify(message='yes')
    except Exception,e:
        return jsonify(status='OK', message='insertion failed')

@app.route('/Sample')
def Sample():
    if 'user' in session:
        return render_template('SamplePaper.html')
    return render_template('login3.html')
m=0
@app.route('/tableresult')
def tableresult():
    return render_template('tableresult.html', my_answers=my_answers,answerscores=answerscores,marks=marks,marks2=marks2,counter=counter,totalscore=totalscore,obtained_marks=obtained_marks,scores=scores,answersnew=answersnew,answerscores2=answerscores2,m=m)
error=None
@app.route('/setpaper2', methods=['GET','POST'])
def setpaper2():
    if 'user' in session:
        return render_template('uploadfile.html',arr=arr,arr2=arr2,my_answers=my_answers,questions=questions,marks2=marks2)
    return render_template('login3.html')

import os
import csv
UPLOAD_FOLDER = '/home/fawad/Desktop/fawadkhan/project'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
counter2=0
scores2=0
answerscores2=[]
answerscores3=[]
avg=0
min=0
max=0
score=0
m=0
p='fawad'
anothercounter=[]
@app.route('/uploader', methods=['GET','POST'])
def upload_file():
    error=None
    #my_method = request.json['method']
    if request.method == 'POST' and 'file' in request.files:
        f = request.files['file']
       # f.save(secure_filename(f.filename))
        if f and allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            global p
            p=UPLOAD_FOLDER+"/"+f.filename
            checking_format_csv=check_format(f.filename, 2)
            print "format is =", checking_format_csv
            if checking_format_csv==False:
                error='File uploaded is not in correct order'
                return render_template('uploadfile.html', error=error)
            print "p= ",p
            q_id1=[]
            questions1=[]
            answerofteacher1=[]
            score1=[]
            global counter2
            counter2=0
            global score
            with open(p) as f:
                reader = csv.reader(f)
                for row in reader:
                    #q_id1.append(row[0])
                    #while counter2<5:
                    if counter2==0:
                            #questions1.append(row[0])
                        questions1=row[0]
                        score=row[1]
                        man=score
                    else:
                        answerofteacher1.append(row[0])
                        #score1.append(float(row[3]))
                   # if counter2==51:
                    #    break
                    counter2=counter2+1
            print "counter2 =",counter2
            print "score = ",score
            print questions1
            print answerofteacher1
            exam_name="MIDTERM1"
            global avg
            avg=0
            sum1=0
            #############33
          #  my_method = request.json['method']
          #  print "^^^^^^^^^^^^", my_method
          #  all_methods = ["POS", "One Hot Encodding", "Bag of words", "Hybrid"]
          #  dropdown= all_methods.index(my_method) + 1
         #   print "m : ", dropdown, ", type : ", type(dropdown)
            ###############

            #print "^^^^^^^^^^^^", my_method
            #all_methods = ["One Hot Encodding", "Bag of words", "Hybrid"]
            #dropdown = all_methods.index(my_method) + 1
            #print "m : ", dropdown, ", type : ", type(dropdown)
            #########
            for i in range(0,counter2-1):
                g=answerofteacher1[i]
                print "calculating score = ",i+1
                f=Semantic_Similarity.Calculate_Similarity(questions1, g, score, 3)#m=3
                sum1=sum1+f
                obtained_marks.append(f)

            global max
            max=0
            max=maximum(obtained_marks)
            max=float(max)
            max = format(round(max, 2))
            global min
            min=0
            min=minimum(obtained_marks)
            min=float(min)
            min = format(round(min, 2))
            #obtained_marks = Semantic_Similarity.Evaluate_Paper(questions1, answerofteacher1, p, 2)
            print "+++++++++++", obtained_marks
            global scores2
            scores2=0
            answerscores3=obtained_marks
            for i in range(0,counter2-1):
                scores2=scores2+obtained_marks[i]
            scores2 = format(round(scores2, 2))
            print "scores2 = ",scores2
            global answerscores2
            answerscores2=[]
            global m
            m=(counter2-1)*int(score)
            print "m = ",m
            for i in range(0,counter2-1):
                x=obtained_marks[i]
                x=format(round(x,2))
                answerscores2.append(x)
                answerscores3.append(x)
            l=counter2-1


            avg=sum1/l
            avg=format(round(avg,2))
            global anothercounter
            anothercounter=[]
            for i in range(0,counter2):
                h=i+1
                anothercounter.append(h)
            print "avg=",avg
            global checker
            checker=1
            return render_template('tableresult2.html',counter2=counter2,scores2=scores2,answerscores2=answerscores2,answerscores3=answerscores3,score=score,m=m,avg=avg,min=min,max=max,anothercounter=anothercounter)
        error='The file is not in csv format. Please upload a file in csv format'
        return render_template('uploadfile.html',error=error)
@app.route('/tableresult2',methods=['GET', 'POST'])
def tableresult2():
    if 'user' in session:
        if checker==1:
            return render_template('tableresult2.html', counter2=counter2, scores2=scores2, answerscores2=answerscores2,answerscores3=answerscores3, score=score, m=m, avg=avg, min=min, max=max,anothercounter=anothercounter)
        else:
            error="Please upload a file first"
            return render_template('uploadfile.html', error=error)
    return render_template('login3.html')

checker=0

@app.route('/ViewPaper2', methods=['GET','POST'])
def ViewPaper2():
    if 'user' in session:
        global checker
        if checker==1:
            global p
            counter2=0
            answerofteacher1=[]
            with open(p) as f:
                reader = csv.reader(f)
                for row in reader:
                    # q_id1.append(row[0])
                    # while counter2<5:
                    if counter2 == 0:
                        # questions1.append(row[0])
                        questions1 = row[0]
                        score = row[1]
                        man = score
                    else:
                        answerofteacher1.append(row[0])
                        # score1.append(float(row[3]))
                        # if counter2==51:
                    #    break
                    counter2 = counter2 + 1
        else:
            error="Please first upload the Paper"
            return render_template('uploadfile.html',error=error)
        return render_template('ViewPaper2.html',counter2=counter2,answerofteacher1=answerofteacher1,anothercounter=anothercounter,score=score,answerscores2=answerscores2)
    return render_template('login3.html')
questions1='mmm'
@app.route('/ViewQuestionPaper', methods=['GET','POST'])
def ViewPaper3():
    if 'user' in session:
        global checker
        if checker==1:
            global p
            counter2=0
            answerofteacher1=[]
            global questions1
            with open(p) as f:
                reader = csv.reader(f)
                for row in reader:
                    # q_id1.append(row[0])
                    # while counter2<5:
                    if counter2 == 0:
                        # questions1.append(row[0])
                        questions1 = row[0]
                        score = row[1]
                        man = score
                    else:
                        answerofteacher1.append(row[0])
                        # score1.append(float(row[3]))
                        # if counter2==51:
                    #    break
                    counter2 = counter2 + 1
        else:
            error="Please first upload the Paper"
            return render_template('uploadfile.html',error=error)
        global counter3
        counter3=1
        return render_template('ViewPaper3.html',counter3=counter3,answerofteacher1=answerofteacher1,anothercounter=anothercounter,score=score,answerscores2=answerscores2,questions1=questions1)
    return render_template('login3.html')
counter3=1
def minimum(list):
    min = list[0]
    for elm in list[1:]:
        if elm < min:
            min = elm
    return min


def maximum(list):
    max = list[0]
    for elm in list[1:]:
        if elm > max:
            max = elm
    return max


def check_format(filename, total_columns):
    column_that_should_not_exist = total_columns

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        i = 0
        Format = False
        for row in reader:
            try:
                row[column_that_should_not_exist]
                Format = False
                return Format
            except:
                Format = True
        return Format

if __name__ == "__main__":
    app.run(host='127.0.0.1')
