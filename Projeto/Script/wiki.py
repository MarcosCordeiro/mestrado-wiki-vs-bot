import json
import boto3
from sseclient import SSEClient as EventSource

my_stream_name = 'WikiStream'
kinesis_client = boto3.client('firehose', region_name='us-east-1', aws_access_key_id='AKIAR3CZLWEYF7GITSGS' ,aws_secret_access_key='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')
domains = ['pt.wikipedia.org']
url = 'https://stream.wikimedia.org/v2/stream/recentchange'

for event in EventSource(url):

    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
            if(change['meta']['domain'] in domains ):
                print(event)
                response = kinesis_client.put_record(
                    DeliveryStreamName='WikiStream',
                    Record={
                        'Data': str(event).replace('$schema','schema')
                    }
                )

                print(response)