import requests
import json
import urllib


def get_all_owners(hapikey, app_private_token):
    if hapikey is not None:
        url = "https://api.hubapi.com/owners/v2/owners?"
        parameter_dict = {"hapikey": hapikey}
        headers = {}
    else:
        url = "https://api.hubapi.com/owners/v2/owners"
        headers = {"content-type": "application/json", "cache-control": "no-cache",
                   'Authorization': f"Bearer {app_private_token}"}
        parameter_dict = ""

    parameters = urllib.parse.urlencode(parameter_dict)
    get_url = url + parameters
    r = requests.get(url=get_url, headers=headers)
    response_dict = json.loads(r.text)

    return response_dict
