#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
GPIO.setmode (GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(4,GPIO.OUT)

count = 0
t1=1

while 1:
	print( "LED on")
	
	GPIO.output(25, GPIO.HIGH)
	GPIO.output(24, GPIO.HIGH)
	GPIO.output(23, GPIO.HIGH)
	GPIO.output(4, GPIO.HIGH)
	time.sleep(.05)
	print ("LED off")
	GPIO.output(25, GPIO.LOW)
	GPIO.output(24, GPIO.LOW)
	GPIO.output(23, GPIO.LOW)
	GPIO.output(4, GPIO.LOW)
	time.sleep(.45)
	count = count +1

GPIO.cleanup()
