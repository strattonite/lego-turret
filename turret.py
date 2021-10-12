from cued_ia_lego import *
import time 
import numpy as np
import matplotlib.pyplot as plt

class Turret: 
    def __init__(self):
        print("initialising")
        self.brick = NXTBrick()
        self.pan_motor = Motor(self.brick, PORT_A)
        self.tilt_motor = Motor(self.brick, PORT_B)
        #self.fire_motor = Motor(self.brick, PORT_C)

        # set the turret tilt to 0 degrees and hold it
        self.tilt_motor.turn(27.5, 25, True, True, True, True)
        self.tilt_motor.wait_for()

        self.pan_motor.reset_position()
        self.tilt_motor.reset_position()
        #self.fire_motor.reset_position()

        #self.ultrasonic = Ultrasonic(self.brick, PORT_1)
        #self.touch = Touch(self.brick, PORT_2)


    def start(self):
        print("starting")

    def scan(self, az_min, az_max):
        print("scanning")

    def aim_at(self, ax, az):
        self.pan_motor.turn_to(az, 10, True, True, True, False)
        self.pan_motor.wait_for()
        self.tilt_motor.turn_to(-ax, 10, True, False, True, True)
        self.tilt_motor.wait_for()


    def fire(self):
        self.fire_motor.turn(5, 100, False, False, False, False)
        self.fire_motor.wait_for()

    def pan(self, angle):
        self.pan_motor.turn(angle, 10, True, True, True, False)
        self.pan_motor.wait_for()

    def tilt(self, angle, hold):
        self.tilt_motor.turn(-angle, 25, True, True, True, hold)
        self.tilt_motor.wait_for()

    def home(self):
        self.pan_motor.turn_to(0, 10)
        self.tilt_motor.turn_to(0, 10)

    def release_brakes(self):
        self.tilt_motor.idle()


