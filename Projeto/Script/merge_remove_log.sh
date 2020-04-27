mkdir /tmp/csv_file
cd /tmp/csv_file

aws s3 cp s3://wikibot/wikidata/2020/ . --recursive

find . -type f -exec cat {} + > mergedfile
sed '/log/d' -i mergedfile.csv 
hadoop fs -put mergedfile.csv wikibot/csv_data