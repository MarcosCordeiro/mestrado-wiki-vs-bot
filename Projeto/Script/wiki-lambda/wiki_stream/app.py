import base64
import json
from decimal import Decimal

def lambda_handler(event, context):
    output = []

    for record in event['records'] :
        print(record['recordId'])
        payload = base64.b64decode(record['data']).decode('utf-8')
        print(payload)
        #reading = json.loads(payload)
        #print(reading)
        
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': 'e+KAnHN0YXRpb27igJ064oCdQTHigLMs4oCddGVtcOKAnTrigJ02NjZG4oCdfQ=='
        }
        output.append(output_record)

    print('Processed {} records.'.format(len(event['records'])))

    return {'records': output}