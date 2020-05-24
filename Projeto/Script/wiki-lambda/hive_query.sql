
--CRIA SCHEMA E TABELA DA RAW
CREATE SCHEMA IF NOT EXISTS raw;

CREATE EXTERNAL TABLE IF NOT EXISTS raw.wikidata
(schema STRING, wiki_id STRING, type STRING, namespace STRING, title STRING, comment STRING, wiki_timestamp STRING, wiki_user STRING, bot STRING, minor STRING, patrolled STRING, server_url STRING, server_name STRING, server_script_path STRING, wiki STRING, parsedcomment STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'hdfs://ip-172-31-90-192.ec2.internal:8020/user/root/wikibot/csv_data';

--CRIA SCHEMA E TABELA DEFINED
CREATE SCHEMA IF NOT EXISTS defined;

CREATE EXTERNAL TABLE IF NOT EXISTS defined.wikidata
(wiki_id STRING, title STRING, wiki_timestamp STRING, wiki_user STRING, bot STRING);

INSERT INTO table defined.wikidata SELECT wiki_id, title, wiki_timestamp, wiki_user, bot FROM raw.wikidata;

SELECT * FROM raw.wikidata LIMIT 100;
SELECT * FROM defined.wikidata LIMIT 100;