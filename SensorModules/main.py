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


# Global flags for dispenser
WATER = 0
FLOUR = 0
DISPENSE = 0
# dispense flag should call an irq, which activates water and flour dispensing


# Initiazize sensor objects
temp_sensor = dht.DHT11(Pin(dht_config['DHT_PIN']))
distance_sensor = Ultrasonic(ultrasonics_config)
step_motor = Stepper(stepper_config)
#servo_motor = Servo(servo_config)


# Initialize hardware timer, ESP32 has four hardware timers
# Read data every milli-secs
trigger_period = 1000
#timer1 = Timer(0)
#timer1.init(period=trigger_period, mode=Timer.PERIODIC, callback = lambda t:measure())


def call_dht():
    temp_sensor.measure()
    global temp, hum
    temp = temp_sensor.temperature()
    hum = temp_sensor.humidity()
    print('Temperature - ', temp, 'Humidity - ', hum)
    
    
def call_ultrasonics():
    global distance
    distance = distance_sensor.distance_cm()
    print('Distance: ', distance)
    
    
def measure():
    call_dht()
    call_ultrasonics()
  
  
  
# def btn_irq(pin):
#     print("btn pressed")
# # trigger servo motor with a push button
# btn = Pin(34, Pin.IN)
# #btn_state = btn_pin.value()
# # button interrupt
# btn = btn.irq(trigger=Pin.IRQ_FALLING, handler = btn_irq)


delay = 0.01
min = 15
max = 165

p15 = Pin(27)
pwm15 = PWM(p15)
pwm15.freq(50)

while True:
    for d in range(18,115,1):
        print(d)
        # set the duty cycle to d .i.e. 18 through 115 with step of 1
        pwm15.duty(d)
        tSleep = (d/1023)*20
        time.sleep(tSleep)
        # print the pwm details like pin, freq, duty cycle
        print (pwm15)
    time.sleep(2)
      
      