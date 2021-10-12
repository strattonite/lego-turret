#!/usr/bin/env python3
from turret import *
from time import sleep

t = Turret()

sleep(2.5)
t.pan(180)
sleep(2.5)
t.aim_at(25, 10)
sleep(2.5)
#t.fire()
t.release_brakes()

# wait for touch input to start, and set stop time ...