#-*- coding:utf-8 -*-

import psycopg2
import logging, sys
import datetime
import time

path = u"D:/Develop code/IPIR/Text_LDA/1_data/all_lda/"


from gensim import corpora, models
print str(datetime.datetime.now().time().isoformat())+ " dic load start."
dictionary = corpora.Dictionary.load(path+"all_lda_dictionary.dict")
corpus = corpora.MmCorpus(path+"all_lda_corpus.mm")
print str(datetime.datetime.now().time().isoformat())+ " dic load end."







hour_range = range(12, 241, 12)
hour_range.append('all')
topic_range = range(20,101)

topic_range = range(50,51)

for j in hour_range:
    for i in topic_range:
        if i < 40:
            update_table = "aggregate_matrix_1"
        elif i < 60:
            update_table = "aggregate_matrix_2"
        elif i < 80:
            update_table = "aggregate_matrix_3"
        elif i < 101:
            update_table = "aggregate_matrix_4"

        loc_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='localhost', password='terence')
        loc_conn.autocommit = True
        loc_cur = loc_conn.cursor()
        #get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='172.24.7.175', password='terence')
        get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='localhost', password='terence')
        get_conn.autocommit = True
        get_cur = get_conn.cursor()

        lda = models.LdaModel.load(path + "all_lda_" + str(i) + '.model')
        print datetime.datetime.now().time().isoformat()+" topics: " + str(i) + ", hours: " + str(j)
        reusetext  = "Select subject_id, hadm_id From "+update_table+" "
        reusetext += "where lda_"+str(i) +"_"+str(j) +" is null and "
        reusetext += "hadm_id between 100001 and 109963 "
        reusetext += "Order by hadm_id;"
        get_cur.execute(reusetext)
        agg_table = get_cur.fetchall()
        length =len(agg_table)

        count = 0
        while length>0:
            try:
                for row in agg_table:
                    if isinstance( j, int ):
                        text = "Select agg.subject_id, agg.hadm_id, tfidf.tfidf_all " \
                               "From aggregate_matrix as agg inner join tfidf on " \
                               "     agg.subject_id =tfidf.subject_id and agg.hadm_id =tfidf.hadm_id " \
                               "Where tfidf.subject_id = " + str(row[0]) + " and " \
                               "      tfidf.hadm_id = " + str(row[1]) + " and keep_note = 1 and " \
                               "      tfidf.admithour <= " + str(j)
                    else:
                        text = "Select agg.subject_id, agg.hadm_id, tfidf.tfidf_all " \
                               "From aggregate_matrix as agg inner join tfidf " \
                               "     on agg.subject_id =tfidf.subject_id and agg.hadm_id =tfidf.hadm_id " \
                               "Where tfidf.subject_id = " + str(row[0]) + " and " \
                               "      tfidf.hadm_id = " + str(row[1]) + " and " \
                               "      keep_note = 1 "

                    loc_cur.execute(text)
                    text2topic_table = loc_cur.fetchall()



                    if len(text2topic_table)>0:
                        notes = []
                        for note in text2topic_table:
                            notes.append(note[2])
                        t_notes = " ".join(notes)
                        vec_bow = dictionary.doc2bow(t_notes.split())
                        vec_lsi = lda.__getitem__(vec_bow, eps=0)

                        topic_proportion = []
                        for (ii, jj) in vec_lsi:
                            topic_proportion.append(str(jj))

                        text  = "UPDATE "+update_table+" set lda_"+str(i)+"_"+str(j)+" = '"+" ".join(topic_proportion)+"' "
                        text += "Where subject_id = " + str(row[0]) + " and hadm_id = " + str(row[1])+" ;"
                        get_cur.execute(text)

                    else:
                        text  = "UPDATE "+update_table+" set lda_"+str(i)+"_"+str(j)+" = '"+"No notes"+"' "
                        text += "Where subject_id = " + str(row[0]) + " and hadm_id = " + str(row[1])+" ;"
                        get_cur.execute(text)

                    if count % 200 ==0:
                        print datetime.datetime.now().time().isoformat()+" topics: " + str(i) + ", hours: " + str(j)+".  "+str(count+1) + "/"+str(length)
                    count += 1
            except:
                time.sleep(60)
            finally:
                get_cur.execute(reusetext)
                agg_table = get_cur.fetchall()
                length = len(agg_table)
        print datetime.datetime.now().time().isoformat()+" topics: " + str(i) + ", hours: " + str(j)

print 'end'