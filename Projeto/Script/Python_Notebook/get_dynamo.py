import boto3
import json
import decimal
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def query_dynamodb(bot):
    MY_ACCESS_KEY_ID = 'AKIAR3CZLWEYF7GITSGS'
    MY_SECRET_ACCESS_KEY = '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'
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=MY_ACCESS_KEY_ID, aws_secret_access_key=MY_SECRET_ACCESS_KEY, region_name='us-east-1')
    table = dynamodb.Table('wikibot-title_cleaned')
    
    df = pd.DataFrame()
    try:
        response = table.scan(
            FilterExpression = Attr('bot').eq(bot)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        itemsList = []
        for i in response[u'Items']:
            itemsList += response['Items']
            df = pd.DataFrame(itemsList)
        
    return df

title_bot_true = query_dynamodb('True')
title_bot_false = query_dynamodb('False')
print(title_bot_false)