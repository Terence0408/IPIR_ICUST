#-*- coding:utf-8 -*-
import sys
import psycopg2
from gensim import corpora, models
from collections import Counter
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
dictionary = corpora.Dictionary.load(path+"all_lda_dictionary.dict")
lda = models.LdaModel.load(path + "all_lda_50.model")


f = open(path+"re_text.txt", 'r')
regulated = f.read()
f.close()

text = regulated.split(" ")
length = float(len(text))

counts = Counter(text)
for i in [0,2,6,11,12,20,27,30,33,48]:
    topic_texts = lda.get_topic_terms(i,20)
    for j in topic_texts:

        get_cur.execute("update WORDCOUNT set count_" + str(click) + " = " + str(counts[dictionary.get(j[0])]) +
                        ", percent_" + str(click) + " = " +str(counts[dictionary.get(j[0])]/length)+
                        " where topic_id = " + str(i + 1) + " and word = '"+dictionary.get(j[0])+"';")



print "2_1_wordcount.py "+str(click)+" end."
pr.disable()
pr.print_stats(sort="tottime")