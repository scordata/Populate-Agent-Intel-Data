from scape_bugs import get_bugs
from scrape_news import get_news
import requests
import config
import json
import sys

# Config
USER = config.INSTANCE_CONFIG['username']
PWD = config.INSTANCE_CONFIG['password']
INCIDENT_API = "https://" + config.INSTANCE_CONFIG['instance'] + ".service-now.com/api/now/table/incident"
CASE_API = "https://" + config.INSTANCE_CONFIG['instance'] + ".service-now.com/api/now/table/sn_customerservice_case"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
PAYLOAD = {"caller_id": "4d147a386f0331003b3c498f5d3ee437",
           "short_description": '',
           "assignment_group": "8a4dde73c6112278017a6a4baf547aa7",
           "category": "software"}


# Insert the data into the instance
def insert_into_now(instance, payload):
    try:
        response = requests.post(instance, auth=(USER, PWD), headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    data = response.json()
    print(data)


# Build the payloads for incident & CSM
def populate_data(search_query):
    bugs = get_bugs()
    news = get_news(search_query)

    for bug in bugs:
        PAYLOAD['short_description'] = bug
        insert_into_now(CASE_API, PAYLOAD)

    for headline in news:
        # Modify payload for CSM
        if 'caller_id' in PAYLOAD:
            PAYLOAD.pop('caller_id')
            PAYLOAD.pop('category')
        PAYLOAD['short_description'] = headline
        PAYLOAD['contact'] = '4d147a386f0331003b3c498f5d3ee437'
        PAYLOAD['assignment_group'] = 'c1431057db9af700a1f3dd18f49619f1'
        insert_into_now(INCIDENT_API, PAYLOAD)


if __name__ == '__main__':
    populate_data(sys.argv[1])
