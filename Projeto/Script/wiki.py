import json
import boto3

my_stream_name = 'WikiStream'
thing_id = 'wiki-bot'
kinesis_client = boto3.client('firehose', region_name='us-east-1')

from sseclient import SSEClient as EventSource
domains = ['pt.wikipedia.org','en.wikipedia.org']
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
                print('BOT: {bot} ----- USER: {user} ----- TITLE: {title}'.format(**change))
                response = kinesis_client.put_record(
                    DeliveryStreamName='WikiStream',
                    Record={
                        'Data': json.dumps(str(event).replace('$schema','schema'))
                    }
                )

                print(response)