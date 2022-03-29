# Write your code here :-)
from machine import Pin
import time

water_pump = Pin(27, Pin.OUT)
button = Pin(16, Pin.IN)

while True:
    button_state = button.value()
    water_pump.value(1)
    time.sleep(0.3)

