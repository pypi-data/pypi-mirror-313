SELECT DRILLHOLE_NO AS dh_no,
       READING_DATE AS reading_date,
       BATTERY_PERCENTAGE AS battery_pct,
       MEMORY_PERCENTAGE AS memory_pct,
       COMMENT AS comments,
       CreatedBy AS read_by
FROM   WDE_Extended.dbo.Logger_Data
WHERE  DRILLHOLE_NO IN {DH_NO}
