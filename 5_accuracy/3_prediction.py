from sklearn.svm import SVR
from sklearn.externals import joblib
import psycopg2
import numpy as np
import logging, sys
import datetime

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
print datetime.datetime.now().time().isoformat() + ". Start."

path = u"D:/Develop_code/IPIR/Text_LDA/5_accuracy/model/"

get_conn = psycopg2.connect(dbname='mimiciii', user='w10403323', host='localhost', password='terence')
get_conn.autocommit = True
get_cur = get_conn.cursor()


hour_range = range(12, 241, 12)
topic_range = range(50, 51)

models_in = []
models_in.append(joblib.load(path + "svr_in/Admission Baseline Model.pkl"))
models_in.append(joblib.load(path + "svr_in/Retrospective Derived Feature Model.pkl"))
models_in.append(joblib.load(path + "svr_in/Retrospective Topic Model.pkl"))
models_in.append(joblib.load(path + "svr_in/Retrospective Topic and Admission Model.pkl"))
models_in.append(joblib.load(path + "svr_in/Retrospective Topic and Derived Feature Model.pkl"))
for j in hour_range:
    models_in.append(joblib.load(path + "svr_in/Time-varying Topic Model " + str(j/12) + ".pkl"))
    models_in.append(joblib.load(path + "svr_in/Combined Time-varying Model " + str(j/12) + ".pkl"))

models_30 = []
models_30.append(joblib.load(path + "svr_30/Admission Baseline Model.pkl"))
models_30.append(joblib.load(path + "svr_30/Retrospective Derived Feature Model.pkl"))
models_30.append(joblib.load(path + "svr_30/Retrospective Topic Model.pkl"))
models_30.append(joblib.load(path + "svr_30/Retrospective Topic and Admission Model.pkl"))
models_30.append(joblib.load(path + "svr_30/Retrospective Topic and Derived Feature Model.pkl"))
for j in hour_range:
    models_30.append(joblib.load(path + "svr_30/Time-varying Topic Model " + str(j/12) + ".pkl"))
    models_30.append(joblib.load(path + "svr_30/Combined Time-varying Model " + str(j/12) + ".pkl"))


models_1y = []
models_1y.append(joblib.load(path + "svr_1y/Admission Baseline Model.pkl"))
models_1y.append(joblib.load(path + "svr_1y/Retrospective Derived Feature Model.pkl"))
models_1y.append(joblib.load(path + "svr_1y/Retrospective Topic Model.pkl"))
models_1y.append(joblib.load(path + "svr_1y/Retrospective Topic and Admission Model.pkl"))
models_1y.append(joblib.load(path + "svr_1y/Retrospective Topic and Derived Feature Model.pkl"))
for j in hour_range:
    models_1y.append(joblib.load(path + "svr_1y/Time-varying Topic Model " + str(j/12) + ".pkl"))
    models_1y.append(joblib.load(path + "svr_1y/Combined Time-varying Model " + str(j/12) + ".pkl"))


for i in topic_range:
    if i < 40:
        update_table = "aggregate_matrix_1"
    elif i < 60:
        update_table = "aggregate_matrix_2"
    elif i < 80:
        update_table = "aggregate_matrix_3"
    elif i < 101:
        update_table = "aggregate_matrix_4"

# Step1: Select a features.
    print datetime.datetime.now().time().isoformat() + ". Step1: Select a admission."

    text  = "With temptable as (Select hadm_id from accuracy where death_type = '1y') "
    text += "Select agg.hadm_id "
    text += "From temptable as acc right join new_table as agg on acc.hadm_id =agg.hadm_id "
    text += "Where acc.hadm_id is null;"# and agg.hadm_id = 151943; "


    get_cur.execute(text)
    idtable = get_cur.fetchall()


    for row in idtable:
