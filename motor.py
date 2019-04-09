import RPi.GPIO as gpio
import time
import numpy as np

#test
# for L298N motor driver
IN1 = 7
IN2 = 11
ENA = 33 # PWM1 channel(33, 35)
IN3 = 13
IN4 = 15

# for servo motor
# other 2 pins => direct connect
# RED : 12V
# BLACK : GND
SERVO = 32 # PWM pin // PWM0 channel(12, 32) % 12 pin is DEAD!
FREQUENCY = 50

# specify degree!!!!
MIDDLE = 7.8 
MAX_LEFT = 9.3
MAX_RIGHT = 6.7

def init():
    # gpio.BOARD: using #pin / gpio.BCM: using #GPIO
    gpio.setmode(gpio.BOARD)

    # gpio.OUT: use this pin for OUTPUT / gpio.IN: use this pin for INPUT
    # DC MOTOR(L293N)
    # OUT 1, 2
    gpio.setup(IN1, gpio.OUT)
    gpio.setup(IN2, gpio.OUT)
    # MOTOR 1 PWM
    gpio.setup(ENA, gpio.OUT)

    # OUT 3, 4
    gpio.setup(IN3, gpio.OUT)
    gpio.setup(IN4, gpio.OUT)

    # SERVO MOTOR(PWM)
    gpio.setup(SERVO, gpio.OUT)

    # for unwanted movement
    gpio.output(IN1, False)
    gpio.output(IN2,False)

    #gpio.output(IN3, False)
    #gpio.output(IN4, False)

def test_dc_motor(seconds):
    # False: gpio.LOW / True: gpio.HIGH
    accelerator = gpio.PWM(ENA, FREQUENCY)
    accelerator.start(25)

    accelerator.ChangeDutyCycle(50)
    gpio.output(IN1, False)
    gpio.output(IN2, True)
    time.sleep(1)

    accelerator.ChangeDutyCycle(70)
    gpio.output(IN1, False)
    gpio.output(IN2, True)
    time.sleep(1)

    accelerator.ChangeDutyCycle(90)
    gpio.output(IN1, False)
    gpio.output(IN2, True)
    time.sleep(1)

    accelerator.ChangeDutyCycle(100)
    gpio.output(IN1, False)
    gpio.output(IN2, True)
    time.sleep(1)

    time.sleep(seconds)

    except KeyboardInterrupt:
        accelerator.stop()
        gpio.cleanup()`


def test_servo_motor():
    # in servo motor,
    # 1ms pulse for 0 degree (LEFT)
    # 1.5ms pulse for 90 degree (MIDDLE)
    # 2ms pulse for 180 degree (RIGHT)

    # so for 50hz, one frequency is 20ms
    # duty cycle for 0 degree = (1/20)*100 = 5%
    # duty cycle for 90 degree = (1.5/20)*100 = 7.5%
    # duty cycle for 180 degree = (2/20)*100 = 10%

    servo_motor = gpio.PWM(SERVO, FREQUENCY)
    servo_motor.start(2.5) # starting duty cycle (it set the servo to 0 degree)

    degrees = np.arange(MAX_RIGHT, MAX_LEFT, 0.1)
    
    servo_motor.ChangeDutyCycle(MIDDLE)
    time.sleep(1)
    
    try:
        while True:
            for x in degrees:
                servo_motor.ChangeDutyCycle(x)
                time.sleep(0.3)
                print(x)

    except KeyboardInterrupt:
        gpio.cleanup()

def destruct():
    gpio.cleanup()

init()
#test_dc_motor(4)
test_servo_motor()
destruct()
