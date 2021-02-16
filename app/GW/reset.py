#!/usr/bin/env python
import RPi.GPIO as GPIO  
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)  
time.sleep(.100)
GPIO.output(22, GPIO.LOW)  
GPIO.cleanup()   
