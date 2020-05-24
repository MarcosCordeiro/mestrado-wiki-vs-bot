FROM python:3.8
RUN pip install boto3 sseclient
COPY  wiki.py /wiki.py
ENTRYPOINT ["python","-u","wiki.py"]