import tensorflow as tf
import pandas as pd
import numpy as np
from keras.backend.tensorflow_backend import clip
from keras import backend
import h5py
# clipping gradient to avoid exploding gradient (loss function)

def clipped_err(y_true, y_pred):
	return backend.mean(backend.square(backend.clip(y_pred, -1., 1.) - backend.clip(y_true, -1., 1.)), axis=-1)

def sigmoid_clip(units, input_shape):
	# Neural Netowrk Architecture
	model = tf.keras.Sequential()
	# input layer
	model.add(tf.keras.layers.Flatten(input_shape = (input_shape,)))
	# activation layers
	model.add(tf.keras.layers.Dense(units, activation="sigmoid"))
	model.add(tf.keras.layers.Dropout(0.2))
	model.add(tf.keras.layers.Dense(units, activation="sigmoid"))
	# output layer
	model.add(tf.keras.layers.Dense(1, activation = "sigmoid"))
	# compile model
	model.compile(optimizer="adam", loss= clipped_err, metrics=['accuracy'])
	return model

def sigmoid(units, input_shape):
	# Neural Netowrk Architecture
	model = tf.keras.Sequential()
	# input layer
	model.add(tf.keras.layers.Flatten(input_shape = (input_shape,)))
	# activation layers
	model.add(tf.keras.layers.Dense(units, activation="sigmoid"))
	model.add(tf.keras.layers.Dropout(0.2))
	model.add(tf.keras.layers.Dense(units, activation="sigmoid"))
	# output layer
	model.add(tf.keras.layers.Dense(1, activation = "sigmoid"))
	# compile model
	model.compile(optimizer="adam", loss="mean_squared error", metrics=['accuracy'])
	return model


