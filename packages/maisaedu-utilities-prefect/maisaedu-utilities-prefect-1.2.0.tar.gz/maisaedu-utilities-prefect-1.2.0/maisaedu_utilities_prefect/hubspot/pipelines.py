import requests
import json
import urllib


def get_all_pipelines(hapikey, app_private_token):
    tipo = "tickets"
    url = "https://api.hubapi.com/crm-pipelines/v1/pipelines"
    if hapikey is not None:
        parameter_dict = {"hapikey": hapikey, "archived": False}
        headers = {}
    else:
        parameter_dict = {"archived": False}
        headers = {"content-type": "application/json", "cache-control": "no-cache", 'Authorization': f"Bearer {app_private_token}"}

    parameters = urllib.parse.urlencode(parameter_dict)
    get_url = "%s/%s?" % (url, tipo) + parameters
    r = requests.get(url=get_url, headers=headers)
    data = list()
    res = json.loads(r.text)
    data = data + res["results"]
    tipo = "deals"
    get_url = "%s/%s?" % (url, tipo) + parameters
    r = requests.get(url=get_url, headers=headers)
    res = json.loads(r.text)
    data = data + res["results"]

    return data
