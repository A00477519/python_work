#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 20:06:41 2024

@author: papantiamoah

Python assignment - question 3

"""



import streamlit as st
import numpy as np
from PIL import Image
from keras.models import load_model
from PIL import ImageOps

# Load the pre-trained model
model = load_model("/Users/papantiamoah/Documents/School/Masters/2ndSemester/Data&Text_Mining/python_assignment/keras_model.h5")

# Compile the model with appropriate loss function and metrics
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


# Function to preprocess the uploaded image

def preprocess_image(image):
    # Resize image to 28x28 pixels (MNIST dataset size)
    resized_image = image.resize((28, 28))
    
    # Create a transparent background
    transparent_background = Image.new('RGBA', resized_image.size, (255, 255, 255, 0))
    
    # Composite the resized image onto the transparent background
    composite_image = Image.alpha_composite(transparent_background, resized_image.convert('RGBA'))
    
    # Convert the composite image to grayscale
    grayscale_image = ImageOps.grayscale(composite_image)
    
    # Normalize pixel values to range [0, 1]
    normalized_image = np.array(grayscale_image) / 255.0
    
    # Reshape image to match model input shape (flatten)
    flattened_image = normalized_image.flatten().reshape((1, 784))
    
    return flattened_image


# Main function
def main():
    # Display app title and description
    st.title("Image Classifier")
    st.write("Upload an image of a digit (0 to 9) to classify it.")

    # File uploader widget for image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the uploaded image as a PIL Image object
        image = Image.open(uploaded_file)
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Classify the image using the loaded model
        prediction = model.predict(processed_image)
        
        # Get the predicted class (digit)
        predicted_class = np.argmax(prediction)
        
        # Display the predicted class
        st.write(f"Predicted Digit: {predicted_class}")

# Run the app
if __name__ == "__main__":
    main()
