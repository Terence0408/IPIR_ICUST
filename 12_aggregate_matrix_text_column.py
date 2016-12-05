#-*- coding:utf-8 -*-

import psycopg2

get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='localhost', password='terence')
get_conn.autocommit = True
get_cur = get_conn.cursor()

get_cur.execute("""Create table aggregate_matrix_1 as Select * from aggregate_matrix;""")
get_cur.execute("""Create table aggregate_matrix_2 as Select * from aggregate_matrix;""")
get_cur.execute("""Create table aggregate_matrix_3 as Select * from aggregate_matrix;""")
get_cur.execute("""Create table aggregate_matrix_4 as Select * from aggregate_matrix;""")

hour_range = range(12,241,12)
hour_range.append('all')



hour_range = range(12,241,12)
hour_range.append('all')

for i in range(20,101):
    if i < 40:
        update_table = "aggregate_matrix_1"
    elif i < 60:
        update_table = "aggregate_matrix_2"
    elif i < 80:
        update_table = "aggregate_matrix_3"
    elif i < 101:
        update_table = "aggregate_matrix_4"
    for j in hour_range:
        text = "Alter table "+update_table+" add lda_"+str(i) +"_"+str(j)+" text;"
        #text = "Alter table "+update_table+" drop lda_"+str(i) +"_"+str(j)+";"
        get_cur.execute(text)
print "end"
