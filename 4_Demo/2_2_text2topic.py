#-*- coding:utf-8 -*-
import sys
import psycopg2
from gensim import corpora, models
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

vec_bow = dictionary.doc2bow(regulated.split())
vec_lsi = lda.__getitem__(vec_bow, eps=0)

for (ii, jj) in vec_lsi:
    get_cur.execute("update TEXT2TOPIC set proportion_"+str(click)+" = "+str(float(jj))+" where topic_id = "+str(ii+1)+";")

print "2_2_text2topic.py "+str(click)+" end."
pr.disable()
pr.print_stats(sort="tottime")


