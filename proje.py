from dcmotor import DCMotor
from machine import Pin, PWM
from time import sleep
from servo import Servo
import dht
from hcsr04 import HCSR04
#
#
# DC Engine
frequency = 15000

pin1 = Pin(12, Pin.OUT)
pin2 = Pin(14, Pin.OUT)
enable = PWM(Pin(13), frequency)

dc_motor = DCMotor(pin1, pin2, enable)

def ileri(x):
    dc_motor.forward(x)
def geri(y):
    dc_motor.backwards(y)
def dur():
    dc_motor.stop()

# DC Engine
#
#
# Servo Engine
motor=Servo(pin=27)

def hareket(c):
    motor.move(c)
# Servo Engine
#
#
# DHT Sensor + Ultrasonic Sensor
DHTsensor = dht.DHT22(Pin(33))

Mesafe_sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

perde_açık = False
kapı_açık = False
a = True
hareket(0)

while True:
  try:
    distance = Mesafe_sensor.distance_cm()
    DHTsensor.measure()
    temp = DHTsensor.temperature()
    hum = DHTsensor.humidity()
    print("#############################")
    print('Distance:', distance, 'cm')
    print("-----------------------------")
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
    print("#############################")
    sleep(0.25)
    if temp > 650 and perde_açık == False:
        ileri(10)
        sleep(2.5)
        dur()
        hareket(90)
        perde_açık=True
        kapı_açık=True
    elif temp < 650 and perde_açık == True and kapı_açık == True:
        ileri(10)
        sleep(2.5)
        dur()
        hareket(0)
        perde_açık == False
        kapı_açık == False
    if 30 > distance > 20 and perde_açık == False :
        ileri(10)
        sleep(2.5)
        dur()
        perde_açık = True 
    elif distance > 30 and kapı_açık == False:
        ileri(10)
        sleep(2.5)
        dur()
        hareket(90)
        kapı_açık == True
  except OSError as e:
    print('Failed to read sensor.')
# DHT Sensor + Ultrasonic Sensor