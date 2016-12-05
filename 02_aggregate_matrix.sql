Create table aggregate_matrix as
WITH  dem as(
Select dem.subject_id, dem.hadm_id, 
    dem.admittime, dem.dischtime, dem.dod ,
    EXTRACT(DAY FROM (dem.dischtime  - dem.admittime))*24+EXTRACT(HOUR FROM (dem.dischtime  - dem.admittime))   as staytime,
    Case When dem.deathtime is not NULL THEN 1 else 0 end as death_inhosp,
    Case When dem.deathtime is NULL and EXTRACT(DAY FROM (dem.dod - dem.admittime)) between  0 and  30 then 1 Else 0 end as death_30,
    Case When dem.deathtime is NULL and EXTRACT(DAY FROM (dem.dod - dem.admittime)) between  0 and  30 then 0 
        When dem.deathtime is NULL and EXTRACT(DAY FROM (dem.dod - dem.admittime)) between 30 and 365 then 1  ELSE  0 end as death_1year,
    dem.age, dem.gender, saps.first_sapsii, saps.min_sapsii, saps.max_sapsii, saps.final_sapsii
FROM demographic as dem inner join sapsii_use as saps on dem.subject_id =saps.subject_id and dem.hadm_id = saps.hadm_id
Where dem.age >= 18
)
Select dem.*, 
	eh.congestive_heart_failure as eh_congestive_heart_failure,
	    eh.cardiac_arrhythmias as eh_cardiac_arrhythmias,
    eh.valvular_disease as eh_valvular_disease,
    eh.pulmonary_circulation as eh_pulmonary_circulation,
    eh.peripheral_vascular as eh_peripheral_vascular,
    eh.hypertension as eh_hypertension,
    eh.paralysis as eh_paralysis,
    eh.other_neurological as eh_other_neurological,
    eh.chronic_pulmonary as eh_chronic_pulmonary,
    eh.diabetes_uncomplicated as eh_diabetes_uncomplicated,
    eh.diabetes_complicated as eh_diabetes_complicated,
    eh.hypothyroidism as eh_hypothyroidism,
    eh.renal_failure as eh_renal_failure,
    eh.liver_disease as eh_liver_disease,
    eh.peptic_ulcer as eh_peptic_ulcer,
    eh.aids as eh_aids,
    eh.lymphoma as eh_lymphoma,
    eh.metastatic_cancer as eh_metastatic_cancer,
    eh.solid_tumor as eh_solid_tumor,
    eh.rheumatoid_arthritis as eh_rheumatoid_arthritis,
    eh.coagulopathy as eh_coagulopathy,
    eh.obesity as eh_obesity,
    eh.weight_loss as eh_weight_loss,
    eh.fluid_electrolyte as eh_fluid_electrolyte,
    eh.blood_loss_anemia as eh_blood_loss_anemia,
    eh.deficiency_anemias as eh_deficiency_anemias,
    eh.alcohol_abuse as eh_alcohol_abuse,
    eh.drug_abuse as eh_drug_abuse,
    eh.psychoses as eh_psychoses,
    eh.depression as eh_depression
FROM dem inner join elixhauser_ahrq as eh on dem.subject_id =eh.subject_id and dem.hadm_id = eh.hadm_id
