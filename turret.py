from cued_ia_lego import *
import time 
import numpy as np
import matplotlib.pyplot as plt

class Turret: 
    def __init__(self, config):
        print("initialising")
        self.brick = NXTBrick()
        self.pan_motor = Motor(self.brick, PORT_A)
        self.tilt_motor = Motor(self.brick, PORT_B)
        self.fire_motor = Motor(self.brick, PORT_C)

        self.pan_motor.reset_position()
        self.tilt_motor.reset_position()
        self.fire_motor.reset_position()

        self.ultrasonic = Ultrasonic(self.brick, PORT_1)
        self.touch = Touch(self.brick, PORT_2)


    def start(self):
        print("starting")

    def scan(self, az_min, az_max):
        print("scanning")

    def aim_at(self, ax, az):
        print(f'aiming: [{ax}, {az}]')
        self.pan_motor.turn_to(az, 50, True, True, True, False)
        self.tilt_motor.turn_to(ax, 50, True, False, True, True)
        self.pan_motor.wait_for()
        self.tilt_motor.wait_for()


    def fire(self):
        print("firing")
        self.fire_motor.turn(5, 100, False, False, False, False)
        self.fire_motor.wait_for()

    def pan(self, angle):
        print("rotating turret (az): " + angle)
        self.pan_motor.turn(angle, 50, True, True, True, False)
        self.pan_motor.wait_for()

    def tilt(self, angle):
        print("rotating turret (ax): " + angle)
        self.tilt_motor.turn(angle, 50, True, True, True, False)
        self.tilt_motor.wait_for()


