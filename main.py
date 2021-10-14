#!/usr/bin/env python3
from turret import *
from time import sleep

t = Turret(0)

sleep(2.5)
#t.scan(-60, 60, 10)
t.pan(30)
t.tilt(10)
t.fire()
sleep(2.5)
t.release_brakes()
#t.plot_graph()

