from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
import requests
import cohere
from cohere.classify import Example
import sqlite3

# Custom API key with toxic message board dataset
co = cohere.Client('3E7E98dyvUvoVm59NG3Z9HWyTuUaKdvNOaxx7u8r')

# Add more examples to narrow down on exceptions (double negatives etc...)
examples = [
  Example("you are hot trash", "Toxic"),  
  Example("go to hell", "Toxic"),
  Example("get rekt moron", "Toxic"),  
  Example("get a brain and use it", "Toxic"), 
  Example("say what you mean, you jerk.", "Toxic"), 
  Example("Are you really this stupid", "Toxic"), 
  Example("I will honestly kill you", "Toxic"),  
  Example("yo how are you", "Benign"),  
  Example("I'm curious, how did that happen", "Benign"),  
  Example("Try that again", "Benign"),  #10
  Example("Hello everyone, excited to be here", "Benign"), 
  Example("I think I saw it first", "Benign"),  
  Example("That is an interesting point", "Benign"), 
  Example("I love this", "Benign"), 
  Example("We should try that sometime", "Benign"), 
  Example("You should go for it", "Benign"),
  Example("Bitch", "Toxic"),
  Example("Not that bad", "Benign"),
  Example("Aren't that bad", "Benign")
]

app = Flask(__name__)
app.config['SECRET'] = "test12345!"
socketio = SocketIO(app)
url = 'http://127.0.0.1:5000'


def db_connection():
    conn = sqlite3.connect('topics.db')
    
    with open('topic.sql') as f:
        conn.executescript(f.read())

    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = db_connection()
    cur = conn.cursor()
    count = cur.execute("SELECT COUNT(*) FROM topics")

    if count != 0:
        topics = conn.execute("SELECT * FROM topics").fetchall()
        conn.close()
        return render_template("index.html", topics=topics)

    return render_template("index.html")

def messageReceived(methods=['GET', 'POST']):
    print('Message was received')

def messageError(methods=['GET', 'POST']):
    print('Message error: Toxic')

def is_toxic(msg):
    response = co.classify(
        model='large',
        inputs=[msg],
        examples=examples
        )

    if response[0].prediction == 'Toxic' and response[0].confidence >= 0.8:
        return True
    else:
        return False


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    if 'data' in json:
        pass
    elif is_toxic(json['message']) is True:
        socketio.emit('my response', {'message': 'Toxic'}, callback=messageError)
    else:
        socketio.emit('my response', json, callback=messageReceived)


@app.route('/newTopic', methods=["POST"])
def newTopic():
    topic = request.form.get("topic")

    conn = db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO topics (topic, description) VALUES(?, ?)", (topic, topic))

    conn.commit()
    conn.close()

    return redirect("/")
    

if __name__ == "__main__":
    app.run()
    socketio.run(app, host="localhost")