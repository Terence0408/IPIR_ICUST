#-*- coding:utf-8 -*-

import psycopg2
import random

random.seed(19870712)

get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='localhost', password='terence')
get_conn.autocommit = True
get_cur = get_conn.cursor()

#get_cur.execute("Alter table aggregate_matrix add train int")
#get_cur.execute("Alter table aggregate_matrix_1 add train int")
#get_cur.execute("Alter table aggregate_matrix_2 add train int")
#get_cur.execute("Alter table aggregate_matrix_3 add train int")
#get_cur.execute("Alter table aggregate_matrix_4 add train int")


get_cur.execute("Select distinct(subject_id) from aggregate_matrix;")
agg_table = get_cur.fetchall()


subject_ids = []
for row in agg_table:
    subject_ids.append(str(row[0]))


test_ids = random.sample(subject_ids, int(len(agg_table)*0.2))

for table in ["aggregate_matrix", "aggregate_matrix_1", "aggregate_matrix_2", "aggregate_matrix_3", "aggregate_matrix_4"]:
    text = "UPDATE "+table+" set train = 0 where subject_id in ("+','.join(test_ids)+");"
    get_cur.execute(text)
    text = "UPDATE " + table + " set train = 1 where subject_id not in (" + ','.join(test_ids) + ");"
    get_cur.execute(text)

print 'end'
