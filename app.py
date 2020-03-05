from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import RPi.GPIO as GPIO
from time import sleep

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

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

def sendLeds(ledRow, ledIndex, callback):
	ledRow0Indexed = ledRow - 1
	ledIndex0Indexed = ledIndex - 1

	# Handle needed row
	GPIO.output(ledRows[ledRow0Indexed], GPIO.LOW)

	# Handle needed index
	GPIO.output(ledIndexes[ledIndex0Indexed], GPIO.LOW)

	sleep(1)
	detectRotation(callback)


def resetLeds():
	# Handle rows
	for item in ledRows:
		 GPIO.output(item, GPIO.HIGH)

	# Handle indexes
	for item in ledIndexes:
		 GPIO.output(item, GPIO.LOW)


def detectRotation(callback):
	revolutionIndicator = 0
	while True:
		if(GPIO.input(pullupIndex) == 1):
			revolutionIndicator = revolutionIndicator + 1
			sleep(3)
			print(revolutionIndicator)
			if(revolutionIndicator == 2):
				resetLeds()
				callback()
				revolutionIndicator = 0
				break


# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        sendLeds(2, 1, lambda : db.collection(u'games').document(doc.id).update({u'isTransmitted': True}))

doc_ref = db.collection(u'games').where(u'isEnded', u'==', True).where(u'isTransmitted', u'==', False)


# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

app.run(debug=True, host='0.0.0.0')


