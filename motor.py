import RPi.GPIO as gpio
import time
import numpy as np

#test
# for L298N motor driver
IN1 = 7
IN2 = 11
IN3 = 13
IN4 = 15

# for servo motor
# other 2 pins
# RED : 12V
# BLACK : GND
SERVO = 32 # PWM pin
FREQUENCY = 50

# specify degree!!!!
MIDDLE = 7.8 
MAX_LEFT = 9.3
MAX_RIGHT = 6.7

#control = [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
#control = [7.8, 8, 8.2, 8.5, 8.7, 9, 9.2, 9.3, 6.7, 7.0, 7.2, 7.5]

def init():
    # gpio.BOARD: using #pin / gpio.BCM: using #GPIO
    gpio.setmode(gpio.BOARD)

    # gpio.OUT: use this pin for OUTPUT / gpio.IN: use this pin for INPUT
    gpio.setup(IN1, gpio.OUT)
    gpio.setup(IN2, gpio.OUT)
    gpio.setup(IN3, gpio.OUT)
    gpio.setup(IN4, gpio.OUT)
    gpio.setup(SERVO, gpio.OUT)

    gpio.output(IN1, False)
    gpio.output(IN2,False)

    #gpio.output(IN3, False)
    #gpio.output(IN4, False)


def test_dc_motor(seconds):
    # False: gpio.LOW / True: gpio.HIGH
    gpio.output(IN1, False)
    gpio.output(IN2,True)

    gpio.output(IN3, True)
    gpio.output(IN4, True)

    # after sleep, will return resources (ex: gpio.cleanup())
    time.sleep(seconds)

def test_servo_motor():
    servo_motor = gpio.PWM(SERVO,FREQUENCY) # pin_num, frequency
    servo_motor.start(2.5)

    try:
        while True:
            for duty in range(50, 81, 5):
                # duty: ratio of HIGH on period // if 5V -> 50% Duty cycle == 2.5V
                # increasing the duty cycle increases the pulse width
                # ratio of pulse width == duty cycle
                servo_motor.ChangeDutyCycle(duty)
                time.sleep(0.5)
            for duty in range(80, 50, -5):
                servo_motor.ChangeDutyCycle(duty)
                time.sleep(0.5)

    except KeyboardInterrupt:
        #gpio.cleanup()
        servo_motor.stop()
        gpio.output(SERVO, False)

def test_servo_motor_2():
    servo_motor = gpio.PWM(SERVO, FREQUENCY)
    servo_motor.start(2.5)

    try:
        while True:
            servo_motor.ChangeDutyCycle(5)
            print(5)
            time.sleep(1.5)
            servo_motor.ChangeDutyCycle(7.5)
            print(7.5)
            time.sleep(1.5)
            servo_motor.ChangeDutyCycle(10)
            print(10)
            time.sleep(1.5)
            servo_motor.ChangeDutyCycle(12.5)
            print(12.5)
            time.sleep(1.5)
            servo_motor.ChangeDutyCycle(10)
            print(10)
            time.sleep(1.5)
            servo_motor.ChangeDutyCycle(7.5)
            print(7.5)
            time.sleep(1.5)
            servo_motor.ChangeDutyCycle(5)
            print(5)
            time.sleep(1.5)
            servo_motor.ChangeDutyCycle(2.5)
            print(2.5)
            time.sleep(1.5)

    except KeyboardInterrupt:
        servo_motor.stop()

def test_servo_motor_3():
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

            #for x in range(10, 0, -1):
                #servo_motor.ChangeDutyCycle(control[x])
                #time.sleep(1)
                #print(control[x])

    except KeyboardInterrupt:
        gpio.cleanup()


def destruct():
    gpio.cleanup()

init()
#test_dc_motor(4)
test_servo_motor_3()
#test_servo_motor()
#set_angle(45)
#set_duty(8)
#set_duty(50)
#set_duty(0)
destruct()
