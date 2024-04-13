#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 21:04:41 2024

@author: papantiamoah
"""

from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

# Create a simple Sequential model
model = Sequential()
model.add(Dense(64, activation='relu', input_dim=784))
model.add(Dense(10, activation='softmax'))

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model (example)
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Save the model to an HDF5 file
model.save("models.h5")
