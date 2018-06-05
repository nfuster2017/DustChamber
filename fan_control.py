import tkinter as tk
from timerfunction import *
import RPi.GPIO as GPIO

def Fan_sequence(x):

    if x == True:
        GPIO.setwarnings (False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.OUT)
        cycle = 1

        for i in range(1000):
            print (cycle)
            GPIO.output (40,1)
            time.sleep (10)
            GPIO.output (40,0)
            time.sleep (10)
            cycle = cycle + 1


        GPIO.cleanup()