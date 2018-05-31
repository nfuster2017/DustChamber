# Libraries

import RPi.GPIO as GPIO
import time
import datetime as time1
import tkinter as tk
#from tkinter import *

#  Hardware Configuration
light = 35
fan1 = 36 
fan2 = 37
fan3 = 38

# GPIO pin configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(light,GPIO.OUT)
GPIO.setup(fan1, GPIO.OUT)
GPIO.setup(fan2, GPIO.OUT)
GPIO.setup(fan3, GPIO.OUT)
### Hardware initialization
GPIO.output(light, False)
GPIO.output(fan1, False)
GPIO.output(fan2, False)
GPIO.output(fan3, False)

# Tkinter configuration
window = tk.Tk()
window.title("Dust Controller")
window.minsize(100,100)  
window.maxsize(700,500)

## Current date/time labels
time = tk.Label(window,text= "Time")
time.grid(row=1, column=0)

##Buttons
###start 
start = tk.Button(window,text = "Start")
start.grid(row=10, column=0)
### settime
set_time = tk.Button(window,text = "Set timer")
set_time.grid (row=2, column=0)
#set_time.pack()


# Classes

#class fan_cycle(object):

 #   def cycle ():
 #      fan1
        
    


# Functions



# Tkinter main program


# Tkinter main loop
window.mainloop()


