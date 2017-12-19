#!/usr/bin/env python

import time
import blinkt
import buttonshim
import signal
import os
import math
import sys
from os.path import getmtime
import subprocess

# s = stereo pair
# m = mono pair
# d = disabled pair
# a = a armed, b disabled
# b = b armed, a disabled

mtime = getmtime(__file__)
OPTIONS = ["m","a","b","d"] # no stereo atm
CHANS = ["m","a","m","d"]
RECORDING = False

LED_OFF = [0,0,0]
LED_RED = [255,0,0]
LED_WHITE = [135,135,135]

def draw():
    for chan, val in enumerate([val for val in CHANS for _ in (0, 1)]):
        switcher = {
                "a": (LED_OFF if chan % 2 == 1 else LED_WHITE),
                "b": (LED_OFF if chan % 2 == 0 else LED_WHITE),
                "d": LED_OFF,
                "m": LED_WHITE,
                "s": LED_RED
                }
        rgb = switcher.get(val, LED_OFF)
        blinkt.set_pixel(chan, rgb[0], rgb[1], rgb[2])
    blinkt.show()
    if RECORDING:
        buttonshim.set_pixel(255,0,0)
    else:
        buttonshim.set_pixel(0,0,0)

blinkt.set_brightness(0.04)

def recordnow():
    print(CHANS)
    jacklist = []
    for chan, val in enumerate([val for val in CHANS for _ in (0, 1)]):
        switcher = {
                "a": chan % 2 == 1,
                "b": chan % 2 == 0,
                "d": False,
                "m": True,
                "s": True
                }
        shallrecord = switcher.get(val, False)
        if shallrecord:
            jacklist.append("-p")
            jacklist.append("system:capture_{}".format(chan+1))
    if len(jacklist) > 0:
        cmd = ["jack_capture", "-c", str(len(jacklist)//2)] + jacklist

@buttonshim.on_press([1,2,3,4])
def arm (button, pressed):
    invnum = range(len(OPTIONS)-1,-1,-1)[button]
    CHANS[invnum] = OPTIONS[(OPTIONS.index(CHANS[invnum])+1)%len(OPTIONS)]

@buttonshim.on_press(0)
def record (button, pressed):
    global RECORDING
    RECORDING = not RECORDING
    if RECORDING:
         recordnow()

while True:
    if getmtime(__file__) > mtime:
      print("Restarting program! -- file changed")
      os.execv(sys.executable, ['python3'] + sys.argv)
    draw()
    time.sleep(0.05)
