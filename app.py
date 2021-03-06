# -*- coding: utf-8 -*-
"""The FLASK Server

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UjV2rff6rJzRAwJJuUkohnOUhLkQFuFR
"""
#loading necessary libraries
import string
import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
from flask import Flask, jsonify, request
import pickle
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

#loading the Tokenizer File
with open('./files/word_indexes_tokenizer_787.pickle','rb') as f:
  tokenizer = pickle.load(f)


#functions to pre-process data
def clean_data(text):

    # split into words
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    
    str1 = ""
    for i in words:
      str1 = str1 + i + " "
    return str1


def transform(data):
  essays = []
  for d in data:
    essays.append(d.split())
  return essays

#Function to prepare the data for the Model
def prepare_data(single_data_):
  data_ = []
  MAX_SEQUENCE_LENGTH = 500 #-- working well
  trunc_type='post'
  padding_type='post'
  text = clean_data(single_data_)
  count = len(text.split())
  data_.append(text)
  #print(data_)
  preproc_data = tokenizer.texts_to_sequences(data_)
  preproc_data = sequence.pad_sequences(preproc_data, maxlen=MAX_SEQUENCE_LENGTH,padding=padding_type, truncating=trunc_type)

  return preproc_data ,count


"""#The Flask Server"""

print('Starting Server')
model = tf.keras.models.load_model('./files/Essay_Grader_787_Format2')
    
# app
app = Flask(__name__)

# routes
@app.route("/",methods=['GET','POST'])
def predict():
    
    data = request.get_json(force=True)
    pass_value = data['password']
    data_vec,word_count = prepare_data(data['text'])
    
    print('Received Data :',data)
    if pass_value != 'AQUA121G890UP002':
        message = 'Unauthorized request'
        return message
    
    data_vec_ = data_vec
    results = model.predict(data_vec_)[0]
    print (results)
    score = results[0]*10
    score = round(score,2)
    # send back to browser
    output = {'results': float(score)}
    output['count'] = word_count
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 5000)
