#-*- coding:utf-8 -*-
import sys
import psycopg2
import numpy as np
from sklearn.externals import joblib
import cProfile

pr = cProfile.Profile()
pr.enable()

#click = int(sys.argv[1])
#path = str(sys.argv[2])
#get_conn = psycopg2.connect(dbname=sys.argv[4],user=sys.argv[5], host=sys.argv[3], password=sys.argv[6])

click = 1
path = u"D:/Develop_code/IPIR/Text_LDA/4_Demo/data/"
get_conn = psycopg2.connect(dbname='Demo DB',user='w10403323', host='localhost', password='terence')

get_conn.autocommit = True
get_cur  = get_conn.cursor()


get_cur.execute("Select basic.age, basic.gender, basic.sapsii_first from basic")
basictable = get_cur.fetchall()
if basictable[0][1] == 'M':
    gender = 1
else:
    gender = 0
newx=[float(basictable[0][0]),gender,float(basictable[0][2])]

get_cur.execute("Select proportion_"+str(click)+" from text2topic")
text2topictable = get_cur.fetchall()
for row in text2topictable:
    newx.append(float(row[0]))


np.array(newx).reshape(1,53)

use_all = False
if use_all == True:
    svr_in = joblib.load(path + "svr_in_50.pkl")
elif click == 0:
    svr_in = joblib.load(path + "svr_in_12.pkl")
else:
    svr_in = joblib.load(path + "svr_in_"+str(click*12)+".pkl")



get_cur.execute("update svm set survival_"+str(click)+" = "+str(1-float(svr_in.predict(np.array(newx).reshape(1,53))))+" where patient_id = 26429")




print "3_2_svm.py "+str(click)+" end."
pr.disable()
pr.print_stats(sort="tottime")