from cued_ia_lego import *
import time as t
import numpy as np
import matplotlib.pyplot as plt

class Turret: 
    def __init__(self):
        print("initialising")
        self.brick = NXTBrick()
        self.pan_motor = Motor(self.brick, PORT_A)
        #self.tilt_motor = Motor(self.brick, PORT_B)
        #self.fire_motor = Motor(self.brick, PORT_C)

        self.reading  = [[]]

        # set the turret tilt to 0 degrees and hold it
        #self.tilt_motor.turn(27.5, 25, True, True, True, True)
        #self.tilt_motor.wait_for()

        self.pan_motor.reset_position()
        #self.tilt_motor.reset_position()
        #self.fire_motor.reset_position()

        self.ultrasonic = Ultrasonic(self.brick, PORT_1)
        #self.touch = Touch(self.brick, PORT_2)

        
    def pan_angle(self):
        return self.pan_motor.get_position()

    def sense(self):
        return self.ultrasonic.get_distance()

    def start(self):
        print("starting")

    def scan_time(self, duration, direction):
        print("scanning")
        
        inc = -1
        if direction:
            inc = 1
        
        t_start = t.time()
        readings = [[]]
        
        while t.time() < t_start + duration:
            angle = self.pan_angle()
            dist = self.sense()
            readings.append([angle,dist])
            self.pan_motor.pan(inc)
        
        return readings
        
    def scan_angle(self, limit):
        print("scanning")
        readings = [[]]
        angle = self.pan_angle()
        inc = -1
        if angle < limit:
            inc = 1
        
        while (limit-angle)*inc > 0:
            angle = self.pan_angle()
            dist = self.sen()
            readings.append([angle,dist])
            self.pan_motor.pan(inc)

        return readings

    def sweep(self, angle):
        print("sweeping")
        cur_angle = self.pan_angle
        readings1 = self.scan_angle(angle)
        readings2 = self.scan_angle(cur_angle)
        final = readings1 + readings2
        self.reading = final
        return final
            
           
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

    
