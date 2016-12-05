#-*- coding:utf-8 -*-

import datetime
import psycopg2
get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()
get_cur.execute("""Select row_id, desc_stop_free, tf_idf_500_all FROM tfidf
                   Where keep_note = 1 and tfidf_all is null
                         and row_id between 396996 and 459896""")
table = get_cur.fetchall()
length = len(table)

for i in range(0, length):
    info_set = set(table[i][2].split())
    content = [w for w in table[i][1].split() if w in info_set]

    text = "UPDATE tfidf set tfidf_all = '" + " ".join(content) + "'"
    text += "Where row_id = " + str(table[i][0])
    get_cur.execute(text)
    if i % 100 == 0:
        print str(datetime.datetime.now().time().isoformat()) + str(i) + ", total " + str(length)
