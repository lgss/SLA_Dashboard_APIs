import json
import os
import urllib.parse
import urllib.request
from botocore.vendored import requests


def respond(message):
    return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": None,
            "body": json.dumps(message)
        }


def harvest_call(search):
    url = "https://api.harvestapp.com/v2/projects"
    headers = {
        "User-Agent": "Python Harvest API Sample",
        "Authorization": "Bearer " + os.environ.get("HARVEST_ACCESS_TOKEN"),
        "Harvest-Account-ID": os.environ.get("HARVEST_ACCOUNT_ID"),
        "is_active": "true"
    }

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    response_body = response.read().decode("utf-8")
    json_response = json.loads(response_body)

    filtered_response = [x for x in json_response["projects"] if search in x['notes']]

    return respond(filtered_response)


def lambda_handler(event, context):
    search = event['queryStringParameters']['search']
    return harvest_call(search)
