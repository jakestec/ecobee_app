from schedule import every, repeat, run_pending
from ecobee_wrapper import EccobeeWrapper
import time
import logging

logging.basicConfig(filename='humidity_monitor.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def convertTemp(temp):

    return round((temp - 320) * 5 / 90)

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

    # initialize params variables for API calls and wrapper object
    settings_params = {'format': 'json', 'body':'{"selection":{"selectionType":"registered","selectionMatch":"","includeSettings":true}}'}
    weather_params = {'format': 'json', 'body':'{"selection":{"selectionType":"registered","selectionMatch":"","includeWeather":true}}'}
    eb = EccobeeWrapper("api.ecobee.com")

    outside_temp = convertTemp(eb.get("thermostat", ep_params=weather_params.copy())['thermostatList'][0]['weather']['forecasts'][0]['temperature'])
    humidity_setpoint = eb.get("thermostat", ep_params=settings_params.copy())['thermostatList'][0]['settings']['humidity']
    required_humidity = requiredHumidityLevel(outside_temp)

    if int(humidity_setpoint) != required_humidity:
        set_params = {'format': 'json'}
        set_data = '{"selection" : {"selectionType":"registered","selectionMatch":""},"thermostat": {"settings":{"humidity":'+str(required_humidity)+'}}}'
        eb.post("thermostat", ep_params=set_params, data=set_data)
        logging.info(f'Humidity change needed, outdoor temp: {outside_temp}, current setpoint: {humidity_setpoint}, new setpoint: {required_humidity}')
    else:
        logging.info(f'No change needed, outdoor temp: {outside_temp}, keeping setpoint: {humidity_setpoint}')

if __name__ == "__main__":
    watchHumidity()
    while True:
        run_pending()
        time.sleep(1)