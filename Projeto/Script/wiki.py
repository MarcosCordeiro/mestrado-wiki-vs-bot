import json
import pymongo

myclient = pymongo.MongoClient("mongodb://172.17.0.2:27017/")
mydb = myclient["wiki"]
mycol = mydb["articles"]



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
                r = mycol.insert_one(json.loads(str(event).replace('$schema','schema')))
                print('Inserted ID: ' + str(r.inserted_id))
