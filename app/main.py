#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from flask import Flask, flash, request, redirect, url_for, json
from werkzeug.utils import secure_filename
import os, fnmatch
import soundfile as sf
import tensorflow as tf
import sys
import numpy as np
from scipy import signal
import keras
from keras.models import model_from_json

from utils import individual_feature_extractor_pred, individual_create_predictions_pred


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav'}


app = Flask(__name__,static_url_path='/static')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = None
graph = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compile_model():
    global model

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("test.h5")

    print("Loaded model from disk")

    model.compile(
        optimizer= "adam",
        loss= "mse")

    global graph
    graph = tf.get_default_graph() 

@app.route('/predict',methods=['POST'])
def predict():
   
    file = request.files['file']
    if file.filename == '':
        response = app.response_class(
            response=json.dumps({"error":"No selected file"}),
            status=401,
            mimetype='application/json'
        )
        return response


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_n = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_n)

        data, sr = sf.read(file_n)
        if sr != 16000:
            response = app.response_class(
                response=json.dumps({"error":"file must be sampled >= 16khz"}),
                status=404,
                mimetype='application/json'
            )
            return response

        features, complex_, real_length  = individual_feature_extractor_pred(16384)(data)

        results = []

        global model
        global graph
        y = 0
        with graph.as_default():
            for x in features:
                print(y)
                prediction= model.predict(x[np.newaxis,...])
                results.append(prediction[0][...,0:1])
                y += 1;
        print("done")
        individual_create_predictions_pred(results,complex_,real_length,filename.split('.')[0],'./static/media/')

        local_dir = "/static/media/{}"
        voice_file_name = local_dir.format(file_n.split("/")[-1])
        no_voice_file_name = voice_file_name.replace(".wav","_b.wav")

        response = app.response_class(
            response=json.dumps({"voice":voice_file_name,"no_voice":no_voice_file_name}),
            status=201,
            mimetype='application/json'
        )
        return response

    response = app.response_class(
            response=json.dumps({"error":"No allowed file"}),
            status=404,
            mimetype='application/json'
        )
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

compile_model()
if __name__ == '__main__':
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'O$%7kQgXKVOhT@refsbY;mQmt9lMWg')
    port = os.getenv('PORT', 5000)
    print('port=', port)
    app.run(host='0.0.0.0', debug=True, port=port)
