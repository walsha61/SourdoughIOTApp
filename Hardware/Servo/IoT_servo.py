# Write your code here :-)
import machine
import time
from machine import Pin

p13 = machine.Pin(13)
pwm13 = machine.PWM(p13)
pwm13.freq(50)
# duty for servo min = 26, max = 115

button = Pin(16, Pin.IN)

while True:
    button_state = button.value()
    if button_state == 1:
        pwm13.duty(50)
    else:
        pwm13.duty(100)
    time.sleep(0.1)


