import RPi.GPIO as GPIO
from time import sleep # Import the sleep function from the time module

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True: # Run forever
 print(GPIO.input(17)) # Turn on
 sleep(1) # Sleep for 1 second
