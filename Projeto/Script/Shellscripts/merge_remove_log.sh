#!/bin/bash

mkdir /tmp/csv_file
cd /tmp/csv_file

aws s3 cp s3://wikibot/wikidata/2020/ . --recursive

aws s3 mv s3://wikibot/wikidata/2020/ s3://wikibot/wikidata/old/ --recursive

find . -type f -exec cat {} + > mergedfile.csv
sed '/log/d' -i mergedfile.csv 
hadoop fs -put mergedfile.csv wikibot/csv_data