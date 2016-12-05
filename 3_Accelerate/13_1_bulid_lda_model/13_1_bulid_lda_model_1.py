#-*- coding:utf-8 -*-


import numpy
import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


numpy.random.seed(19870712)
path = u"D:/Develop code/IPIR/Text_LDA/1_data/all_lda/"

'''
import psycopg2
get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()
get_cur.execute("""Select row_id, tfidf_all FROM tfidf Where keep_note = 1 and tfidf_all is not null """)
table = get_cur.fetchall()
length = len(table)

texts=[]; i=0;
for row in table:
    texts.append(row[1].lower().split())
    i = i+1
    if i%100000 ==0:
        print str(i)+", total "+ str(length)
print str(i)+", get data end."


from gensim import corpora
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

dictionary.save(path+"all_lda_dictionary.dict")
corpora.MmCorpus.serialize(path+"all_lda_corpus.mm", corpus)

print 'dic save end'




'''
from gensim import corpora, models
import os.path

dictionary = corpora.Dictionary.load(path+"all_lda_dictionary.dict")
corpus = corpora.MmCorpus(path+"all_lda_corpus.mm")
print "dic load end."

for j in range(20, 61):
    if os.path.isfile(path +"all_lda_"+str(j)+'.model'):
        print "Number of topics: " + str(j)
    else:
        lda = models.ldamodel.LdaModel(corpus,id2word=dictionary, num_topics=j, update_every=1, passes=1)
        lda.save(path +"all_lda_"+str(j)+'.model')
        print "Number of topics: "+ str(j)

