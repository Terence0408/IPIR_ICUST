#-*- coding:utf-8 -*-

import psycopg2
import pickle

path = u"D:/Develop code/IPIR/Text_LDA/1_data/all_tfidf/"


'''
get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()
get_cur.execute("""Select row_id, desc_stop_free FROM tfidf Where keep_note = 1""")
table = get_cur.fetchall()
length = len(table)

corpus = []; row_id = []; i=0;
for row in table:
    corpus.append(row[1])
    row_id.append(row[0])
    i = i+1
    if i%1000 ==0:
        print str(i)+", total "+ str(length)
print str(i)+", get data end."


pickle.dump(row_id, open(path+"all_tfidf_row_id.txt", "w"))
pickle.dump(corpus, open(path+"all_tfidf_corpus.txt", "w"))
print "pickle end."
'''


corpus = pickle.load(open(path+"all_tfidf_corpus.txt", "r"))
row_id = pickle.load(open(path+"all_tfidf_row_id.txt", "r"))
print "pickle load end."


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(lowercase=False, max_df=1.0, min_df=0.0)
tfidf = vectorizer.fit_transform(corpus)
words = vectorizer.get_feature_names()
print "TF-IDF end."


get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()
get_cur.execute("""Select row_id From tfidf Where keep_note = 1 and tf_idf_500_all is null limit 20000""")
update_rows = get_cur.fetchall()
length = len(update_rows); print length;
while length>0:
    try:
        for row in update_rows:
            i = row_id.index(int(row[0]))
            d = tfidf.getrow(i)
            s = zip(d.indices, d.data)
            sorted_s = sorted(s, key=lambda v: v[1], reverse=True)
            info_word = ""
            for j in range(0, min(500, len(sorted_s))):
                info_word += " " + words[sorted_s[j][0]]

            get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='172.24.7.175', password='terence')
            get_conn.autocommit = True
            get_cur = get_conn.cursor()
            get_cur.execute("""UPDATE tfidf set tf_idf_500_all =(%s) where row_id=(%s);""",
                            (info_word.strip(), str(row_id[i])))
            length =length - 1
            if length % 500 == 0:
                print str(length)

    except:
        print 'error!!!! row '+ str(row[0])
    finally:
        get_cur.execute("""Select row_id From tfidf Where keep_note = 1 and tf_idf_500_all is null limit 20000""")
        update_rows = get_cur.fetchall()
        length = len(update_rows);
        print length;
print "End."






