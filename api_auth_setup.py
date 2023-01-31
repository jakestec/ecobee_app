import json
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

def getAppCode(api_key):
    auth_request = {
    'response_type': 'ecobeePin',
    'client_id': api_key,
    'scope': 'SCOPE'
    }
    try:
        response = requests.get("https://api.ecobee.com/authorize", params = auth_request)
    except requests.exceptions.RequestException as e:
        logging.error(e)
    return json.loads(response.text)

def getAuthToken(auth_token, api_key):
    token_data = {
    'grant_type': 'ecobeePin',
    'code': auth_token,
    'client_id': api_key,
    }
    try:
        response = requests.post("https://api.ecobee.com/token", data = token_data)
    except requests.exceptions.RequestException as e:
        logging.error(e)
    return json.loads(response.text)


with open('api_data.json') as api_data:
    api_data_dict = json.load(api_data)
api_key = api_data_dict.get('api_key')

auth_response = getAppCode(api_key)

print(f"Your application PIN is {auth_response['ecobeePin']}. Please authorize your app.")
user_input = input("Are you ready to contiue with authentication token process? Y or N\n")

if user_input.upper() == "Y":
    print("Calling POST method for token creation and saving locally.")
    token_response = getAuthToken(auth_response['code'], api_key)
    print(token_response)
    api_data_dict['access_token'] = token_response['access_token']
    api_data_dict['refresh_token'] = token_response['refresh_token']
    with open('api_data.json', 'w') as api_data:
        json.dump(api_data_dict, api_data)
else:
    exit()