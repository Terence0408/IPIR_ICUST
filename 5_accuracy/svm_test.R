library(RPostgreSQL)
library(ROCR)
library(e1071)

con = dbConnect(PostgreSQL(), user= "w10403323", password="terence", dbname="mimiciii")

hour="12"
Retrospective = 0



all_table   = dbGetQuery(con, statement = paste("Select death_1year, age, Case When gender = 'F' then 0 else 1 end as gender,
                                                 first_sapsii, min_sapsii, max_sapsii, final_sapsii, 
                                                 lda_50_",hour,", lda_50_all,
                                                 eh_congestive_heart_failure, 
                                                 eh_cardiac_arrhythmias, 
                                                 eh_valvular_disease, 
                                                 eh_pulmonary_circulation, 
                                                 eh_peripheral_vascular, 
                                                 eh_hypertension, 
                                                 eh_paralysis, 
                                                 eh_other_neurological, 
                                                 eh_chronic_pulmonary, 
                                                 eh_diabetes_uncomplicated, 
                                                 eh_diabetes_complicated, 
                                                 eh_hypothyroidism, 
                                                 eh_renal_failure, 
                                                 eh_liver_disease, 
                                                 eh_peptic_ulcer, 
                                                 eh_aids, 
                                                 eh_lymphoma, 
                                                 eh_metastatic_cancer, 
                                                 eh_solid_tumor, 
                                                 eh_rheumatoid_arthritis, 
                                                 eh_coagulopathy, 
                                                 eh_obesity, 
                                                 eh_weight_loss, 
                                                 eh_fluid_electrolyte, 
                                                 eh_blood_loss_anemia, 
                                                 eh_deficiency_anemias, 
                                                 eh_alcohol_abuse, 
                                                 eh_drug_abuse, 
                                                 eh_psychoses, 
                                                 eh_depression, train 
                                                 from new_table
                                                 where staytime > ", hour, ";", sep = ""))

death = as.numeric(all_table$death_1year)
age = all_table$age
gender = as.numeric(all_table$gender)
first_sapsii = as.numeric(all_table$first_sapsii)
min_sapsii = as.numeric(all_table$min_sapsii)
max_sapsii = as.numeric(all_table$max_sapsii)
final_sapsii = as.numeric(all_table$final_sapsii)
eh_congestive_heart_failure = as.numeric(all_table$eh_congestive_heart_failure)
eh_cardiac_arrhythmias = as.numeric(all_table$eh_cardiac_arrhythmias)
eh_valvular_disease = as.numeric(all_table$eh_valvular_disease)
eh_pulmonary_circulation = as.numeric(all_table$eh_pulmonary_circulation)
eh_peripheral_vascular = as.numeric(all_table$eh_peripheral_vascular)
eh_hypertension = as.numeric(all_table$eh_hypertension)
eh_paralysis = as.numeric(all_table$eh_paralysis)
eh_other_neurological = as.numeric(all_table$eh_other_neurological)
eh_chronic_pulmonary = as.numeric(all_table$eh_chronic_pulmonary)
eh_diabetes_uncomplicated = as.numeric(all_table$eh_diabetes_uncomplicated)
eh_diabetes_complicated = as.numeric(all_table$eh_diabetes_complicated)
eh_hypothyroidism = as.numeric(all_table$eh_hypothyroidism)
eh_renal_failure = as.numeric(all_table$eh_renal_failure)
eh_liver_disease = as.numeric(all_table$eh_liver_disease)
eh_peptic_ulcer = as.numeric(all_table$eh_peptic_ulcer)
eh_aids = as.numeric(all_table$eh_aids)
eh_lymphoma = as.numeric(all_table$eh_lymphoma)
eh_metastatic_cancer = as.numeric(all_table$eh_metastatic_cancer)
eh_solid_tumor = as.numeric(all_table$eh_solid_tumor)
eh_rheumatoid_arthritis = as.numeric(all_table$eh_rheumatoid_arthritis)
eh_coagulopathy = as.numeric(all_table$eh_coagulopathy)
eh_obesity = as.numeric(all_table$eh_obesity)
eh_weight_loss = as.numeric(all_table$eh_weight_loss)
eh_fluid_electrolyte = as.numeric(all_table$eh_fluid_electrolyte)
eh_blood_loss_anemia = as.numeric(all_table$eh_blood_loss_anemia)
eh_deficiency_anemias = as.numeric(all_table$eh_deficiency_anemias)
eh_alcohol_abuse = as.numeric(all_table$eh_alcohol_abuse)
eh_drug_abuse = as.numeric(all_table$eh_drug_abuse)
eh_psychoses = as.numeric(all_table$eh_psychoses)
eh_depression = as.numeric(all_table$eh_depression)
train = as.numeric(all_table$train)

text_data = as.data.frame(strsplit(all_table[,Retrospective+8], " "))
lda_01 = as.numeric(as.character(text_data[ 1,]))
lda_02 = as.numeric(as.character(text_data[ 2,]))
lda_03 = as.numeric(as.character(text_data[ 3,]))
lda_04 = as.numeric(as.character(text_data[ 4,]))
lda_05 = as.numeric(as.character(text_data[ 5,]))
lda_06 = as.numeric(as.character(text_data[ 6,]))
lda_07 = as.numeric(as.character(text_data[ 7,]))
lda_08 = as.numeric(as.character(text_data[ 8,]))
lda_09 = as.numeric(as.character(text_data[ 9,]))
lda_10 = as.numeric(as.character(text_data[10,]))
lda_11 = as.numeric(as.character(text_data[11,]))
lda_12 = as.numeric(as.character(text_data[12,]))
lda_13 = as.numeric(as.character(text_data[13,]))
lda_14 = as.numeric(as.character(text_data[14,]))
lda_15 = as.numeric(as.character(text_data[15,]))
lda_16 = as.numeric(as.character(text_data[16,]))
lda_17 = as.numeric(as.character(text_data[17,]))
lda_18 = as.numeric(as.character(text_data[18,]))
lda_19 = as.numeric(as.character(text_data[19,]))
lda_20 = as.numeric(as.character(text_data[20,]))
lda_21 = as.numeric(as.character(text_data[21,]))
lda_22 = as.numeric(as.character(text_data[22,]))
lda_23 = as.numeric(as.character(text_data[23,]))
lda_24 = as.numeric(as.character(text_data[24,]))
lda_25 = as.numeric(as.character(text_data[25,]))
lda_26 = as.numeric(as.character(text_data[26,]))
lda_27 = as.numeric(as.character(text_data[27,]))
lda_28 = as.numeric(as.character(text_data[28,]))
lda_29 = as.numeric(as.character(text_data[29,]))
lda_30 = as.numeric(as.character(text_data[30,]))
lda_31 = as.numeric(as.character(text_data[31,]))
lda_32 = as.numeric(as.character(text_data[32,]))
lda_33 = as.numeric(as.character(text_data[33,]))
lda_34 = as.numeric(as.character(text_data[34,]))
lda_35 = as.numeric(as.character(text_data[35,]))
lda_36 = as.numeric(as.character(text_data[36,]))
lda_37 = as.numeric(as.character(text_data[37,]))
lda_38 = as.numeric(as.character(text_data[38,]))
lda_39 = as.numeric(as.character(text_data[39,]))
lda_40 = as.numeric(as.character(text_data[40,]))
lda_41 = as.numeric(as.character(text_data[41,]))
lda_42 = as.numeric(as.character(text_data[42,]))
lda_43 = as.numeric(as.character(text_data[43,]))
lda_44 = as.numeric(as.character(text_data[44,]))
lda_45 = as.numeric(as.character(text_data[45,]))
lda_46 = as.numeric(as.character(text_data[46,]))
lda_47 = as.numeric(as.character(text_data[47,]))
lda_48 = as.numeric(as.character(text_data[48,]))
lda_49 = as.numeric(as.character(text_data[49,]))
lda_50 = as.numeric(as.character(text_data[50,]))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
all_data = as.data.frame(cbind(death, age, gender, first_sapsii, min_sapsii, max_sapsii, final_sapsii, lda_01, lda_02, lda_03, 
                                 lda_04, lda_05, lda_06, lda_07, lda_08, lda_09, lda_10, lda_11, lda_12, lda_13, 
                                 lda_14, lda_15, lda_16, lda_17, lda_18, lda_19, lda_20, lda_21, lda_22, lda_23, 
                                 lda_24, lda_25, lda_26, lda_27, lda_28, lda_29, lda_30, lda_31, lda_32, lda_33, 
                                 lda_34, lda_35, lda_36, lda_37, lda_38, lda_39, lda_40, lda_41, lda_42, lda_43, 
                                 lda_44, lda_45, lda_46, lda_47, lda_48, lda_49, lda_50, eh_congestive_heart_failure, eh_cardiac_arrhythmias, eh_valvular_disease, 
                                 eh_pulmonary_circulation, eh_peripheral_vascular, 	eh_hypertension, 	eh_paralysis, 	eh_other_neurological, 	eh_chronic_pulmonary, 	eh_diabetes_uncomplicated, 	eh_diabetes_complicated, 	eh_hypothyroidism, 	eh_renal_failure, 	
                                 eh_liver_disease, 	eh_peptic_ulcer, 	eh_aids, 	eh_lymphoma, 	eh_metastatic_cancer, 	eh_solid_tumor, 	eh_rheumatoid_arthritis, 	eh_coagulopathy, 	eh_obesity, 	eh_weight_loss, 	
                                 eh_fluid_electrolyte, 	eh_blood_loss_anemia, 	eh_deficiency_anemias, 	eh_alcohol_abuse, 	eh_drug_abuse, 	eh_psychoses, 	eh_depression, train))

train_data = all_data[which(all_data$train==1),]
test_data = all_data[which(all_data$train==0),]



#tuneResult <- tune(svm, death ~., data=train_data, validation.x = test_data[,2:54], validation.y= test_data$death,
#                   ranges = list(epsilon = seq(0,0.5,0.1)))


svm_model = svm(death ~., epsilon=0.2, data=train_data[,1:4]) # 3
log_model=glm(death ~.,family=binomial(link='logit'),data=train_data[,c(1:4)]) # 3

svm_model = svm(death ~., epsilon=0.2, data=train_data[,c(1,8:57)]) # 50
log_model=glm(death ~.,family=binomial(link='logit'),data=train_data[,c(1,8:57)]) # 50

svm_model = svm(death ~., epsilon=0.2, data=train_data[,c(1:4,8:57)]) # 53
log_model=glm(death ~.,family=binomial(link='logit'),data=train_data[,c(1:4,8:57)]) # 53

svm_model = svm(death ~., epsilon=0.2, data=train_data[,c(1,58:87)]) # 36
log_model=glm(death ~.,family=binomial(link='logit'),data=train_data[,c(1,58:87)]) # 36

svm_model = svm(death ~., epsilon=0.2, data=train_data[,c(1:87)]) # 86
log_model=glm(death ~.,family=binomial(link='logit'),data=train_data[,c(1:87)]) # 86




test_prediction = predict(svm_model, test_data)
test_pred <- prediction( test_prediction, test_data$death)
test_AUC=unlist(slot(performance(test_pred,"auc"), "y.values"));
train_prediction = predict(svm_model, train_data)
train_pred <- prediction( train_prediction, train_data$death)
train_AUC=unlist(slot(performance(train_pred,"auc"), "y.values"));
c(test_AUC,train_AUC)


test_prediction = predict(log_model, test_data, type='response')
test_pred <- prediction( test_prediction, test_data$death)
test_AUC=unlist(slot(performance(test_pred,"auc"), "y.values"));
train_prediction = predict(log_model, train_data, type='response')
train_pred <- prediction( train_prediction, train_data$death)
train_AUC=unlist(slot(performance(train_pred,"auc"), "y.values"));
c(test_AUC,train_AUC)



perf <- performance(pred,"tpr","fpr")
plot(perf)
perf1 <- performance(pred, "sens", "spec")
plot(perf1)
