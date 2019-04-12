import RPi.GPIO as gpio
import time
import numpy as np
import sys, tty, termios, os


class Car:
    __DIR1 = 15
    __PWM1 = 33
    __SERVO = 32 # PWM pin // PWM0 channel(12, 32) % 12 pin is DEAD!
    __DC_FREQUENCY = 20 # MDD10A PWM max frequency
    __SERVO_FREQUENCY = 50
    __MAX_PWM = 100
    __MAX_SPEED = 1
    __SPEED_UNIT = 0.1    

    # specify degree!!!!
    __MIDDLE = 7.8 
    __MAX_LEFT = 9.4
    __MAX_RIGHT = 6.4
    __STEER_UNIT = 0.2
    __MAX_STEER = 1.5
    # __MAX_LEFT = 9.3
    # __MAX_RIGHT = 6.7

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

    def __init__(self):
        # gpio.BOARD: using #pin / gpio.BCM: using #GPIO
        gpio.setmode(gpio.BOARD)

        # gpio.OUT: use this pin for OUTPUT / gpio.IN: use this pin for INPUT
        # DC MOTOR(MDD10A)
        gpio.setup(Car.__DIR1, gpio.OUT)
        gpio.setup(Car.__PWM1, gpio.OUT)

        # SERVO MOTOR(PWM)
        gpio.setup(Car.__SERVO, gpio.OUT)

        # for unwanted movement
        gpio.output(Car.__DIR1, False)

        # DC MOTOR
        self.motor_power = 0
        self.speed = 0
        self.motor = gpio.PWM(Car.__PWM1, Car.__DC_FREQUENCY)
        self.motor.start(0)
        self.motor.ChangeDutyCycle(0)

        # Servo MOTOR
        self.servo_motor = gpio.PWM(Car.__SERVO, Car.__SERVO_FREQUENCY)
        self.servo_motor.start(2.5) # starting duty cycle (it set the servo to 0 degree)
        self.servo_motor.ChangeDutyCycle(Car.__MIDDLE)
        self.steer = 0

    def show_inst(self):
        os.system('clear')
        print("w/s: direction")
        print("a/d: steering")
        print("q: stops the motor")
        print("x: exit")
        print("================= Speed Control ==============")
        print("motor: ", self.speed)
        print("steer: ", self.steer)

    def forward(self):
        self.speed = self.speed + Car.__SPEED_UNIT

        if self.speed > Car.__MAX_SPEED:
            self.speed = Car.__MAX_SPEED

        self.set_speed()

    def reverse(self):
        self.speed = self.speed - Car.__SPEED_UNIT

        if self.speed < -Car.__MAX_SPEED:
            self.speed = -Car.__MAX_SPEED

        self.set_speed()

    def stop_motor(self):
        self.speed = 0
        self.set_speed()

    def steer_right(self):
        self.steer = self.steer - Car.__STEER_UNIT

        if self.steer < -Car.__MAX_STEER:
            self.steer = -Car.__MAX_STEER

        self.servo_motor.ChangeDutyCycle(self.steer + Car.__MIDDLE)

    def steer_left(self):
        self.steer = self.steer + Car.__STEER_UNIT

        if self.steer > Car.__MAX_STEER:
            self.steer = Car.__MAX_STEER
            
        self.servo_motor.ChangeDutyCycle(self.steer + Car.__MIDDLE)

    def set_speed(self):
        
        if self.speed < 0:
            # Reverse mode for the motor
            gpio.output(Car.__DIR1, False)
            pwm = -int(Car.__MAX_PWM * self.speed)

            if pwm > Car.__MAX_PWM:
                pwm = Car.__MAX_PWM

        elif self.speed > 0:
            # Forward mode for the motor
            gpio.output(Car.__DIR1, True)
            pwm = int(Car.__MAX_PWM * self.speed)
            if pwm > Car.__MAX_PWM:
                pwm = Car.__MAX_PWM

        else:
            # Stop mode for the motor
            gpio.output(Car.__DIR1, False)
            pwm = 0

        print(pwm)
        self.motor_power = pwm
        self.motor.ChangeDutyCycle(int(pwm))

    def stop_program(self):
        print("Program Ended")
        gpio.output(Car.__DIR1, False)
        gpio.cleanup()

    # The catch method can determine which key has been pressed
    # by the user on the keyboard
    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch

    def run(self):

        while True:
            # Keyboard character retreival method.
            # This method will save the pressed key into the variable char
            self.show_inst() 
            
            input = self.getch()

            if(input == "w"):
                self.forward()
            elif(input == "s"):
                self.reverse()
            elif(input == "a"):
                self.steer_left()
            elif(input == "d"):
                self.steer_right()
            elif(input == "q"):
                self.stop_motor()
            elif(input == "x"):
                self.stop_program()
                break
            else:
                pass
            
            input =""


car = Car()
car.run()
