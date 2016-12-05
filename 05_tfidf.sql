CREATE TABLE tfidf
                   (
                     row_id integer,
                     subject_id integer,
                     hadm_id integer,
                     admittime timestamp(0) without time zone,
                     dischtime timestamp(0) without time zone,
                     chartdate timestamp(0) without time zone,
                     charttime timestamp(0) without time zone,
                     desc_stop_free text,
                     desc_stop_free_c integer,
                     keep_note integer,
                     tf_idf_500_all text,
                     tf_idf_500_per text,
                     tf_idf_all text,
                     tf_idf_per text
                    )