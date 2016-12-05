#-*- coding:utf-8 -*-


from sklearn.feature_extraction.text import TfidfVectorizer
import psycopg2


get_conn = psycopg2.connect(dbname='mimiciii',user='w10403323', host='172.24.7.175', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()

get_cur.execute("""SELECT DISTINCT(subject_id)
                   FROM tfidf
                   Where keep_note = 1 and tf_idf_500_per is null
                   ORDER BY subject_id;""")
patients = get_cur.fetchall()
length =len(patients)

for k in range(0,length):
    get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='172.24.7.175', password='terence')
    get_conn.autocommit = True
    get_cur = get_conn.cursor()
    sql_text =  "Select row_id, desc_stop_free FROM tfidf WHERE keep_note = 1 and subject_id = " + str(patients[k][0])
    get_cur.execute(sql_text)
    table = get_cur.fetchall()

    corpus = []
    row_id = []
    for row in table:
        corpus.append(row[1])
        row_id.append(row[0])

    vectorizer = TfidfVectorizer(lowercase=False, max_df=1.0, min_df=0.0)
    tfidf = vectorizer.fit_transform(corpus)
    words = vectorizer.get_feature_names()

    for i in range(0, len(table)):
        d = tfidf.getrow(i)
        s = zip(d.indices, d.data)
        sorted_s = sorted(s, key=lambda v: v[1], reverse=True)
        info_word = ""
        for j in range(0, min(500, len(sorted_s))):
            info_word += " " + words[sorted_s[j][0]]
        get_cur.execute("""UPDATE tfidf set tf_idf_500_per =(%s) where row_id=(%s);""",
                        (info_word.strip(), str(row_id[i])))
    print str(patients[k][0]) +", " + str(k) +"/"+str(length)


