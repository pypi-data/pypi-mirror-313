SELECT DrillholeNo AS dh_no,
       DateCreated AS creation_date,
       Active AS active,
       Description AS description,
       CreatedBy AS created_by,
       ModifiedBy AS modified_by,
       DateModified AS modified_date
FROM   WDE_Extended.dbo.Alerts
WHERE  DrillholeNo IN {DH_NO}