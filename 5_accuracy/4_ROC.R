library(RPostgreSQL)
library(ROCR)

con = dbConnect(PostgreSQL(), user= "w10403323", password="terence", dbname="mimiciii")

pred_type=c("admission_baseline",
           "time_varying_topic_1",
           "time_varying_topic_10",
           "time_varying_topic_20",
           "combined_time_varying_1",
           "combined_time_varying_10",
           "combined_time_varying_20",
           "retrospective_derived_feature",
           "retrospective_topic",
           "retrospective_topic_and_admission",
           "retrospective_topic_and_derived_feature")

AUC=c()
for (i in 1:11){
    
    SQL_data= dbGetQuery(con, statement = paste(
      "Select death, ",pred_type[i] ," from accuracy 
      where death_type = 'inhosp' and train = 1 and ",pred_type[i] ," not like 'leave'"))
    ROC_data =as.data.frame(cbind(as.numeric(SQL_data[,1]), as.numeric(SQL_data[,2])))
    colnames(ROC_data) = c("reals", "predictions")
    
    pred <- prediction( ROC_data$predictions, ROC_data$reals)
    perf <- performance(pred,"tpr","fpr")
    plot(perf)
    
    #perf1 <- performance(pred, "sens", "spec")
    #plot(perf1)
    
    AUC=c(AUC,unlist(slot(performance(pred,"auc"), "y.values")))
    }
AUC
