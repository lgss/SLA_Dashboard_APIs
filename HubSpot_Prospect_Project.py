import json
import os
import requests


def respond(message):
    return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": None,
            "body": json.dumps(message)
        }


def prospect_to_project():
    key = os.getenv('hubAPI')
    my_response = requests.get(
        'https://api.hubapi.com/deals/v1/deal/paged',
        params={
            'properties': 'dealstage',
            'hapikey': key
        }
    )
    resp = json.loads(my_response.content)["deals"]
    total = len(resp)

    blocked = 0
    failure = 0

    for deal in resp:
        if deal["properties"]["dealstage"]["value"] == '649208':
            blocked += 1
        elif deal["properties"]["dealstage"]["value"] == 'closedlost':
            failure += 1

    return {
        'totalProjects': total,
        'abandonedProjects': failure,
        'inDelivery': total - blocked,
        'inDeliveryPercent': 1 - (failure / (total - blocked))
    }


def lambda_handler(event, context):
    return respond(prospect_to_project())
