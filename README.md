# Ecobee Humidity Monitor

A simple python application that monitors the humidity setpoint on an ecobee thermostat and then modifies the setpoint based on the outdoor temperature. 

The outside temperature to indoor humidity setpoint is currently hardcoded to work best for my home.

```
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
```
Your 'API_KEY' and 'REFRESH_TOKEN' are expected to be read in from the enviroment. These are used by the app to re-generate the access_token due to its 60min expiry.

```
api_data['api_key'] = os.environ['API_KEY']
api_data['refresh_token'] = os.environ['REFRESH_TOKEN']
```

api_auth_setup.py can be used to register the application with your ecobee account and get your refresh token. It requires at an api_key value which is provided via 'api_data.json', it will then populate the refresh and access token into the same file.

`{"api_key": "8N...Sz"}`

# Todo
- Create a webapp which will let the user authenticate to their ecobee account via OAuth 2.0 
- Allow the user to set desired humidity setpoints via webapp and monitor the running application
