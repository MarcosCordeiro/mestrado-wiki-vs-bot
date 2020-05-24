import json
import boto3
import csv, sys
from sseclient import SSEClient as EventSource

my_stream_name = 'WikiStream'
kinesis_client = boto3.client('firehose', region_name='us-east-1', aws_access_key_id='AKIAR3CZLWEYF7GITSGS' ,aws_secret_access_key='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')
domains = ['pt.wikipedia.org']
url = 'https://stream.wikimedia.org/v2/stream/recentchange'
TIPO_GRAVACAO = "local"
fileOutput = "/csv_output/local.csv"

def gravarKinesis(dataStream):
    response = kinesis_client.put_record(
        DeliveryStreamName='WikiStream',
        Record={
            'Data': str(event).replace('$schema','schema')
        }
    )

    print(response)

def gravarLocal(dataStream):
    listFields = readJson(dataStream)

    with open(fileOutput, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(listFields)
    
    print(listFields)


def readJson(dataStream):
    listValues=[]
    for key, value in dataStream.items():
        if isinstance(value, dict):
            readJson(value)
        else:
            if isinstance(value, str):
                listValues.append(value.replace(',','').replace('\'','').replace('\n', ' ').replace('\r', ''))
            else:
                listValues.append(value)
    return listValues
    


for event in EventSource(url):

    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
            if(change['meta']['domain'] in domains ):
                #print(event)
                if(TIPO_GRAVACAO=="local"):
                    gravarLocal(change)
                elif(TIPO_GRAVACAO=="kinesis"):
                    gravarKinesis(event)

               
                
