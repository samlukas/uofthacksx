from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
import requests
import cohere
from cohere.classify import Example
import sqlite3
import firebase


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


@app.route('/')
def index():
    return render_template("index.html")


# @app.route('/thread/<thread_name>')
# def access_thread(thread_name):
#     threads = firebase.retrieve_threads()
#     if thread_name in threads:
#         posts = firebase.retrieve_posts(thread_name)
#         for post in posts:
#             socketio.emit('my response', posts[post])

#     return render_template("index.html")

   
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
    if response[0] == ' ' or (response[0].prediction == 'Toxic' and response[0].confidence >= 0.8):
        return True
    else:
        return False


@socketio.on('new title')
def handle_topic_event(json, methods=['GET','POST']):
    firebase.create_thread(json['topic'])
    socketio.emit('made topic', json, callback=messageReceived)


@socketio.on("get msg")
def get_msg(json, methods=['GET', 'POST']):
    posts = firebase.retrieve_posts(json['t_id'])
    if posts is None:
        pass
    else:
        for post in posts:
            socketio.emit('my response', {'user_name':posts[post]['username'], 'message':posts[post]['message']}, to=json['data'])


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    if 'data' in json:
        threads = firebase.retrieve_threads()
        for thread in threads:
            socketio.emit('made topic', {'topic':threads[thread]["thread_name"],'sid':json['data']}, to=json['data'], callback=messageReceived)

    elif 'message' in json and json['message'] != '' and is_toxic(json['message']):
        socketio.emit('my response', {'user_name':json['user_name'],'message': 'Toxic'}, callback=messageError)    
    else:
        firebase.create_post(json['user_name'], json['message'], json['thr_id'])
        socketio.emit('my response', json, callback=messageReceived)


# @app.route('/newTopic', methods=["POST"])
# def newTopic():
#     topic = request.form.get("topic")
#     socketio.emit('connectToRoom')
    

if __name__ == "__main__":
    app.run()
    socketio.run(app, host="localhost")