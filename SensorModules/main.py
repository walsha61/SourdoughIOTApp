## Monitoring System

## Import Libraries ##
# import GPIO pins header
from machine import Pin, Timer, PWM
import time
import dht
from ultrasonics import Ultrasonic
from config import *
from stepper import Stepper
from servo import Servo
import network
from umqtt.robust import MQTTClient
import machine
import json


# -------------------------------------------------------------------------#
# AWS endpoint parameters.
HOST = b'HOST'    # ex: b'abcdefg1234567'
REGION = b'REGION'  # ex: b'us-east-1'


CLIENT_ID = "ESP32_kk"  # Should be unique for each device connected.
AWS_ENDPOINT = b'a2ct0i272lnfu5-ats.iot.eu-west-1.amazonaws.com' #% (HOST, REGION)


keyfile = 'PrivateK.key'
with open(keyfile, 'r') as f:
    key = f.read()
    

certfile = "Certificate.crt"
with open(certfile, 'r') as f:
    cert = f.read()


# SSL certificates.
SSL_PARAMS = {'key': key,'cert': cert, 'server_side': False}


# Setup WiFi connection.
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.connect('Pixel6', '12345678')
while not wlan.isconnected():
    print('Connecting.......')
    machine.idle()
print('Connected to WI-fi')
# Connect to MQTT broker.


mqtt = MQTTClient( CLIENT_ID, AWS_ENDPOINT, port = 8883, keepalive = 10000,
                   ssl = True, ssl_params = SSL_PARAMS )
mqtt.connect()
print("connecting to mqtt")
# Publish a test MQTT message.

mqtt.publish( topic = 'esp32/pub', msg = 'Connected to AWS', qos = 0 )

#--------------------------------------------------------------------------# 

# Global flags for dispenser
WATER = 0
FLOUR = 0
DISPENSE = 0
# dispense flag should call an irq, which activates water and flour dispensing


# Initiazize sensor objects
temp_sensor = dht.DHT11(Pin(dht_config['DHT_PIN']))
distance_sensor = Ultrasonic(ultrasonics_config['trig_pin'], ultrasonics_config['echo_pin'])
#servo_motor = Servo(servo_config)
step_motor = Stepper(stepper_config)


# Initialize hardware timer, ESP32 has four hardware timers
# Read data every milli-secs
trigger_period = 1000
timer1 = Timer(0)
timer1.init(period=trigger_period, mode=Timer.PERIODIC, callback = lambda t:measure())


temp=0
hum = 0
def call_dht():
    temp_sensor.measure()
    global temp, hum
    temp = temp_sensor.temperature()
    hum = temp_sensor.humidity()
    print('Temperature - ', temp, 'Humidity - ', hum)
    
    
distance = 0
def call_ultrasonics():
    global distance
    distance = distance_sensor.distance_cm()
    print('Distance: ', distance)


def start_motor():
    water_pump = Pin(waterpump_config['pump_pin'], Pin.OUT)
    water_pump.value(1)
    time.sleep(0.3)
    
    
def msg_handler():
    msg = {'temperature':temp, 'humidity':hum, 'rise':distance}
    msg_obj = json.dumps(msg)
    return msg_obj
           

def measure():
    call_dht()
    call_ultrasonics()
    #print(msg)
    mqtt.publish( topic = 'esp32/pub', msg = msg_handler(), qos = 0 )
    

