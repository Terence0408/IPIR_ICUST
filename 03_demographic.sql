Create table demographic as
select ad.subject_id,ad.hadm_id,dp.gender,
   Case When date_part('year',age(ad.admittime, dp.dob))>=300 then date_part('year',age(ad.admittime, dp.dob))-210
   Else date_part('year',age(ad.admittime, dp.dob)) end as age, 
   ad.admittime,ad.dischtime, ad.deathtime,ad.hospital_expire_flag,
   dp.dob, dp.dod, dp.dod_hosp, dp.dod_ssn, dp.expire_flag
from admissions ad, patients dp where ad.subject_id = dp.subject_id
order by ad.subject_id, ad.admittime