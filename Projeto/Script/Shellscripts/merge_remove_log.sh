
#Cria pasta temporária
mkdir /tmp/csv_file
cd /tmp/csv_file

#Copiar arquivos do S3
aws s3 cp s3://wikibot/wikidata/2020/ . --recursive

#Junta todos arquivos em um só
find . -type f -exec cat {} + > mergedfile.csv
 
#Cria pasta no Hadoop e copia o arquivo CSV
hadoop fs -mkdir -p wikibot/csv_data
hadoop fs -put mergedfile.csv wikibot/csv_data