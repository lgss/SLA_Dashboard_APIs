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


def api_get(endpoint):
    url_address = "https://api.harvestapp.com/v2/" + endpoint
    headers = {
        "User-Agent": "LGSS SLA Dashboard (https://www.lgss-digital.co.uk/)",
        "Authorization": "Bearer " + os.environ.get("HARVEST_ACCESS_TOKEN"),
        "Harvest-Account-ID": os.environ.get("HARVEST_ACCOUNT_ID"),
        "is_active": "true"
    }
    request = urllib.request.Request(url=url_address, headers=headers)
    response = json.loads(urllib.request.urlopen(request, timeout=5).read().decode("utf-8"))
    total_pages = int(response['total_pages'])
    all_entries = []

    page = 1
    while page < (total_pages + 1):
        url = "https://api.harvestapp.com/v2/" + endpoint
        if "?" in url:
            url += "&page=" + str(page)
        else:
            url += "?page=" + str(page)

        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req, timeout=5).read().decode("utf-8")
        all_entries.append(res)
        page += 1

    return json.loads(all_entries[0])


def get_cost(project_id):
    json_response = api_get("time_entries?project_id=" + str(project_id))

    filtered_response = [x for x in json_response["time_entries"] if
                         x['billable'] is True and x['billable_rate'] is not None]
    total = 0.0
    for time in filtered_response:
        total += time['hours'] * time['billable_rate']

    return total


def get_projects(search):
    message = []
    json_response = api_get("projects")

    filtered_response = [x for x in json_response['projects'] if
                         x['notes'] is not None and search in x['notes']]

    filtered_response2 = [x for x in filtered_response if
                          'cost_budget' in x and x['cost_budget'] is not None]

    for project in filtered_response2:
        total = get_cost(project["id"])
        message.append({
            "projectName": project["name"],
            "budget": project["cost_budget"],
            "spend": total,
            "budgetRemaining": project["cost_budget"] - total
        })

    return respond(message)


def lambda_handler(event, context):
    search = event['queryStringParameters']['search']
    return get_projects(search)
