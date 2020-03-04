import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pullupIndex = 25
ledRows = [20, 21, 22, 23, 24]
ledIndexes = [4, 5, 6, 12, 13]

# Setup defaults
GPIO.setup(pullupIndex, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for item in ledRows:
	GPIO.setup(item, GPIO.OUT, initial=GPIO.HIGH)
for item in ledIndexes:
	GPIO.setup(item, GPIO.OUT, initial=GPIO.LOW)


def sendLeds(ledRow, ledIndex):
	ledRow0Indexed = ledRow - 1
	ledIndex0Indexed = ledIndex - 1

	# Handle needed row
	GPIO.output(ledRows[ledRow0Indexed], GPIO.LOW)

	# Handle needed index
	GPIO.output(ledIndexes[ledIndex0Indexed], GPIO.HIGH)

	detectRotation()


def resetLeds():
	# Handle rows
	for item in ledRows:
		 GPIO.output(item, GPIO.HIGH)

	# Handle indexes
	for item in ledIndexes:
		 GPIO.output(item, GPIO.LOW)


def detectRotation():
	isRotating = True if GPIO.input(pullupIndex) == 0 else False
	while isRotating:
		if(GPIO.input(pullupIndex) == 1):
			resetLeds()
			isRotating = False


#sendLeds(3, 2)
resetLeds()
