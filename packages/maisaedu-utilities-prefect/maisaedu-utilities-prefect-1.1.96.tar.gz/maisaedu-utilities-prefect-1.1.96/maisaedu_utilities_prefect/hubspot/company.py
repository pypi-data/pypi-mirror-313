import prefect
import requests
import json
import urllib
from time import sleep


def getCompanies(hapikey, app_private_token, properties, offset, tries=5):
    url = "https://api.hubapi.com/companies/v2/companies/paged?"
    if hapikey is not None:
        parameter_dict = {"hapikey": hapikey, "limit": 250}
        headers = {"content-type": "application/json", "cache-control": "no-cache"}
    else:
        parameter_dict = {"limit": 250}
        headers = {
            "content-type": "application/json",
            "cache-control": "no-cache",
            "Authorization": f"Bearer {app_private_token}",
        }
    if offset > 0:
        parameter_dict["offset"] = offset

    parameters = urllib.parse.urlencode(parameter_dict)

    for i in properties:
        parameters = parameters + "&properties=" + i
    get_url = url + parameters
    for i in range(tries):
        try:
            r = requests.get(url=get_url, headers=headers)
            response_dict = json.loads(r.text)
            return response_dict
        except Exception as e:
            prefect.get_run_logger().error(e)


def getAllCompanies(hapikey, app_private_token, properties):
    hasmore = True
    offset = 0
    attempts = 0
    while hasmore:
        resp = getCompanies(hapikey, app_private_token, properties, offset)
        try:
            hasmore = resp["has-more"]
            offset = resp["offset"]
            yield resp["companies"]
            attempts = 0
        except KeyError as e:
            if "status" in resp and resp["status"] == "error":
                attempts += 1
                sleep(10)
                if attempts > 2:
                    raise Exception(resp["message"])
            else:
                hasmore = False
