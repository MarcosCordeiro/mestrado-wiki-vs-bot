import json
from sseclient import SSEClient as EventSource

my_stream_name = 'WikiStream'
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
                print( str(event).replace('$schema','schema'))