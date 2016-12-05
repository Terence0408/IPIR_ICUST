#-*- coding:utf-8 -*-

import psycopg2

get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()
get_cur.execute("""Select note.row_id, tfidf.admithour, note.chartdate, note.charttime, note.text
                   From tfidf left join public.noteevents as note on tfidf.row_id = note.row_id
                   Where tfidf.hadm_id = 151943 and tfidf.keep_note = 1 and tfidf.admithour <= 132 """)

raw_table = get_cur.fetchall()


get_cur.execute("""Select hadm_id, admittime, age, gender, first_sapsii,
                   lda_50_12, lda_50_24, lda_50_36,  lda_50_48,  lda_50_60, lda_50_72,
                   lda_50_84, lda_50_96, lda_50_108, lda_50_120, lda_50_132
                   From aggregate_matrix
                   Where hadm_id = 151943 """)

basic_table = get_cur.fetchall()



from gensim import corpora, models
path = u"D:/Develop code/IPIR/Text_LDA/1_data/all_lda/"
lda = models.LdaModel.load(path + "all_lda_50.model")

