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

# variables
WIFI_NAME = 'Pixel6'
WIFI_PASSWORD = '12345678'

# control monitor timing
trigger_period = 4000 #ms, triggers internal timer every 1s to perform measurements

# control message publishing
last_message = 0 # last time messgae was sent
message_interval = 5  #s, time between each messages


# -------------------------------------------------------------------------#
# AWS setup
# AWS endpoint parameters.
HOST = b'HOST'    # ex: b'abcdefg1234567'
REGION = b'REGION'  # ex: b'us-east-1'
pub_topic = 'esp32/pub'
sub_topic = 'esp32/pub'

# AWS Client ID 
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


# -------------------------------------------------------------------------#
# Setup WiFi connection.
def connect_wifi():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan.connect(WIFI_NAME, WIFI_PASSWORD)
    if not wlan.isconnected():
        machine.idle()
    return wlan
    

def restart_reconnect():
    print("Failed to connect")
    time.sleep(2)
    machine.reset()
    
    
# -------------------------------------------------------------------------#   
# Connect to MQTT broker.
def connect_mqtt():
    mqtt = MQTTClient( CLIENT_ID, AWS_ENDPOINT, port = 8883, keepalive = 10000,
                   ssl = True, ssl_params = SSL_PARAMS )
    mqtt.set_callback(aws_subscribe)
    mqtt.connect()
    # Publish a test MQTT message.

    mqtt.publish( topic = pub_topic, msg = 'Connected to AWS', qos = 0 )
    mqtt.subscribe(sub_topic)
    return mqtt


#--------------------------------------------------------------------------#
## Monitoring System
#--------------------------------------------------------------------------#

# Initiazize sensor objects
temp_sensor = dht.DHT11(Pin(dht_config['DHT_PIN']))
distance_sensor = Ultrasonic(ultrasonics_config['trig_pin'], ultrasonics_config['echo_pin'])
#servo_motor = Servo(servo_config)
step_motor = Stepper(stepper_config)



# Initialize variables
temp=0
hum = 0
distance = 0


def dht_callback():
    try:
        temp_sensor.measure()
    except OSError as e:
        return
    global temp, hum
    temp = temp_sensor.temperature()
    hum = temp_sensor.humidity()
    print('Temperature - ', temp,'Humidity - ', hum)
    

def ultrasonics_callback():
    global distance
    distance = distance_sensor.distance_cm()
    print('Distance: ', distance)


def monitor():
    dht_callback()
    ultrasonics_callback()
    #print(msg)
   
   
#--------------------------------------------------------------------------#
## Dispenser System
#--------------------------------------------------------------------------#
# Global flags for dispenser
WATER = 0
FLOUR = 0
DISPENSE = 0
# dispense flag should call an irq, which activates water and flour dispensing


def start_pump():
    water_pump = Pin(waterpump_config['pump_pin'], Pin.OUT)
    water_pump.value(1)
    time.sleep(0.3)



#--------------------------------------------------------------------------#
## AWS communication
#--------------------------------------------------------------------------#
def msg_generator():
    msg = {'temperature':temp, 'humidity':hum, 'rise':distance}
    msg_obj = json.dumps(msg)
    return msg_obj


def aws_publish():
    mqtt.publish( topic = pub_topic, msg = msg_handler(), qos = 0)
    
    

def aws_subscribe(topic, msg):
    #if msg == b'dispense':
    print("dispense")
   
   

def main():
    try:
        print("connecting to wifi..")
        wifi = connect_wifi()
        print("wifi connected..")
        time.sleep(2)
    except OSError as e:
        restart_reconnect()
        time.sleep(2)
        
        
    try:
        print("connecting to wifi..")
        mqtt = connect_mqtt()
        print("mqtt connected..")
        time.sleep(2)
    except OSError as e:
        restart_reconnect()
        time.sleep(2)
        
    
    # Initialize hardware timer, ESP32 has four hardware timers
    # Read data every milli-secs
    timer1 = Timer(0)
    timer1.init(period=trigger_period, mode=Timer.PERIODIC, callback = lambda t:monitor())
        
    
# sort out how often to publish a message
# sort out subscribing to a message
# sort out dispenser system
# sort our esp eye
    
main()
    
    


