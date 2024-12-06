SELECT DRILLHOLE_NO AS dh_no,
       DATE_INSTALLED as install_date,
       TYPE as type,
       MODEL as model,
       SERIAL_NO as serial_no,
       TELEMETRY as telemetry,
       COMMENT as comments
FROM   WDE_Extended.dbo.Logger
WHERE  DRILLHOLE_NO IN {DH_NO}