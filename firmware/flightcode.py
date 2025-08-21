from machine import Pin, PWM
import time
from nrf24l01 import NRF24L01

PIN_SOLENOID = 0
PIN_SPARK = 1
PIN_THRUST = 2
PIN_SERVO = 3


solenoid = Pin(PIN_SOLENOID, Pin.OUT)
spark = Pin(PIN_SPARK, Pin.OUT)
thrust = Pin(PIN_THRUST, Pin.OUT)
servo = PWM(Pin(PIN_SERVO))
servo.freq(50) 


TARGET_ALTITUDE_FT = 15  #intended peak height
LANDING_THRUST_ON = 6     #starting point to kick the thrust
LANDING_THRUST_OFF = 3    #point where whole of the g force accumulated 
ROCKET_MASS_KG = 2  