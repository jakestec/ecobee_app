import json
import requests
import urllib.parse
from schedule import every, repeat, run_pending
import time
import logging

logging.basicConfig(filename='humidity_monitor.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def getAccesToken():

    with open('api_data.json') as api_data:
        api_data = json.load(api_data)

    return refreshToken(api_data['refresh_token'], api_data['api_key'])

def refreshToken(refresh_token, api_key):

    refresh_token_data = {
    'grant_type': 'refresh_token',
    'code': refresh_token,
    'client_id': api_key,
    }

    try:
        response = requests.post("https://api.ecobee.com/token", data = refresh_token_data)
    except requests.exceptions.RequestException as e:
        logging.error(e)

    return response.json().get('access_token')

def convertTemp(temp):

    return (temp - 320) * 5 / 90

def getCurrentHumidity(access_token):

    url = "https://api.ecobee.com/1/thermostat?format=json&body="
    headers = {'Content-Type': 'text/json', 'Authorization': 'Bearer ' + access_token}
    data = '{"selection":{"selectionType":"registered","selectionMatch":"","includeRuntime":true}}'
    url_encoded_data = urllib.parse.quote_plus(data)
    url += url_encoded_data

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.error(e)

    return response.json()['thermostatList'][0]['runtime']['actualHumidity']

def getHumiditySetpoint(access_token):

    url = "https://api.ecobee.com/1/thermostat?format=json&body="
    headers = {'Content-Type': 'text/json', 'Authorization': 'Bearer ' + access_token}
    data = '{"selection":{"selectionType":"registered","selectionMatch":"","includeSettings":"true"}}'
    url_encoded_data = urllib.parse.quote_plus(data)
    url += url_encoded_data

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.error(e)

    return int(response.json()['thermostatList'][0]['settings']['humidity'])

def getOutsideTemp(access_token):

    url = "https://api.ecobee.com/1/thermostat?format=json&body="
    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Bearer ' + access_token}
    data = '{"selection":{"selectionType":"registered","selectionMatch":"","includeWeather":true}}'
    url_encoded_data = urllib.parse.quote_plus(data)
    url += url_encoded_data

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        
    outdoor_temp = response.json()['thermostatList'][0]['weather']['forecasts'][0]['temperature']
    return round(convertTemp(outdoor_temp))

def setHumidity(access_token, setpoint):

    url = "https://api.ecobee.com/1/thermostat?format=json"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    data = {"selection" : {"selectionType":"registered","selectionMatch":""},"thermostat": {"settings":{"humidity":str(setpoint)}}}
    data_json = json.dumps(data)
    url_encoded_data = urllib.parse.quote_plus(data_json)

    try:
        response = requests.post(url, headers=headers, data=url_encoded_data)
    except requests.exceptions.RequestException as e:
        logging.error(e)

    return response.text

def requiredHumidityLevel(current_outside_temp):
    
    if current_outside_temp > 4:
        return 38
    elif current_outside_temp <= 4 and current_outside_temp >= -1:
        return 36
    elif current_outside_temp <= -2 and current_outside_temp >= -6:
        return 34
    elif current_outside_temp <= -7 and current_outside_temp >= -12:
        return 32
    elif current_outside_temp <= -13 and current_outside_temp >= -17:
        return 28
    elif current_outside_temp <= -18 and current_outside_temp >= -22:
        return 26
    elif current_outside_temp <= -23 and current_outside_temp >= -29:
        return 20
    elif current_outside_temp < -29:
        return 16

@repeat(every(30).minutes)
def watchHumidity():

    access_token = getAccesToken()
    outside_temp = getOutsideTemp(access_token)
    humidity_setpoint = getHumiditySetpoint(access_token)
    required_humidity = requiredHumidityLevel(outside_temp)

    if humidity_setpoint != required_humidity:
        setHumidity(access_token, required_humidity)
        logging.info(f'Humidity change needed, outdoor temp: {outside_temp}, new setpoint: {required_humidity}')
    else:
        logging.info(f'No change needed, outdoor temp: {outside_temp}, keeping setpoint: {humidity_setpoint}')

if __name__ == "__main__":
    watchHumidity()
    while True:
        run_pending()
        time.sleep(1)