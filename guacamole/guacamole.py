import requests
import json

GUACAMOLE_HOST = 'http://guacamole:8080'
USERNAME = 'guacadmin'
PASSWORD = 'guacadmin'

# get token /
def get_token():
    # CA_CRT = '/path/to/ca_bundle.crt'
    # CA_CRT = False # Disable SSL certificate verification
    session = requests.Session()
    # session.verify = CA_CRT
    response = session.post(
        f"{GUACAMOLE_HOST}/guacamole/api/tokens",
        data={'username': USERNAME, 'password': PASSWORD},
        # verify=CA_CRT
    )
    data = response.json()
    return  data['authToken']

# get session info TODO: avoid request again here
def get_session_info():
    session = requests.Session()
    response = session.post(
        f"{GUACAMOLE_HOST}/guacamole/api/tokens",
        data={'username': USERNAME, 'password': PASSWORD},
    )
    data = response.json()    
    session.headers.update({
      'Guacamole-Token': data['authToken'],
    })
    url = f"{GUACAMOLE_HOST}/guacamole/api/session/data/mysql/connections"
    response = session.get(url)

    return response.text

# create user /
def create_user(username, password):
    token = get_token()
    url = f"{GUACAMOLE_HOST}/guacamole/api/session/data/mysql/users?token={token}"
    config = {
        "username": username,
        "password": password,
        "attributes": {
            "disabled": "",
            "expired": "",
            "access-window-start": "",
            "access-window-end": "",
            "valid-from": "",
            "valid-until": "",
            "timezone": ""
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(config), headers=headers)
    return response

# delete user
def delete_user(username):
    token = get_token()
    url = f"{GUACAMOLE_HOST}/guacamole/api/session/data/mysql/users/{username}?token={token}"
    response = requests.delete(url)
    return response

# create connection
def create_connection(name, protocol, port, hostname, username, password, parentIdentifier):
    token = get_token()
    url = f"{GUACAMOLE_HOST}/guacamole/api/session/data/mysql/connections?token={token}"
    config = {
      "parentIdentifier": parentIdentifier,
      "name": name,
      "protocol": protocol,
      "parameters": {
        "port": port,
        "hostname": hostname,
        "username": username,
        "password": password
      },
      "attributes": {}
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(config), headers=headers)

    # get connection id
    data = response.json()
    return data
    return data["identifier"]

# delete connection
def delete_connection(connection_id):
    token = get_token()
    url = f"{GUACAMOLE_HOST}/guacamole/api/session/data/mysql/connections/{connection_id}?token={token}"
    response = requests.delete(url)
    return response

# assign connection
def assign_connection(username, connection_id):
    token = get_token()
    url = f"{GUACAMOLE_HOST}/guacamole/api/session/data/mysql/users/{username}/permissions?token={token}"
    config = [
          {
            "op": "add",
            "path": f"/connectionPermissions/{connection_id}",
            "value": "READ"
          }
        ]
    headers = {'Content-Type': 'application/json'}
    response = requests.patch(url, data=json.dumps(config), headers=headers)
    return response
