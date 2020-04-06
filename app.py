from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np

import gpt

import ner

import time
import spacy
from spacy import displacy
import parsedatetime
import datetime
import re, string
from flask_socketio import SocketIO, emit

cal = parsedatetime.Calendar()

tokenizer, model = gpt.get_model()

nlp = ner.get_spacy_model()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/generate', methods=["GET"])
def generate():
    start_time = time.time()
    seed = request.args['text']
    next_token = gpt.generate_text(seed, tokenizer, model)
    
    return jsonify({
        "seed_text": seed,
        "next_token": next_token,
        "time_taken": time.time() - start_time
    })

@app.route('/ner', methods=["POST"])
def ner():
    text = request.json['text']
    html, data = ner.get_entities(text, nlp, cal)
    return jsonify({
        "html": html,
        "entities": data
    })

# Test web socket connection
@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('connect')
def test_connect():
    print("Connected")
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
  #app.run()
  socketio.run(app, host="0.0.0.0", port=80)
  #app.run(host="0.0.0.0", port=80)