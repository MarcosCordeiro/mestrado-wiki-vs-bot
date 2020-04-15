import base64
import json
from decimal import Decimal


def readJson(y):
    listValues=[]
    for key, value in y.items():
        if isinstance(value, dict):
            k=key
            readJson(value)
        else:
            listValues.append(value)
    return listValues

def lambda_handler(event, context):
    output = []

    for record in event['records'] :
        print(record['recordId'])
        payload = base64.b64decode(record['data']).decode('utf-8')
        print(payload)
        reading = json.loads(payload)

        csv_line = str(readJson(reading))[1:-1]

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': str(base64.b64encode(csv_line.encode("utf-8")), "utf-8")
        }
        output.append(output_record)

    print('Processed {} records.'.format(len(event['records'])))
    return {'records': output}