import json
import datetime
import os
import urllib.parse
from botocore.vendored import requests


def respond(message):
    return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": None,
            "body": json.dumps(message)
        }


def wormly_uptime(hostid, startday, endday):
    key = os.getenv('APIkey')
    my_response = requests.get(
        'https://api.wormly.com/',
        params={
            'key': key,
            'response': 'json',
            'cmd': 'getDailyUptimeReport',
            'hostid': hostid,
            'startday': startday,
            'endday': endday
        }
    )

    if my_response.status_code == 200:
        json_data = json.loads(my_response.content)
        list_secs = map(lambda x: int(x['downseconds']), json_data['dailyuptime'])
        total_down_seconds = sum(list_secs)

        start_date = datetime.datetime.strptime(startday, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(endday, '%Y-%m-%d').date()
        total_seconds = int((end_date - start_date).days) * 60 * 60 * 24

        total_uptime_seconds = total_seconds - total_down_seconds
        return ({
            "hostid": hostid,
            "details": {
                "downtime": {
                    "Pretty": str(datetime.timedelta(seconds=total_down_seconds)),
                    "Seconds": total_down_seconds,
                    "Percent": total_down_seconds / total_seconds
                },
                "uptime": {
                    "Pretty": str(datetime.timedelta(seconds=total_uptime_seconds)),
                    "Seconds": total_uptime_seconds,
                    "Percent": total_uptime_seconds / total_seconds
                }
            }
        })
    else:
        return {
            "isBase64Encoded": False,
            'statusCode': my_response.status_code,
            'header': None,
            'body': 'API Connection Error'
        }


def lambda_handler(event, context):
    hosts = event['multiValueQueryStringParameters']['hostid']
    startday = urllib.parse.quote(event['queryStringParameters']['startday'])
    endday = urllib.parse.quote(event['queryStringParameters']['endday'])

    message = []
    for host in hosts:
        message.append(wormly_uptime(urllib.parse.quote(host), startday, endday))

    return respond(message)
