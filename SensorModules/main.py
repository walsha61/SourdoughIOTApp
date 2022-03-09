## Monitoring System

## Import Libraries ##
# import GPIO pins header
from machine import Pin, Timer
import time
# import DHT temperature module library
import dht
# import HCSR04 ultrasonics library
from ultrasonics import HCSR04 


## Define PINS ##
DHT_PIN = 25
ULTRASONICS_TRIG_PIN = 26
ULTRASONICS_ECHO_PIN = 27


# Read data every milli-secs
trigger_period = 1000


# Initialize hardware timer, ESP32 has four hardware timers
timer1 = Timer(0)
timer1.init(period=trigger_period, mode=Timer.PERIODIC, callback = lambda t:measure())


# Initiazize sensor objects
dht_sensor = dht.DHT11(Pin(DHT_PIN))
ultrasonics_sensor = HCSR04(trigger_pin=ULTRASONICS_TRIG_PIN, echo_pin=ULTRASONICS_ECHO_PIN, echo_timeout_us=10000)


def call_dht():
    dht_sensor.measure()
    global temp, hum
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()
    print('Temperature - ', temp, 'Humidity - ', hum)
    
    
def call_ultrasonics():
    global distance
    distance = ultrasonics_sensor.distance_cm()
    print('Distance: ', distance)
    
    
def measure():
    call_dht()
    call_ultrasonics()
    
     
#while True:


    
