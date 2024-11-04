import streamlit as st
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the Keras model
model = load_model("./keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Set up the Streamlit interface
st.title('Image Classification Project')
st.write("Upload an image to classify")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and preprocess the image
    image = Image.open(uploaded_file).convert("RGB")

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Resize the image to 224x224 as required by the model
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Convert the image to a numpy array and normalize it
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Create an array of the right shape to feed into the Keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Make prediction
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index] * 100

    # Display the prediction and confidence score
    st.write(f"Prediction: {class_name.strip()}")
    st.write(f"Confidence Score: {confidence_score:.2f}%")
