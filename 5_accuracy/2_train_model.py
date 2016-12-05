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

for i in topic_range:
    if i < 40:
        update_table = "aggregate_matrix_1"
    elif i < 60:
        update_table = "aggregate_matrix_2"
    elif i < 80:
        update_table = "aggregate_matrix_3"
    elif i < 101:
        update_table = "aggregate_matrix_4"




# Step1: Train Time-varying Topic Model and Combined Time-varying Model.

    print datetime.datetime.now().time().isoformat() + ". Step1: Train Time-varying Topic Model and Combined Time-varying Model."
    # Step1-1: Get outcome, admission baseline, lda topic proportions data.
    for j in hour_range:
        text = "Select count(*) from "+ update_table + " Where lda_"+str(i)+"_"+str(j)+" is null;"
        get_cur.execute(text)
        checktable = get_cur.fetchall()
        length_check =len(checktable)

        if checktable[0][0] == 0L:
            train_text  = "Select death_inhosp, death_30, death_1year, age, Case When gender = 'F' then 0 else 1 end as gender, first_sapsii, lda_" + str(i) + "_" + str(j)+" "
            train_text += "from new_table "
            train_text += "Where train = 1 and staytime > "+ str(j)+" "
            train_text += "and lda_" + str(i) + "_" + str(j)+ " not like 'No notes';"

            get_cur.execute(train_text)
            traintable = get_cur.fetchall()
            length_use = len(traintable)
        print datetime.datetime.now().time().isoformat() + ". Get hour "+str(j)+" data. length = "+str(length_use)

    # Step1-2: Translate admission baseline data into numpy format.
        X = np.zeros((1, i + 3)); y_in = np.zeros((1, 0)); y_30 = np.zeros((1, 0)); y_1y = np.zeros((1, 0));
        for row in traintable:
            X = np.vstack((X, np.array(map(np.float64, [row[3], row[4], row[5]] + row[6].split()))))
            y_in = np.append(y_in, np.float64(row[0]))
            y_30 = np.append(y_30, np.float64(row[1]))
            y_1y = np.append(y_1y, np.float64(row[2]))

        X = X[1:]; y_in = y_in[0:]; y_30 = y_30[0:]; y_1y = y_1y[0:];
        print datetime.datetime.now().time().isoformat() + ". translate hour "+str(j)+" data."



    # Step1-3: Train Time-varying Topic Model.
        svr_in = SVR(C=1.0, epsilon=0.2);    svr_in.fit(X[:,range(3,53)], y_in);
        joblib.dump(svr_in, path + "svr_in/Time-varying Topic Model " + str(j/12) + ".pkl")
        svr_30 = SVR(C=1.0, epsilon=0.2);    svr_30.fit(X[:,range(3,53)], y_30);
        joblib.dump(svr_30, path + "svr_30/Time-varying Topic Model " + str(j/12) + ".pkl")
        svr_1y = SVR(C=1.0, epsilon=0.2);    svr_1y.fit(X[:,range(3,53)], y_1y);
        joblib.dump(svr_1y, path + "svr_1y/Time-varying Topic Model " + str(j/12) + ".pkl")
        print datetime.datetime.now().time().isoformat() + ". train Time-varying Topic Model. hour "+str(j)+"."



    # Step1-4: Train Combined Time-varying Model.
        svr_in = SVR(C=1.0, epsilon=0.2);    svr_in.fit(X, y_in);
        joblib.dump(svr_in, path + "svr_in/Combined Time-varying Model " + str(j/12) + ".pkl")
        svr_30 = SVR(C=1.0, epsilon=0.2);    svr_30.fit(X, y_30);
        joblib.dump(svr_30, path + "svr_30/Combined Time-varying Model " + str(j/12) + ".pkl")
        svr_1y = SVR(C=1.0, epsilon=0.2);    svr_1y.fit(X, y_1y);
        joblib.dump(svr_1y, path + "svr_1y/Combined Time-varying Model " + str(j/12) + ".pkl")
        print datetime.datetime.now().time().isoformat() + ". train Combined Time-varying Model. hour "+str(j)+"."


