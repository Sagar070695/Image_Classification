import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Load Keras model
model = load_model('your_model.h5')

# Load labels
with open('labels.txt', 'r') as f:
    labels = [line.strip() for line in f]

# Title
st.title('Image Classification Project')

# Current time input
current_time = st.time_input('Current Time')

# Project description
description = st.text_area('Description of the Project')

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

# Process and classify image if an image is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Preprocess the image to fit the model input shape
    image = image.resize((224, 224))  # Resize as per model's expected input size
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    
    # Predict
    predictions = model.predict(image)
    predicted_label = labels[np.argmax(predictions)]
    confidence = np.max(predictions) * 100
    
    # Display prediction
    st.write(f"Prediction: {predicted_label}")
    st.write(f"Confidence: {confidence:.2f}%")
