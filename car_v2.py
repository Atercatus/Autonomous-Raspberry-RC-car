import PRESETS as env
import RPi.GPIO as gpio
import time
import numpy as np
import sys, tty, termios, os
import pygame



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

        # Controller
        self.controller = {}

    def show_inst(self):
        os.system('clear')
        print("Left handle: direction")
        print("Right handle: steering")
        print("X: exit")
        print("================= Speed Control ==============")
        print("motor: ", self.speed)
        print("steer: ", self.steer)

    def set_steer(self):
        self.steer = Car.__MIDDLE + (self.controller.get_axis(env.R_HORIZONTAL) * Car.__MAX_STEER)
        self.servo_motor.ChangeDutyCycle(self.steer)

    def set_speed(self):
        self.speed = self.controller.get_axis(env.L_VERTICAL)

        if self.speed < 0:
            # Reverse mode for the motor
            gpio.output(Car.__DIR1, False)
            pwm = -int(Car.__MAX_PWM * self.speed)
        
        else :
            gpio.output(Car.__DIR1, True)
            pwm = int(Car.__MAX_PWM * self.speed)

        self.motor_power = pwm
        self.motor.ChangeDutyCycle(int(pwm))

    def turn_off(self):
        print("Program Ended")
        gpio.output(Car.__DIR1, False)
        gpio.cleanup()

    def bind(self):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def turn_on(self):
        self.bind()

        while True:
            self.show_inst() 
            self.set_speed()
            self.set_steer()

            # test
            print(self.controller.get_button(0))

            # if press x btn
            # turn_off

car = Car()
car.turn_on()
