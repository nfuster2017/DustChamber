import time
import RPi.GPIO as GPIO
def Conditions_met():
    #if current is right t+1
    #if current is right on vacuum t+1
    #if x=5 all conditions met return x=True

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