# Step2: Select features for hadm_id.
        text  = "Select subject_id, hadm_id, staytime, death_inhosp, death_30, death_1year, "
        text += "age, gender, first_sapsii, min_sapsii, max_sapsii, final_sapsii, "
        text += "eh_congestive_heart_failure, eh_cardiac_arrhythmias, eh_valvular_disease, eh_pulmonary_circulation, eh_peripheral_vascular, "
        text += "eh_hypertension, eh_paralysis, eh_other_neurological, eh_chronic_pulmonary, eh_diabetes_uncomplicated, "
        text += "eh_diabetes_complicated, eh_hypothyroidism, eh_renal_failure, eh_liver_disease, eh_peptic_ulcer, "
        text += "eh_aids, eh_lymphoma, eh_metastatic_cancer, eh_solid_tumor, eh_rheumatoid_arthritis, "
        text += "eh_coagulopathy, eh_obesity, eh_weight_loss, eh_fluid_electrolyte, eh_blood_loss_anemia, "
        text += "eh_deficiency_anemias, eh_alcohol_abuse, eh_drug_abuse, eh_psychoses, eh_depression, "
        text += "lda_"+str(i)+"_12, lda_"+str(i)+"_24, lda_"+str(i)+"_36, "
        text += "lda_"+str(i)+"_48, lda_"+str(i)+"_60, lda_"+str(i)+"_72, "
        text += "lda_"+str(i)+"_84, lda_"+str(i)+"_96, lda_"+str(i)+"_108, "
        text += "lda_"+str(i)+"_120, lda_"+str(i)+"_132, lda_"+str(i)+"_144, "
        text += "lda_"+str(i)+"_156, lda_"+str(i)+"_168, lda_"+str(i)+"_180, "
        text += "lda_"+str(i)+"_192, lda_"+str(i)+"_204, lda_"+str(i)+"_216, "
        text += "lda_"+str(i)+"_228, lda_"+str(i)+"_240, lda_"+str(i)+"_all, "
        text += "train "
        text += "from new_table "
        text += "Where hadm_id = "+str(row[0])+" ;"

        get_cur.execute(text)
        featuretable = get_cur.fetchall()
        features = featuretable[0]
        if features[7] == 'M':
            gender = 1
        else:
            gender = 0


# Step3: Prediction Time-varying Topic Model and Combined Time-varying Model.
        predictions_in = [];
        predictions_30 = [];
        predictions_1y = [];
        for j in hour_range:
            if j <= int(features[2]):
                if features[41+j/12] == 'No notes':
                    predictions_in.append('No notes')
                    predictions_30.append('No notes')
                    predictions_1y.append('No notes')

                    predictions_in.append('No notes')
                    predictions_30.append('No notes')
                    predictions_1y.append('No notes')
                else:
                    newx=np.array(map(np.float64, [features[6], gender, features[8]] + features[41+j/12].split())).reshape(1,53)

                    predictions_in.append(str(float(models_in[4+(j/12)*2-1].predict(newx[:, range(3,53)]))))
                    predictions_30.append(str(float(models_30[4+(j/12)*2-1].predict(newx[:, range(3,53)]))))
                    predictions_1y.append(str(float(models_1y[4+(j/12)*2-1].predict(newx[:, range(3,53)]))))

                    predictions_in.append(str(float(models_in[4+(j/12)*2].predict(newx))))
                    predictions_30.append(str(float(models_30[4+(j/12)*2].predict(newx))))
                    predictions_1y.append(str(float(models_1y[4+(j/12)*2].predict(newx))))

            else:
                predictions_in.append('leave')
                predictions_30.append('leave')
                predictions_1y.append('leave')

                predictions_in.append('leave')
                predictions_30.append('leave')
                predictions_1y.append('leave')

