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
rows = [20, 21, 22, 23, 24]
columns = [4, 5, 6, 12, 13]

# Setup defaults
GPIO.setup(pullupIndex, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for row in rows:
	GPIO.setup(row, GPIO.OUT, initial=GPIO.HIGH)
for column in columns:
	GPIO.setup(column, GPIO.OUT, initial=GPIO.LOW)

def triggerMecanism(row, column, callback):
	row0Indexed = row - 1
	column0Indexed = column - 1

	# Handle needed row
	GPIO.output(rows[row0Indexed], GPIO.LOW)

	# Handle needed column
	GPIO.output(columns[column0Indexed], GPIO.LOW)

	sleep(1)
	listenRotation(callback)


def resetMecanism():
	# Handle rows 
	for row in rows:
		 GPIO.output(row, GPIO.HIGH)

	# Handle columns
	for column in columns:
		 GPIO.output(column, GPIO.LOW)


def listenRotation(callback):
	revolutionIndicator = 0
	lastGPIOInput = GPIO.input(pullupIndex)
	while True:
		if (GPIO.input(pullupIndex) != lastGPIOInput):
			if (GPIO.input(pullupIndex) == 1):
				revolutionIndicator = revolutionIndicator + 1
			lastGPIOInput = GPIO.input(pullupIndex)
		if(revolutionIndicator == 2):
			resetMecanism()
			callback()
			revolutionIndicator = 0
			break


# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        triggerMecanism(2, 1, lambda : db.collection(u'games').document(doc.id).update({u'isTransmitted': True}))

doc_ref = db.collection(u'games').where(u'isEnded', u'==', True).where(u'isTransmitted', u'==', False)


# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

app.run(debug=True, host='0.0.0.0')


