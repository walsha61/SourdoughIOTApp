import machine
from network import WLAN
import network
from umqtt.robust import MQTTClient


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
print('Connected')
# Connect to MQTT broker.

print("mqtt")
mqtt = MQTTClient( CLIENT_ID, AWS_ENDPOINT, port = 8883, keepalive = 10000,
                   ssl = True, ssl_params = SSL_PARAMS )
mqtt.connect()
# Publish a test MQTT message.

print("publishing msg")
mqtt.publish( topic = 'esp32/pub', msg = 'hello world', qos = 0 )

