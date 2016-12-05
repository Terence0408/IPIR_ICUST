#-*- coding:utf-8 -*-

import statistics
import psycopg2

get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='localhost', password='terence')
get_conn.autocommit = True
get_cur  = get_conn.cursor()
get_cur.execute("""Select row_id, desc_stop_free_c, tf_idf_500_all, tfidf_all FROM tfidf Where keep_note = 1""")
table = get_cur.fetchall()


row_id=[];before=[]; tfidf_set=[]; after=[]
for row in table:
    row_id.append(row[0])
    before.append(row[1])
    tfidf_set.append(len(row[2].split()))
    after.append(len(row[3].split()))
print "end"

'''print min(before)
print statistics.median(before)
print max(before)

print statistics.mean(before)
print statistics.stdev(before)

print statistics.mode(before)


print min(tfidf_set)
print statistics.median(tfidf_set)
print max(tfidf_set)

print statistics.mean(tfidf_set)
print statistics.stdev(tfidf_set)

print statistics.mode(tfidf_set)



print min(after)
print statistics.median(after)
print max(after)

print statistics.mean(after)
print statistics.stdev(after)

print statistics.mode(after)'''





