

# this is to test the ping sensor
# 
import time
from machine import Pin 
from machine import time_pulse_us

# 
#
def get_distance(pin=27):
    # initiate constants
    #
    SENSOR_PIN = pin
    INCH_FACTOR = 0.0393701 

    # make the signal pin as output to send the pulse
    #
    sensor = Pin(SENSOR_PIN, Pin.OUT)
    
    # clear turn off the pin to clear
    #
    sensor.value(0)
    time.sleep_us(5) 
    
    # send a pulse 
    #
    sensor.value(1)
    time.sleep_us(2)

    
    # HOLDOFF
    #
    sensor.value(0)
    time.sleep_us(750)

    
    # make the signal pin as input to receive incoming pulse
    #
    sensor = Pin(SENSOR_PIN, Pin.IN)
    
    # get time it took to receive the pulse
    #
    pulse_time = time_pulse_us(sensor, 1)
    
    # calculate distance in inches
    #
    dist_mm = pulse_time * 100 // 582
    dist_inches = dist_mm * INCH_FACTOR
    
    # wait 65ms
    #
    time.sleep_ms(65)
        
    return dist_inches

