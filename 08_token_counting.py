#-*- coding:utf-8 -*-

import psycopg2
import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()


get_cur.execute("""Select desc_stop_free FROM tfidf Where keep_note = 1""")
table = get_cur.fetchall()
length = len(table)

words = []
subwords=[]
for i in range(0, length):
    subwords = list(set(subwords) | set(table[i][0].split()))
    if i % 10000 ==0:
        words = list(set(words) | set(subwords))
        subwords = []
        print str(i) + ", total " + str(length)
words = list(set(words) | set(subwords))
print "Unique vocabulary: "+str(len(words))




texts=[]; i=0;
for row in table:
    texts.append(row[0].lower().split())
    i = i+1
    if i%10000 ==0:
        print str(i)+", total "+ str(length)
print str(i)+", get data end."


from gensim import corpora
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
print "Unique vocabulary: " + str(len(words))