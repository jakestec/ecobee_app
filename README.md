# ecobee_app

A simple python application that monitors the humidity setpoint on an ecobee thermostat and then modifies the setpoint based on the outdoor temperature. 

The outside temperature to indoor humidity setpoint is currently hardcoded to work best for my home.


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


# To do
-create a webapp which will let the user authenticate to their ecobee account via OAuth 2.0 
-allow the user to set desired humidity setpoints via webapp and monitor the running application 
