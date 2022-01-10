// Definition of table was manually clicked in AWS Glue.
// Below code comes from `Generate table DDL` feature.

CREATE EXTERNAL TABLE `temperature_measurements`(
  `id` string COMMENT 'from deserializer',
  `sensor_id` string COMMENT 'from deserializer',
  `temperature` float COMMENT 'from deserializer',
  `epoch` int COMMENT 'from deserializer',
  `temp_group` string COMMENT 'from deserializer',
  `event_dt` timestamp COMMENT 'from deserializer',
  `ingestion_source` string COMMENT 'from deserializer')
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'paths'='epoch,event_dt,id,ingestion_source,sensor_id,temp_group,temperature')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://simple-push-pipeline-bucket/nopartitions/'
TBLPROPERTIES (
  'classification'='json')
