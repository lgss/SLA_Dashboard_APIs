from Wormly_Lambda import lambda_handler
from HubSpot_Prospect_Project import lambda_handler
"""
print(lambda_handler(
    {
        "queryStringParameters": {
            "hostid": "66475",
            "startday": "2019-01-01",
            "endday": "2019-03-31"
        },
        "multiValueQueryStringParameters": {
            "hostid": ["62663", "66475"]
        }
    }, None))
"""
print(lambda_handler(None, None))