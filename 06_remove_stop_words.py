#-*- coding:utf-8 -*-

from Appendix import Appendix
import psycopg2

get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()

'''
get_cur.execute("""SELECT count(*) FROM valid_noteevents as a left join tfidf as b on a.row_id = b.row_id Where b.row_id is null;""")
length = get_cur.fetchall()[0][0]
print length

while length > 0:
    sql_text = "Select * From w10403323.valid_noteevents as a left join tfidf as b on a.row_id = b.row_id Where b.row_id is null limit 10000;"
    get_cur.execute(sql_text)
    table = get_cur.fetchall()
    for row in table:
        desc_stop_free = Appendix.text_to_wordlist(row[7], remove_numbers=True,  remove_stopwords=True)
        if len(desc_stop_free)>=100:
            keep_note="1"
        else:
            keep_note="0"
        get_cur.execute("""INSERT INTO w10403323.tfidf (row_id, subject_id, hadm_id, admittime, dischtime, chartdate, charttime , desc_stop_free, desc_stop_free_c, keep_note)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (row[0], row[1], row[2], row[3], row[4], row[5], row[6]," ".join(desc_stop_free), len(desc_stop_free), keep_note))


    get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='172.24.7.175', password='terence')
    get_conn.autocommit = True
    get_cur = get_conn.cursor()

    get_cur.execute("""SELECT count(*) FROM valid_noteevents as a left join tfidf as b on a.row_id = b.row_id Where b.row_id is null;""")
    length = get_cur.fetchall()[0][0]
    print length


get_cur.execute("""
DELETE FROM tfidf
WHERE row_id IN (SELECT row_id
              FROM (SELECT row_id,
                             ROW_NUMBER() OVER (partition BY row_id ORDER BY row_id) AS rnum
                     FROM tfidf) t
              WHERE t.rnum > 1);""")
'''