# Step4: Prediction Other Model.
        if features[62] == 'No notes':
            newx = np.array(map(np.float64, [features[6], gender, features[8]] + list(features[9:42]))).reshape(1, 36)

            predictions_in.append(str(float(models_in[0].predict(newx[:, range(0,3)]))))
            predictions_30.append(str(float(models_30[0].predict(newx[:, range(0,3)]))))
            predictions_1y.append(str(float(models_1y[0].predict(newx[:, range(0,3)]))))

            predictions_in.append(str(float(models_in[1].predict(newx[:, range(0, 36)]))))
            predictions_30.append(str(float(models_30[1].predict(newx[:, range(0, 36)]))))
            predictions_1y.append(str(float(models_1y[1].predict(newx[:, range(0, 36)]))))

            predictions_in += ['No notes']*3
            predictions_30 += ['No notes']*3
            predictions_1y += ['No notes']*3

        else:
            newx = np.array(map(np.float64, [features[6], gender, features[8]] + list(features[9:42]) + features[62].split())).reshape(1, 86)

            predictions_in.append(str(float(models_in[0].predict(newx[:, range(0,3)]))))
            predictions_30.append(str(float(models_30[0].predict(newx[:, range(0,3)]))))
            predictions_1y.append(str(float(models_1y[0].predict(newx[:, range(0,3)]))))

            predictions_in.append(str(float(models_in[1].predict(newx[:, range(0, 36)]))))
            predictions_30.append(str(float(models_30[1].predict(newx[:, range(0, 36)]))))
            predictions_1y.append(str(float(models_1y[1].predict(newx[:, range(0, 36)]))))

            predictions_in.append(str(float(models_in[2].predict(newx[:, range(36, 86)]))))
            predictions_30.append(str(float(models_30[2].predict(newx[:, range(36, 86)]))))
            predictions_1y.append(str(float(models_1y[2].predict(newx[:, range(36, 86)]))))

            predictions_in.append(str(float(models_in[3].predict(newx[:, range(0, 3)+range(36, 86)]))))
            predictions_30.append(str(float(models_30[3].predict(newx[:, range(0, 3)+range(36, 86)]))))
            predictions_1y.append(str(float(models_1y[3].predict(newx[:, range(0, 3)+range(36, 86)]))))

            predictions_in.append(str(float(models_in[4].predict(newx))))
            predictions_30.append(str(float(models_30[4].predict(newx))))
            predictions_1y.append(str(float(models_1y[4].predict(newx))))



        text_1 = "insert into accuracy (subject_id, hadm_id, train, topics, death_type, death, admission_baseline, " \
        "time_varying_topic_1, time_varying_topic_2, time_varying_topic_3, time_varying_topic_4, " \
        "time_varying_topic_5, time_varying_topic_6, time_varying_topic_7, time_varying_topic_8, " \
        "time_varying_topic_9, time_varying_topic_10, time_varying_topic_11, time_varying_topic_12, " \
        "time_varying_topic_13, time_varying_topic_14, time_varying_topic_15, time_varying_topic_16, " \
        "time_varying_topic_17, time_varying_topic_18, time_varying_topic_19, time_varying_topic_20, " \
        "combined_time_varying_1, combined_time_varying_2, combined_time_varying_3, combined_time_varying_4, " \
        "combined_time_varying_5, combined_time_varying_6, combined_time_varying_7, combined_time_varying_8, " \
        "combined_time_varying_9, combined_time_varying_10, combined_time_varying_11, combined_time_varying_12, " \
        "combined_time_varying_13, combined_time_varying_14, combined_time_varying_15, combined_time_varying_16, " \
        "combined_time_varying_17, combined_time_varying_18, combined_time_varying_19, combined_time_varying_20, " \
        "retrospective_derived_feature, retrospective_topic, retrospective_topic_and_admission, " \
        "retrospective_topic_and_derived_feature) " \
        "Values ("+str(features[0])+", "+str(features[1])+", "+str(features[63])+", "+str(i)+", "+"'inhosp'"+", "+ \
                 str(features[3])+", '"+str(predictions_in[40])+ "', '"+str(predictions_in[0])+ "', '"+ \
                 str(predictions_in[2])+ "', '"+str(predictions_in[4])+ "', '"+str(predictions_in[6])+ "', '"+ \
                 str(predictions_in[8])+ "', '"+str(predictions_in[10])+ "', '"+str(predictions_in[12])+ "', '"+ \
                 str(predictions_in[14])+ "', '"+str(predictions_in[16])+ "', '"+str(predictions_in[18])+ "', '"+ \
                 str(predictions_in[20])+ "', '"+str(predictions_in[22])+ "', '"+str(predictions_in[24])+ "', '"+ \
                 str(predictions_in[26])+ "', '"+str(predictions_in[28])+ "', '"+str(predictions_in[30])+ "', '"+ \
                 str(predictions_in[32])+ "', '"+str(predictions_in[34])+ "', '"+str(predictions_in[36])+ "', '"+ \
                 str(predictions_in[38])+ "', '"+str(predictions_in[1])+ "', '"+str(predictions_in[3])+ "', '"+ \
                 str(predictions_in[5])+ "', '"+str(predictions_in[7])+ "', '"+str(predictions_in[9])+ "', '"+ \
                 str(predictions_in[11])+ "', '"+str(predictions_in[13])+ "', '"+str(predictions_in[15])+ "', '"+ \
                 str(predictions_in[17])+ "', '"+str(predictions_in[19])+ "', '"+str(predictions_in[21])+ "', '"+ \
                 str(predictions_in[23])+ "', '"+str(predictions_in[25])+ "', '"+str(predictions_in[27])+ "', '"+ \
                 str(predictions_in[29])+ "', '"+str(predictions_in[31])+ "', '"+str(predictions_in[33])+ "', '"+ \
                 str(predictions_in[35])+ "', '"+str(predictions_in[37])+ "', '"+str(predictions_in[39])+ "', '"+ \
                 str(predictions_in[41])+ "', '"+str(predictions_in[42])+ "', '"+str(predictions_in[43])+ "', '"+ \
                 str(predictions_in[44])+ "')"
        get_cur.execute(text_1)

        text_2 = "insert into accuracy (subject_id, hadm_id, train, topics, death_type, death, admission_baseline, " \
        "time_varying_topic_1, time_varying_topic_2, time_varying_topic_3, time_varying_topic_4, " \
        "time_varying_topic_5, time_varying_topic_6, time_varying_topic_7, time_varying_topic_8, " \
        "time_varying_topic_9, time_varying_topic_10, time_varying_topic_11, time_varying_topic_12, " \
        "time_varying_topic_13, time_varying_topic_14, time_varying_topic_15, time_varying_topic_16, " \
        "time_varying_topic_17, time_varying_topic_18, time_varying_topic_19, time_varying_topic_20, " \
        "combined_time_varying_1, combined_time_varying_2, combined_time_varying_3, combined_time_varying_4, " \
        "combined_time_varying_5, combined_time_varying_6, combined_time_varying_7, combined_time_varying_8, " \
        "combined_time_varying_9, combined_time_varying_10, combined_time_varying_11, combined_time_varying_12, " \
        "combined_time_varying_13, combined_time_varying_14, combined_time_varying_15, combined_time_varying_16, " \
        "combined_time_varying_17, combined_time_varying_18, combined_time_varying_19, combined_time_varying_20, " \
        "retrospective_derived_feature, retrospective_topic, retrospective_topic_and_admission, " \
        "retrospective_topic_and_derived_feature) " \
        "Values ("+str(features[0])+", "+str(features[1])+", "+str(features[63])+", "+str(i)+", "+"'30day'"+", "+ \
                str(features[4])+", '"+str(predictions_30[40])+ "', '"+str(predictions_30[0])+ "', '"+ \
                str(predictions_30[2])+ "', '"+str(predictions_30[4])+ "', '"+str(predictions_30[6])+ "', '"+ \
                str(predictions_30[8])+ "', '"+str(predictions_30[10])+ "', '"+str(predictions_30[12])+ "', '"+ \
                str(predictions_30[14])+ "', '"+str(predictions_30[16])+ "', '"+str(predictions_30[18])+ "', '"+ \
                str(predictions_30[20])+ "', '"+str(predictions_30[22])+ "', '"+str(predictions_30[24])+ "', '"+ \
                str(predictions_30[26])+ "', '"+str(predictions_30[28])+ "', '"+str(predictions_30[30])+ "', '"+ \
                str(predictions_30[32])+ "', '"+str(predictions_30[34])+ "', '"+str(predictions_30[36])+ "', '"+ \
                str(predictions_30[38])+ "', '"+str(predictions_30[1])+ "', '"+str(predictions_30[3])+ "', '"+ \
                str(predictions_30[5])+ "', '"+str(predictions_30[7])+ "', '"+str(predictions_30[9])+ "', '"+ \
                str(predictions_30[11])+ "', '"+str(predictions_30[13])+ "', '"+str(predictions_30[15])+ "', '"+ \
                str(predictions_30[17])+ "', '"+str(predictions_30[19])+ "', '"+str(predictions_30[21])+ "', '"+ \
                str(predictions_30[23])+ "', '"+str(predictions_30[25])+ "', '"+str(predictions_30[27])+ "', '"+ \
                str(predictions_30[29])+ "', '"+str(predictions_30[31])+ "', '"+str(predictions_30[33])+ "', '"+ \
                str(predictions_30[35])+ "', '"+str(predictions_30[37])+ "', '"+str(predictions_30[39])+ "', '"+ \
                str(predictions_30[41])+ "', '"+str(predictions_30[42])+ "', '"+str(predictions_30[43])+ "', '"+ \
                str(predictions_30[44])+ "')"
        get_cur.execute(text_2)


        text_3 = "insert into accuracy (subject_id, hadm_id, train, topics, death_type, death, admission_baseline, " \
        "time_varying_topic_1, time_varying_topic_2, time_varying_topic_3, time_varying_topic_4, " \
        "time_varying_topic_5, time_varying_topic_6, time_varying_topic_7, time_varying_topic_8, " \
        "time_varying_topic_9, time_varying_topic_10, time_varying_topic_11, time_varying_topic_12, " \
        "time_varying_topic_13, time_varying_topic_14, time_varying_topic_15, time_varying_topic_16, " \
        "time_varying_topic_17, time_varying_topic_18, time_varying_topic_19, time_varying_topic_20, " \
        "combined_time_varying_1, combined_time_varying_2, combined_time_varying_3, combined_time_varying_4, " \
        "combined_time_varying_5, combined_time_varying_6, combined_time_varying_7, combined_time_varying_8, " \
        "combined_time_varying_9, combined_time_varying_10, combined_time_varying_11, combined_time_varying_12, " \
        "combined_time_varying_13, combined_time_varying_14, combined_time_varying_15, combined_time_varying_16, " \
        "combined_time_varying_17, combined_time_varying_18, combined_time_varying_19, combined_time_varying_20, " \
        "retrospective_derived_feature, retrospective_topic, retrospective_topic_and_admission, " \
        "retrospective_topic_and_derived_feature) " \
        "Values ("+str(features[0])+", "+str(features[1])+", "+str(features[63])+", "+str(i)+", "+"'1y'"+", "+ \
                str(features[5])+", '"+str(predictions_1y[40])+ "', '"+str(predictions_1y[0])+ "', '"+ \
                str(predictions_1y[2])+ "', '"+str(predictions_1y[4])+ "', '"+str(predictions_1y[6])+ "', '"+ \
                str(predictions_1y[8])+ "', '"+str(predictions_1y[10])+ "', '"+str(predictions_1y[12])+ "', '"+ \
                str(predictions_1y[14])+ "', '"+str(predictions_1y[16])+ "', '"+str(predictions_1y[18])+ "', '"+ \
                str(predictions_1y[20])+ "', '"+str(predictions_1y[22])+ "', '"+str(predictions_1y[24])+ "', '"+ \
                str(predictions_1y[26])+ "', '"+str(predictions_1y[28])+ "', '"+str(predictions_1y[30])+ "', '"+ \
                str(predictions_1y[32])+ "', '"+str(predictions_1y[34])+ "', '"+str(predictions_1y[36])+ "', '"+ \
                str(predictions_1y[38])+ "', '"+str(predictions_1y[1])+ "', '"+str(predictions_1y[3])+ "', '"+ \
                str(predictions_1y[5])+ "', '"+str(predictions_1y[7])+ "', '"+str(predictions_1y[9])+ "', '"+ \
                str(predictions_1y[11])+ "', '"+str(predictions_1y[13])+ "', '"+str(predictions_1y[15])+ "', '"+ \
                str(predictions_1y[17])+ "', '"+str(predictions_1y[19])+ "', '"+str(predictions_1y[21])+ "', '"+ \
                str(predictions_1y[23])+ "', '"+str(predictions_1y[25])+ "', '"+str(predictions_1y[27])+ "', '"+ \
                str(predictions_1y[29])+ "', '"+str(predictions_1y[31])+ "', '"+str(predictions_1y[33])+ "', '"+ \
                str(predictions_1y[35])+ "', '"+str(predictions_1y[37])+ "', '"+str(predictions_1y[39])+ "', '"+ \
                str(predictions_1y[41])+ "', '"+str(predictions_1y[42])+ "', '"+str(predictions_1y[43])+ "', '"+ \
                str(predictions_1y[44])+ "')"
        get_cur.execute(text_3)




print 'end'

