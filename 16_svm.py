from sklearn.svm import SVR
from sklearn.externals import joblib
import psycopg2
import numpy as np
import logging, sys
import datetime

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
print datetime.datetime.now().time().isoformat() + ". Start."

path = u"D:/Develop_code/IPIR/Text_LDA/1_data/all_svm/"

get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='localhost', password='terence')
get_conn.autocommit = True
get_cur = get_conn.cursor()

hour_range = range(12, 241, 12)
hour_range.append('all')
topic_range = range(20, 101)



hour_range=['all']
topic_range = range(50, 51)
for i in topic_range:
    if i < 40:
        update_table = "aggregate_matrix_1"
    elif i < 60:
        update_table = "aggregate_matrix_2"
    elif i < 80:
        update_table = "aggregate_matrix_3"
    elif i < 101:
        update_table = "aggregate_matrix_4"

    X = np.zeros((1, i + 3));
    y_in = np.zeros((1, 0));
    y_30 = np.zeros((1, 0));
    y_1y = np.zeros((1, 0));

    for j in hour_range:
        text = "Select count(*) from "+ update_table + " Where lda_"+str(i)+"_"+str(j)+" is null;"
        get_cur.execute(text)
        checktable = get_cur.fetchall()
        length_check =len(checktable)

        print datetime.datetime.now().time().isoformat() + ". 2."

        if checktable[0][0] == 0L:
            train_text  = "Select death_inhosp, death_30, death_1year, age, gender, first_sapsii, lda_" + str(i) + "_" + str(j)+" "
            train_text += "from "+ update_table+" "
            train_text += "Where train = 1 and lda_" + str(i) + "_" + str(j)+ " not like 'No notes';"

            get_cur.execute(train_text)
            traintable = get_cur.fetchall()
            length_use = len(traintable)

        print datetime.datetime.now().time().isoformat() + ". 3."
        print length_use
        for row in traintable:
            if row[4] == 'M':
                gender = 1
            else:
                gender = 0
            X = np.vstack((X, np.array(map(np.float64, [row[3], gender, row[5]] + row[6].split()))))
            y_in = np.append(y_in, np.float64(row[0]))
            y_30 = np.append(y_30, np.float64(row[1]))
            y_1y = np.append(y_1y, np.float64(row[2]))

        print datetime.datetime.now().time().isoformat() + ". "+ str(len(X))

    X = X[1:]
    y_in = y_in[0:];
    y_30 = y_30[0:];
    y_1y = y_1y[0:]

    print datetime.datetime.now().time().isoformat() + ". translate data."

    svr_in = SVR(C=1.0, epsilon=0.2);
    svr_in.fit(X, y_in);
    joblib.dump(svr_in, path + "topic_" + str(i) + "/" + "svr_in_" + str(j) + ".pkl")
    print datetime.datetime.now().time().isoformat() + ". topics: " + str(i) + ", hours: " + str(j) + ", inhosp model"

    svr_30 = SVR(C=1.0, epsilon=0.2)
    svr_30.fit(X, y_30);
    joblib.dump(svr_30, path + "topic_" + str(i) + "/" + "svr_30_" + str(j) + ".pkl")
    print datetime.datetime.now().time().isoformat() + ". topics: " + str(i) + ", hours: " + str(j) + ", 30 day model"

    svr_1y = SVR(C=1.0, epsilon=0.2)
    svr_1y.fit(X, y_1y);
    joblib.dump(svr_1y, path + "topic_" + str(i) + "/" + "svr_1y_" + str(j) + ".pkl")
    print datetime.datetime.now().time().isoformat() + ". topics: " + str(i) + ", hours: " + str(j) + ", 1 year model"





'''
n_samples, n_features = 10, 5
np.random.seed(0)
y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)
clf = SVR(C=1.0, epsilon=0.2)
clf.fit(X, y)

joblib.dump(clf, 'D:/filename.pkl')

clf = joblib.load('D:/filename.pkl')

np.random.seed(0)
x = np.random.randn(1, n_features)
clf.predict(x)
'''



print 'end'

