from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

questions = db.collection(u'questions').stream()
for question in questions:
    print(u'{} => {}'.format(question.id, question.to_dict()))

app = Flask(__name__)

@app.route('/')

def index():

 return 'Hello world'

if __name__ == '__main__':

 app.run(debug=True, host='0.0.0.0')
