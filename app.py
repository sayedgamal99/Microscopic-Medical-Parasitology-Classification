import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import streamlit as st
from PIL import Image
import numpy as np

# Load the pre-trained model
model = load_model('/app/model.keras')

# Streamlit app
st.title("Microscopic Image Classifier")
st.write("This app classifies microscopic images using a pre-trained ResNet model.")

# File upload
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Preprocess the image
    img = np.array(image.resize((224, 224))) / 255.0
    img = np.expand_dims(img, axis=0)

    # Make the prediction
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction, axis=1)

    # Display the prediction
    st.write(f"The image is classified as: {predicted_class[0]}")