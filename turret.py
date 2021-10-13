from cued_ia_lego import *
import time as t
import numpy as np
import matplotlib.pyplot as plt
import math

class Turret: 
    def __init__(self, sensitivity):
        print("initialising")
        # sensitivity is the smallest object/noise we will fire at
        self.sensitivity = sensitivity
        # initialize brick and motors with defaults
        self.brick = NXTBrick()
        self.pan_motor = Motor(self.brick, PORT_A, 100, True, True, True, False)
        self.tilt_motor = Motor(self.brick, PORT_B, 10, True, True, True, True)
        self.fire_motor = Motor(self.brick, PORT_C, 25, False, False, False, False)

        # set the turret tilt to 0 degrees and hold it
        self.tilt_motor.turn(27.5, 25, True, True, True, True)
        self.tilt_motor.wait_for()

        # reset all motor positions
        self.pan_motor.reset_position()
        self.tilt_motor.reset_position()
        self.fire_motor.reset_position()

        # initialize sensors
        self.ultrasonic = Ultrasonic(self.brick, PORT_1)
        self.touch = Touch(self.brick, PORT_2)

        self.previous_readings = {}
        self.current_readings = {}

        self.accel = 9.81
        self.velocity = "PLACE HOLDER"

    def scan(self, min_angle, max_angle, duration):
        t_end = t.time() + duration
        # self.cw indicates whether turret is panning clockwise
        self.cw = True

        def checkT():
            return t.time() < t_end

        def checkPos():
            pos = self.get_pan_angle()
            # reverses motor if we are at or past min/max angle, and turning in the wrong direction
            if min_angle >= pos and not self.cw:
                # wait for current motor action to finish
                self.pan_motor.wait_for()
                self.pan_motor.turn_to(max_angle)
                self.cw = True
                # detect objects between sweeps
                self.detect()
                # current readings -> previous readings so we can compare between sweeps
                self.previous_readings = self.current_readings
            if max_angle <= pos and self.cw:
                self.pan_motor.wait_for()
                self.pan_motor.turn_to(min_angle)
                self.cw = False
                self.detect()
                self.previous_readings = self.current_readings

        while checkT():
            checkPos()
            # take reading
            self.current_readings[
                self.get_pan_angle()
            ] = self.get_distance()


    def detect(self):
        # create dict of changes to readings between sweeps
        delta_readings = {}
        for angle in self.previous_readings.keys():
            delta_readings[angle] = self.previous_readings[angle] - self.current_readings[angle]
        
        detecting = False
        min_ang = 0 
        max_ang = 0
        min_dist = 0
        max_dist = 0
        closest_dist = 0
        closest_ang = 0
        object_width = 0
        for angle in delta_readings.keys():
            # is object currently being detected?
            if not detecting:
                # start measuring object
                if delta_readings[angle] > 0:
                    detecting = True
                    min_ang = angle
                    min_dist = self.current_readings[angle]
                    closest_point = min_dist

            else:
                # check for closest point
                if delta_readings[angle] > 0:
                    if self.current_readings[angle] < closest_point:
                        closest_dist = self.current_readings[angle]
                        closest_ang = angle
                
                else:
                    # stop measuring object
                    max_ang = angle - 1
                    max_dist = self.current_readings[max_ang]

                    # cosine rule to find width of object
                    object_width = math.sqrt(
                        (min_dist**2) + (max_dist**2) - (2 * min_dist * max_dist * math.cos(max_ang - min_ang))
                    )

        if object_width > self.sensitivity:
            return {
                closest_dist,
                closest_ang,
                object_width
            }
        else:
            return False                

    def aim(self,dist,ang):
        tilt_rad = ((np.arcsin((dist*self.accel)/self.velocity**2))/2)
        tilt_deg = tilt_rad*180/math.pi
        self.aim_at(tilt_deg,ang)
        
    def get_pan_angle(self):
        return self.pan_motor.get_position()

    def get_distance(self):
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
            angle = self.get_pan_angle()
            dist = self.get_distance()
            readings.append([angle,dist])
            self.pan_motor.pan(inc)
        
        return readings
        
    def scan_angle(self, limit):
        print("scanning")
        readings = [[]]
        angle = self.get_pan_angle()
        inc = -1
        if angle < limit:
            inc = 1
        
        while (limit-angle)*inc > 0:
            angle = self.get_pan_angle()
            dist = self.sen()
            readings.append([angle,dist])
            self.pan_motor.pan(inc)

        return readings

    def sweep(self, angle):
        print("sweeping")
        cur_angle = self.get_pan_angle
        self.readings1 = self.scan_angle(angle)
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
        self.fire_motor.turn(5)
        self.fire_motor.wait_for()

    def pan(self, angle):
        self.pan_motor.turn(angle)
        self.pan_motor.wait_for()

    def tilt(self, angle):
        self.tilt_motor.turn(-angle)
        self.tilt_motor.wait_for()

    def home(self):
        self.pan_motor.turn_to(0)
        self.tilt_motor.turn_to(0)

    def release_brakes(self):
        self.tilt_motor.idle()

    
