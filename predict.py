import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle
import string
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
import tensorflow_hub as hub
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True
from keras.models import load_model
from textblob import TextBlob
from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import Dropout
from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import plot_model
from keras.layers import Bidirectional

#function to clean text
def clean_reviews(reviews):
    #loading puctuations
    punctuations = string.punctuation
    X = []
    for review in reviews:
      words = []
      for wrd in review.split():
        eff_wrd = (wrd.strip(punctuations)).lower()
        words.append(eff_wrd)
      new_review = ' '.join(words)
      X.append(new_review)
    return X

def define_model_buyer(vocab_size , max_len):
	inputs = Input(shape = (max_len,))
	se1 = Embedding(vocab_size , 256 , mask_zero = True)(inputs)
	se2 = Dropout(0.5)(se1)
	se3 = LSTM(256)(se2)
	se4 = Dense(512 , activation='relu')(se3)
	se5 = Dropout(0.5)(se4)
	se6 = Dense(128 , activation='relu')(se5)
	outputs = Dense(1 , activation='sigmoid')(se6)

	#initialize the model
	model = Model(inputs=inputs , outputs = outputs)
	#compiling model
	model.compile(loss = 'binary_crossentropy' , optimizer = 'adam')
	#printing summary of model
	return model

def define_model_hotel(vocab_size , max_len):

	inputs = Input(shape = (max_len,))
	se1 = Embedding(vocab_size , 256 , mask_zero = True)(inputs)
	se2 = Dropout(0.5)(se1)
	se3 = Bidirectional(LSTM(256))(se2)
	se4 = Dense(512 , activation='relu')(se3)
	se5 = Dropout(0.5)(se4)
	se6 = Dense(128 , activation='relu')(se5)
	outputs = Dense(1 , activation='sigmoid')(se6)

	#initialize the model
	model = Model(inputs=inputs , outputs = outputs)
	#compiling model
	model.compile(loss = 'binary_crossentropy' , optimizer = 'adam')
	#printing summary of model
	return model

#function to convert words into numbers so that we can feed them in neural network
def create_sequences(tokenizer , reviews_list ,  max_len , vocab_size):
  X = list()
  for i in range(len(reviews_list)):
    in_seq = tokenizer.texts_to_sequences([reviews_list[i]])[0]
    in_seq = pad_sequences([in_seq], maxlen=max_len)[0]
    X.append(in_seq)
  return np.array(X)


#function to predict fake or real and sentiment of review
def Predict_Hotel_Review(file):
	hotel_reviews = pd.read_csv(file , delimiter = ',')

	X = []
	for i in range(hotel_reviews.shape[0]):
		X.append(hotel_reviews.iloc[i]["Review_Text"])

	max_len = 1022
	vocab_size = 4000
	model = define_model_hotel(vocab_size , max_len)
	model.load_weights('hotel_model.h5')

	#model = load_model('hotel_model.h5')
	tokenizer = pickle.load(open('hotel_tokenizer.pkl' , 'rb'))

	X_Clean = clean_reviews(X)
	X_Sequence = create_sequences(tokenizer , X_Clean , max_len , vocab_size)
	
	###prediction for fake or real
	Y = model.predict(X_Sequence)
	Y_pred = []
	for i in range(len(Y)):
	  if Y[i][0] > 0.3:
	  	#real
	    Y_pred.append("Real")
	  else:
	  	#fake
	    Y_pred.append("Fake")
	for b in Y:
		print(b)

	for a in Y_pred:
		print(a)

	###prediction for sentiment
	Y_sentiment = []
	for rev in X_Clean:
		blob = TextBlob(rev)
		polar = blob.sentiment.polarity
		if polar > 0.3:
			Y_sentiment.append("Positive")
		elif polar < -0.3:
			Y_sentiment.append("Negative")
		else:
			Y_sentiment.append("Neutral")

	hotel_reviews["Authenticity"] = Y_pred
	hotel_reviews["Sentiment"] = Y_sentiment

	return hotel_reviews

def Predict_ECommerce_Review(file):
	buyer_reviews = pd.read_csv(file , delimiter = ',')

	X = []
	for i in range(buyer_reviews.shape[0]):
		X.append(buyer_reviews.iloc[i]["Review_Title"] + buyer_reviews.iloc[i]["Review_Text"])
	max_len = 1000
	vocab_size = 3000
	model = define_model_buyer(vocab_size , max_len)
	model.load_weights('product_model.h5')
	#model = load_model('product_model.h5',custom_objects={'KerasLayer':hub.KerasLayer})
	tokenizer = pickle.load(open('product_tokenizer.pkl' , 'rb'))
	

	X_Clean = clean_reviews(X)
	X_Sequence = create_sequences(tokenizer , X_Clean , max_len , vocab_size)
	
	###prediction for fake or real
	Y = model.predict(X_Sequence)
	Y_pred = []
	for i in range(len(Y)):
	  if Y[i][0] > 0.5:
	  	#real
	    Y_pred.append("Real")
	  else:
	  	#fake
	    Y_pred.append("Fake")

	###prediction for sentiment
	Y_sentiment = []
	for rev in X_Clean:
		blob = TextBlob(rev)
		polar = blob.sentiment.polarity
		if polar > 0.3:
			Y_sentiment.append("Positive")
		elif polar < -0.3:
			Y_sentiment.append("Negative")
		else:
			Y_sentiment.append("Neutral")

	buyer_reviews["Authenticity"] = Y_pred
	buyer_reviews["Sentiment"] = Y_sentiment

	return buyer_reviews



if __name__ == '__main__':
	None

