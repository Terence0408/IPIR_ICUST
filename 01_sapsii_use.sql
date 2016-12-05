



CREATE TABLE sapsii_use AS 
WITH sapsii_valid AS (
	WITH dem AS (
		SELECT subject_id, hadm_id, CASE WHEN deathtime IS NULL THEN dischtime ELSE deathtime END AS leavetime
		FROM admissions
		),

	icu AS(
		SELECT icu.subject_id, icu.hadm_id, icu.icustay_id, icu.intime, saps.sapsii
		FROM public.icustays as icu left join w10403323.sapsii as saps on  icu.subject_id = saps.subject_id and  icu.hadm_id = saps.hadm_id and  icu.icustay_id = saps.icustay_id
		)
	Select icu.subject_id, icu.hadm_id, icu.intime, icu.sapsii
	FROM icu left join dem on icu.subject_id = dem.subject_id and icu.hadm_id = dem.hadm_id
	WHERE icu.intime <= dem.leavetime
	),
     sapsii_first AS (
	WITH first_sapsii_temp AS 
		(Select subject_id, hadm_id, min(intime) as min_time
		FROM sapsii_valid
		GROUP BY subject_id, hadm_id)
	
	SELECT val.subject_id, val.hadm_id, val.sapsii as first_sapsii
	FROM sapsii_valid as val right join first_sapsii_temp as tmp on val.subject_id = tmp.subject_id and val.hadm_id = tmp.hadm_id and val.intime = tmp.min_time
	),
     sapsii_final AS (
	WITH final_sapsii_temp AS 
		(Select subject_id, hadm_id, max(intime) as max_time
		FROM sapsii_valid
		GROUP BY subject_id, hadm_id)
	
	SELECT val.subject_id, val.hadm_id, val.sapsii as final_sapsii
	FROM sapsii_valid as val right join final_sapsii_temp as tmp on val.subject_id = tmp.subject_id and val.hadm_id = tmp.hadm_id and val.intime = tmp.max_time
	),
     sapsii_duration AS (
	SELECT subject_id, hadm_id, max(sapsii) as max_sapsii,  min(sapsii) as min_sapsii
	FROM sapsii_valid
	GROUP BY subject_id, hadm_id)

SELECT a.subject_id, a.hadm_id, a.max_sapsii, a.min_sapsii, b.first_sapsii, c.final_sapsii
FROM sapsii_duration as a LEFT JOIN sapsii_first as b on a.subject_id = b.subject_id and a.hadm_id = b.hadm_id
                          LEFT JOIN sapsii_final as c on a.subject_id = c.subject_id and a.hadm_id = c.hadm_id

