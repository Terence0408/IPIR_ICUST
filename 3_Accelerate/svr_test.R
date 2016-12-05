library(RPostgreSQL)
library(stringr)
library (e1071)
library(ROCR)

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, user= "w10403323", password="terence", dbname="mimiciii")


##### train model #####
train_data = dbGetQuery(con, "Select death_inhosp, age, first_sapsii, gender, lda_50_12 
                        from aggregate_matrix_2 
                        Where train = 1 and lda_50_12 not like 'No notes' ;")

test_data = dbGetQuery(con, "Select death_inhosp, age, first_sapsii, gender, lda_50_12 
                       from aggregate_matrix_2 
                       Where train = 0 and lda_50_12 not like 'No notes' ;")

demo_data = dbGetQuery(con, "Select death_inhosp, age, first_sapsii, gender, lda_50_12 
                       from aggregate_matrix_2 
                       Where hadm_id = 151943 and lda_50_12 not like 'No notes' ;")

##### train data #####
train = cbind(as.numeric(train_data$death_inhosp),train_data[,2:3],as.factor(train_data$gender))
texts=str_split_fixed(train_data[,5], " ", 50)

for(i in 1:50){train = cbind(train,as.numeric(texts[,i]))}
colnames(train) =c("death_inhosp", "age", "first_sapsii", "gender",'text_1','text_2','text_3','text_4','text_5','text_6','text_7','text_8','text_9','text_10','text_11','text_12','text_13','text_14','text_15','text_16','text_17','text_18','text_19','text_20','text_21','text_22','text_23','text_24','text_25','text_26','text_27','text_28','text_29','text_30','text_31','text_32','text_33','text_34','text_35','text_36','text_37','text_38','text_39','text_40','text_41','text_42','text_43','text_44','text_45','text_46','text_47','text_48','text_49','text_50')

##### test data #####
test = cbind(as.numeric(test_data$death_inhosp),test_data[,2:3],as.factor(test_data$gender))
texts=str_split_fixed(test_data[,5], " ", 50)

for(i in 1:50){test = cbind(test,as.numeric(texts[,i]))}
colnames(test) =c("death_inhosp", "age", "first_sapsii", "gender",'text_1','text_2','text_3','text_4','text_5','text_6','text_7','text_8','text_9','text_10','text_11','text_12','text_13','text_14','text_15','text_16','text_17','text_18','text_19','text_20','text_21','text_22','text_23','text_24','text_25','text_26','text_27','text_28','text_29','text_30','text_31','text_32','text_33','text_34','text_35','text_36','text_37','text_38','text_39','text_40','text_41','text_42','text_43','text_44','text_45','text_46','text_47','text_48','text_49','text_50')

##### demo data #####
demo = cbind(as.numeric(demo_data$death_inhosp),demo_data[,2:3],as.factor(demo_data$gender))
texts=str_split_fixed(demo_data[,5], " ", 50)

for(i in 1:50){demo = cbind(demo,as.numeric(texts[,i]))}
colnames(demo) =c("death_inhosp", "age", "first_sapsii", "gender",'text_1','text_2','text_3','text_4','text_5','text_6','text_7','text_8','text_9','text_10','text_11','text_12','text_13','text_14','text_15','text_16','text_17','text_18','text_19','text_20','text_21','text_22','text_23','text_24','text_25','text_26','text_27','text_28','text_29','text_30','text_31','text_32','text_33','text_34','text_35','text_36','text_37','text_38','text_39','text_40','text_41','text_42','text_43','text_44','text_45','text_46','text_47','text_48','text_49','text_50')




svr_model_1 <- svm( death_inhosp ~ ., train[,c(1:53)])
svr_model_2 <-svm( death_inhosp ~ ., train[,c(1:54)])


summary(svr_model_1)
model = svr_model_2
##### train data #####
par(mfcol=c(2,2))
pred_train = predict(model,train)

pred <- prediction( pred_train, train$death_inhosp)
perf <- performance(pred,"tpr","fpr")
plot(perf, main='train set')
auc <- performance(pred,"auc")
auc = unlist(slot(auc, "y.values"))
text(0.95,0.02,round(auc,3))
perf1 <- performance(pred, "sens", "spec")
plot(perf1)



##### test data #####
pred_test = predict(model,test)
pred <- prediction( pred_test, test$death_inhosp)
perf <- performance(pred,"tpr","fpr")
plot(perf, main='test set')
auc <- performance(pred,"auc")
auc = unlist(slot(auc, "y.values"))
text(0.95,0.02,round(auc,3))
perf1 <- performance(pred, "sens", "spec")
plot(perf1)


##### demo data #####
pred_demo =predict(model,demo)
pred_demo


