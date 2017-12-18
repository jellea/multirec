#!/usr/bin/env python

import blinkt
import buttonshim
import signal

# s = stereo pair
# m = mono pair
# d = disabled pair
# a = a armed, b disabled
# b = b armed, a disabled

OPTIONS = ["s","m","a","b","d"]

CHANS = ["s","a","m","d"]

def arm_channel_toggle(channel):
    print("hello")

def record():
    print("record!!")

def draw():
    for chan, val in enumerate([val for val in CHANS for _ in (0, 1)]):
      blinkt.set_pixel(chan, 255, 255, 255) 
    blinkt.show()

draw()
