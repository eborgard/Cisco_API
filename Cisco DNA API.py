import requests
import json
from requests.auth import HTTPBasicAuth

def login():
    login_url = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token"
    result = requests.post(url=login_url, auth=HTTPBasicAuth("devnetuser", "Cisco123!"), verify=False)
    token = result.json()["Token"]
    return token

def get_devices():
    token = login()
    url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"
    headers = {'X-Auth-Token': token, 'Content Type': 'Application/JSON'}
    resp = requests.get(url=url, headers=headers)
    devices = resp.json()
    print_device_list(devices)

def polling_interval(token):
    url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device/collection-schedule/global"
    headers = {'X-Auth-Token': token, 'Content Type': 'Application/JSON'}
    resp = requests.get(url=url, headers=headers)
    polling = resp.json()
    polling_int = json.dumps(polling, indent=2)
    return polling_int

def print_device_list(devices):
    print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
          format("hostname", "mgmt IP", "serial","platformId", "SW Version", "role", "Uptime"))
    for device in devices['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        for (serialNumber, platformId) in serialPlatformList:
            print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(device['hostname'],
                         device['managementIpAddress'],
                         serialNumber,
                         platformId,
                         device['softwareVersion'],
                         device['role'], uptime))


if __name__ == "__main__":
    get_devices()
