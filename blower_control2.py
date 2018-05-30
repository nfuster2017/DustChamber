import sys
import tkinter as tk
#from tkinter import *
import time
import RPi.GPIO as GPIO

# Variables
cycle = 0

# GPIO pin assignments
light = 35
fan1 = 36
fan2 = 37
fan3 = 38

#GPIO configuration

GPIO.setwarnings (False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(fan1, GPIO.OUT)
GPIO.setup(fan2, GPIO.OUT)
GPIO.setup(fan3, GPIO.OUT)



#Functions

# turns everything off
def init():
    GPIO.output (light, 0)
    GPIO.output (fan1, 0)
    GPIO.output (fan2, 0)
    GPIO.output (fan3, 0)
    time.sleep(5)


def fan_cycle():
    for i in range(100):
        #print (cycle)
        GPIO.output (fan3,1)
        time.sleep (30)
        GPIO.output (fan3,0)
        time.sleep (30)
        cycle = cycle + 1

def update_timeText():
    current = time.strftime("%H:%M:%S")
    timeText.configure(text=current)
    root.after(1000, update_timeText)
    
init()
fan_cycle()

# Tkinter configuration
window = tk.Tk()
window.title("Dust Controller")
window.minsize(100,100)  
window.maxsize(700,500)

## Current date/time labels
time = tk.Label(window,text= "Time")
time.grid(row=1, column=0)

##Buttons

start = tk.Button(window,text = "Start", command = init)
start.grid(row=10, column=0)
## settime
set_time = tk.Button(window,text = "Set timer")
set_time.grid (row=2, column=0)
#set_time.pack()


    

GPIO.cleanup()

window.mainloop()
