// simple query for observing changes in Athena when producer script is streaming new data to S3

SELECT
       sensor_id
     , MIN(event_dt) first_m_dt
     , MAX(event_dt) last_m_dt
     , COUNT(*)      m_count
FROM temperature_measurements
GROUP BY sensor_id;
