import RPi.GPIO as gpio
import time
import numpy as np

#######################################################
############ for testing
import sys, tty, termios, os

### deprecated
# for L298N motor driver
IN1 = 7
IN2 = 11
ENA = 12 # PWM1 channel(33, 35)
# IN3 = 13
# IN4 = 15


########################################################
########################################################
### FOR SERVO MOTOR
# other 2 pins => direct connect
# RED : 12V
# BLACK : GND
SERVO = 32 # PWM pin // PWM0 channel(12, 32) % 12 pin is DEAD!
FREQUENCY = 20 # MDD10A PWM max frequency
PWM_MAX = 100


# specify degree!!!!
MIDDLE = 7.8 
MAX_LEFT = 9.3
MAX_RIGHT = 6.7

# Disable warning from GPIO
gpio.setwarnings(False)

#########################################################
#########################################################
#########################################################
###################### MDD10A Spec ######################

### Button controlling
# In this way, you can control the direction of the motors, 
# and check if you connect the motors in the current way 
# but cannot control the speed of the motors. 
# When you push M1A button, 
# current flows from output M1A to M1B
# and the Red LED M1A will light as well as 
# for button M1B current flows from output M1B to M1A 
# and the Red LED M1B will light.

### Pins Input controlling
# DIR1: Direction input(Motor 1), low(0 ~ 0.5v), high(3 ~ 5.5v)
# PWM1: PWM input for speed control (Motor 1), Max 20Hz
# DIR2: Direction input(Motor 2), low(0 ~ 0.5v), high(3 ~ 5.5v)
# PWM2: PWM input for speed control (Motor 2), Max 20Hz
# GND : Ground

### Logic controller
# there are four input PWM1-DIR1-PWM2-DIR2
# with MAX Frequency 20Hz, and it works as follow,
#       Input   DIR     Output-A        Output-B
# PWM   off     X       off             off
# PWM   on      off     on              off
# PWM   on      on      off             on

#########################################################
#########################################################
#########################################################


DIR1 = 15
PWM1 = 33

################## Must be objectified later
motor = gpio.PWM(PWM1, FREQUENCY)
motor_power = 0
speed = 0

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
    # gpio.setup(IN3, gpio.OUT)
    # gpio.setup(IN4, gpio.OUT)

    # DC MOTOR(MDD10A)
    gpio.setup(DIR1, gpio.OUT)
    gpio.setup(PWM1, gpio.OUT)

    # SERVO MOTOR(PWM)
    gpio.setup(SERVO, gpio.OUT)

    # for unwanted movement
    gpio.output(IN1, False)
    gpio.output(IN2,False)

    gpio.output(DIR1, False)

    #gpio.output(IN3, False)
    #gpio.output(IN4, False)

def run():
    ################## Must be objectified later
    # motor = gpio.PWM(PWM1, FREQUENCY)
 
    motor.start(0)
    motor.ChangeDutyCycle(0)

    ################## Must be objectified later
    # motor_power = 0

    show_inst()

    while True:
        # Keyboard character retreival method.
        # This method will save the pressed key into the variable char
        input = getch()

        if(input == "w"):
            forward()
        elif(input == "s"):
            reverse()
        elif(input == "a"):
            steer_left()
        elif(input == "d"):
            steer_right()
        elif(input == "q"):
            stop_motor()
        elif(input == "x"):
            stop_program()
        else:
            pass
        
        input =""


def forward():
    speed = speed + 0.1

    if speed > 1:
        speed = 1

    set_motor(speed)
    show_inst()

def reverse():
    speed = speed - 0.1

    if speed < -1:
        speed = -1

    set_motor(speed)
    show_inst()

def stop_motor():
    speed = 0
    set_motor(0)
    show_inst()

def steer_right():
    print("right")

def steer_left():
    print("left")

def stop_program():
    set_motor(0)
    print("Program Ended")

def show_inst():
    os.system('clear')
    print("w/s: direction")
    print("a/d: steering")
    print("q: stops the motor")
    print("x: exit")
    print("================= Speed Control ==============")
    print("motor: ", speed)


# The catch method can determine which key has been pressed
# by the user on the keyboard
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


def set_motor(power):
    
    if power < 0:
        # Reverse mode for the motor
        gpio.output(DIR1, False)
        pwm = -int(PWM_MAX * power)

        if pwm > PWM_MAX:
            pwm = PWM_MAX

    elif power > 0:
        # Forward mode for the motor
        gpio.output(DIR1, True)
        pwm = int(PWM_MAX * power)
        if pwm > PWM_MAX:
            pwm = PWM_MAX

    else:
        # Stop mode for the motor
        gpio.output(DIR1, False)
        pwm = 0

    motor_power = pwm
    motor.ChangeDutyCycle(pwm)


def test_dc_motor(seconds):
    # False: gpio.LOW / True: gpio.HIGH
    accelerator = gpio.PWM(ENA, FREQUENCY)
    accelerator.start(25)

    try:
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
        gpio.cleanup()


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
    gpio.output(DIR1, False)
    gpio.cleanup()


init()
#test_dc_motor(4)
test_servo_motor()
destruct()
