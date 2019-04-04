import RPi.GPIO as gpio
import time

IN1 = 7
IN2 = 11
IN3 = 13
IN4 = 15
SERVO = 12

gpio.setmode(gpio.BOARD)

gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
gpio.setup(IN3, gpio.OUT)
gpio.setup(IN4, gpio.OUT)

gpio.output(IN1, False)
gpio.output(IN2,True)
gpio.output(IN3, True)
gpio.output(IN4, True)

time.sleep(2)

gpio.cleanup()
