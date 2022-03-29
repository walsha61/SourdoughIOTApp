## Monitoring System

## Import Libraries ##
# import GPIO pins header
from machine import Pin, Timer, PWM
import time
import network
from umqtt.robust import MQTTClient
import machine
import json
import camera

# -------------------------------------------------------------------------#
# AWS endpoint parameters.
HOST = b'HOST'    # ex: b'abcdefg1234567'
REGION = b'REGION'  # ex: b'us-east-1'


CLIENT_ID = "ESP32_eye"  # Should be unique for each device connected.
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

# Worked with the cmake....bin file for upload to board
camera.init(0, d0=34, d1=13, d2=14, d3=35, d4=39, d5=38, d6=37, d7=36,
            format=camera.JPEG, framesize=camera.FRAME_VGA, xclk_freq=camera.XCLK_10MHz,
            href=27, vsync=5, reset=-1, sioc=23, siod=18, xclk=4, pclk=25)

buf = camera.capture()
# if capture failed then buf = false
# if capture succeeded len(buf) > 0
f = open('image.jpg','w')
f.write(buf)
f.close()

img_file = open('image.jpg')
image_to_send = json.dumps({'image': img_file})
mqtt.publish( topic = 'esp32/pub', msg = image_to_send, qos = 0 )
