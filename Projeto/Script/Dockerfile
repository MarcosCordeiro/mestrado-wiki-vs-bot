FROM python:3
COPY wiki.py /wiki.py
RUN pip install pymongo sseclient
ENTRYPOINT ["python","-u","wiki.py"]