# Step2: Train Other Model.
    print datetime.datetime.now().time().isoformat() + ". Step2: Train Other Model."
    # Step2-1: Get outcome, retrospective data.
    text = "Select count(*) from "+ update_table + " Where lda_"+str(i)+"_all is null;"
    get_cur.execute(text)
    checktable = get_cur.fetchall()
    length_check =len(checktable)

    if checktable[0][0] == 0L:
        train_text  = "Select death_inhosp, death_30, death_1year, age, Case When gender = 'F' then 0 else 1 end as gender, first_sapsii, lda_" + str(i) + "_all, "
        train_text += "min_sapsii, max_sapsii, final_sapsii, "
        train_text += "eh_congestive_heart_failure, eh_cardiac_arrhythmias, eh_valvular_disease, "
        train_text += "eh_pulmonary_circulation, eh_peripheral_vascular, eh_hypertension, "
        train_text += "eh_paralysis, eh_other_neurological, eh_chronic_pulmonary, "
        train_text += "eh_diabetes_uncomplicated, eh_diabetes_complicated, eh_hypothyroidism, "
        train_text += "eh_renal_failure, eh_liver_disease, eh_peptic_ulcer, "
        train_text += "eh_aids, eh_lymphoma, eh_metastatic_cancer, "
        train_text += "eh_solid_tumor, eh_rheumatoid_arthritis, eh_coagulopathy, "
        train_text += "eh_obesity, eh_weight_loss, eh_fluid_electrolyte, "
        train_text += "eh_blood_loss_anemia, eh_deficiency_anemias, eh_alcohol_abuse, "
        train_text += "eh_drug_abuse, eh_psychoses, eh_depression "
        train_text += "from new_table "
        train_text += "Where train = 1 and lda_" + str(i) + "_all not like 'No notes';"

        get_cur.execute(train_text)
        traintable = get_cur.fetchall()
        length_use = len(traintable)
    print datetime.datetime.now().time().isoformat() + ". Get retrospective data. length = "+str(length_use)

    # Step2-2: Translate outcome, retrospective data into numpy format.
    X = np.zeros((1, 86));
    y_in = np.zeros((1, 0));
    y_30 = np.zeros((1, 0));
    y_1y = np.zeros((1, 0));

    for row in traintable:
        X = np.vstack((X, np.array(map(np.float64, [row[3], row[4], row[5]] + list(row[7:40]) + row[6].split()))))
        y_in = np.append(y_in, np.float64(row[0]))
        y_30 = np.append(y_30, np.float64(row[1]))
        y_1y = np.append(y_1y, np.float64(row[2]))

    X = X[1:];
    y_in = y_in[0:];
    y_30 = y_30[0:];
    y_1y = y_1y[0:];
    print datetime.datetime.now().time().isoformat() + ". translate retrospective data."

    # Step2-3: Train Admission Baseline Model.
    svr_in = SVR(C=1.0, epsilon=0.2);
    svr_in.fit(X[:, range(0, 3)], y_in);
    joblib.dump(svr_in, path + "svr_in/Admission Baseline Model.pkl")
    svr_30 = SVR(C=1.0, epsilon=0.2);
    svr_30.fit(X[:, range(0, 3)], y_30);
    joblib.dump(svr_30, path + "svr_30/Admission Baseline Model.pkl")
    svr_1y = SVR(C=1.0, epsilon=0.2);
    svr_1y.fit(X[:, range(0, 3)], y_1y);
    joblib.dump(svr_1y, path + "svr_1y/Admission Baseline Model.pkl")
    print datetime.datetime.now().time().isoformat() + ". Train Admission Baseline Model."


    # Step2-4: Train Retrospective Derived Feature Model.
    svr_in = SVR(C=1.0, epsilon=0.2);
    svr_in.fit(X[:, range(0, 36)], y_in);
    joblib.dump(svr_in, path + "svr_in/Retrospective Derived Feature Model.pkl")
    svr_30 = SVR(C=1.0, epsilon=0.2);
    svr_30.fit(X[:, range(0, 36)], y_30);
    joblib.dump(svr_30, path + "svr_30/Retrospective Derived Feature Model.pkl")
    svr_1y = SVR(C=1.0, epsilon=0.2);
    svr_1y.fit(X[:, range(0, 36)], y_1y);
    joblib.dump(svr_1y, path + "svr_1y/Retrospective Derived Feature Model.pkl")
    print datetime.datetime.now().time().isoformat() + ". Retrospective Derived Feature Model."

    # Step2-5: Train Retrospective Topic Model.
    svr_in = SVR(C=1.0, epsilon=0.2);
    svr_in.fit(X[:, range(36, 86)], y_in);
    joblib.dump(svr_in, path + "svr_in/Retrospective Topic Model.pkl")
    svr_30 = SVR(C=1.0, epsilon=0.2);
    svr_30.fit(X[:, range(36, 86)], y_30);
    joblib.dump(svr_30, path + "svr_30/Retrospective Topic Model.pkl")
    svr_1y = SVR(C=1.0, epsilon=0.2);
    svr_1y.fit(X[:, range(36, 86)], y_1y);
    joblib.dump(svr_1y, path + "svr_1y/Retrospective Topic Model.pkl")
    print datetime.datetime.now().time().isoformat() + ". Retrospective Topic Model."

    # Step2-6: Train Retrospective Topic and Admission Model.
    svr_in = SVR(C=1.0, epsilon=0.2);
    svr_in.fit(X[:, range(0, 3)+range(36, 86)], y_in);
    joblib.dump(svr_in, path + "svr_in/Retrospective Topic and Admission Model.pkl")
    svr_30 = SVR(C=1.0, epsilon=0.2);
    svr_30.fit(X[:, range(0, 3)+range(36, 86)], y_30);
    joblib.dump(svr_30, path + "svr_30/Retrospective Topic and Admission Model.pkl")
    svr_1y = SVR(C=1.0, epsilon=0.2);
    svr_1y.fit(X[:, range(0, 3)+range(36, 86)], y_1y);
    joblib.dump(svr_1y, path + "svr_1y/Retrospective Topic and Admission Model.pkl")
    print datetime.datetime.now().time().isoformat() + ". Retrospective Topic and Admission Model."

    # Step2-7: Train Retrospective Topic and Derived Feature Model.
    svr_in = SVR(C=1.0, epsilon=0.2);
    svr_in.fit(X[:, range(0, 86)], y_in);
    joblib.dump(svr_in, path + "svr_in/Retrospective Topic and Derived Feature Model.pkl")
    svr_30 = SVR(C=1.0, epsilon=0.2);
    svr_30.fit(X[:, range(0, 86)], y_30);
    joblib.dump(svr_30, path + "svr_30/Retrospective Topic and Derived Feature Model.pkl")
    svr_1y = SVR(C=1.0, epsilon=0.2);
    svr_1y.fit(X[:, range(0, 86)], y_1y);
    joblib.dump(svr_1y, path + "svr_1y/Retrospective Topic and Derived Feature Model.pkl")
    print datetime.datetime.now().time().isoformat() + ". Retrospective Topic and Derived Feature Model."


print 'end'

