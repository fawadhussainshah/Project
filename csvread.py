import csv
from MAIN import *
import method1 as tss
path=r'/home/fawad/Desktop/project/Final_Exam.csv'
with open(path, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print ', '.join(row)
        h=row
#import csv
print "fawadddddd"
with open(path, 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

print your_list
print h

print your_list[5]
h=your_list[2]
i=your_list[1]
print "i"+i[0]
list1 = [1, 2, 3]
str1 = ''.join(str(e) for e in list1)
print str1
print your_list[1]
m=tss.Calculate_Similarity(h[0],i[0])
print m

