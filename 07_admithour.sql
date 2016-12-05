Create table tfidf_1 as


Select tfidf.*,
case When tfidf.charttime is not null then date_part('day', tfidf.charttime - agg.admittime)*24 + date_part('hour', tfidf.charttime - agg.admittime)
     When tfidf.charttime is null and tfidf.chartdate + interval '1 days' <= tfidf.dischtime then date_part('day', tfidf.chartdate - agg.admittime)*24 + 24 + date_part('hour', tfidf.chartdate - agg.admittime)
     When tfidf.charttime is null and tfidf.chartdate + interval '1 days' > tfidf.dischtime then date_part('day', tfidf.dischtime - agg.admittime)*24 + date_part('hour', tfidf.dischtime - agg.admittime)
     end as admithour
From aggregate_matrix as agg left join tfidf on agg.subject_id =tfidf.subject_id and agg.hadm_id =tfidf.hadm_id;

ALTER TABLE tfidf RENAME TO tfidf_2;
ALTER TABLE tfidf_1 RENAME TO tfidf;

Drop TABLE tfidf_2;