find . -type f -exec cat {} + > mergedfile
sed '/log/d' -i mergedfile.csv 