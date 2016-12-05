CREATE TABLE valid_noteevents  AS
SELECT note.row_id, note.subject_id, note.hadm_id, de.admittime, de.dischtime, note.chartdate, note.charttime, note.text
FROM aggregate_matrix AS de 
     LEFT JOIN public.noteevents AS note
       ON de.subject_id = note.subject_id AND de.hadm_id = note.hadm_id
WHERE de.age >= 18 AND
      ((de.dischtime > note.charttime) OR (note.charttime is NULL AND date(de.dischtime)-date(note.chartdate)>0))
ORDER BY note.subject_id, note.hadm_id, note.charttime;