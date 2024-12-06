SELECT drillHoleNo  AS dh_no, 
       DateReported AS reported_date,
       ReportedBy AS reported_by,
       Priority AS priority,
       MTCRequired AS comments,
       DateCompleted AS completed_date,
       ActionedBy AS actioned_by,
       ActionDetails AS action_comments,
       OtherAction AS action_other
FROM   WDE_Extended.dbo.WellMaintenanceNotes 
WHERE  drillHoleNo IN {DH_NO}