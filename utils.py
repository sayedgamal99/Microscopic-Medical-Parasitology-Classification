import os
import logging
import tensorflow as tf
from tensorflow.keras.models import load_model
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CLASS_NAMES = {
    0: "Ascariasis", 1: "Babesia", 2: "Capillaria p", 3: "Enterobius v",
    4: "Epidermophyton floccosum", 5: "Fasciolopsis buski", 6: "Hookworm egg",
    7: "Hymenolepis diminuta", 8: "Hymenolepis nana", 9: "Leishmania",
    10: "Opisthorchis viverrine", 11: "Paragonimus spp", 12: "T. rubrum",
    13: "Taenia spp", 14: "Trichuris trichiura"
}
PARASITE_INFO = {
    "Ascariasis": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Large roundworm infection of the intestines"
    },
    "Babesia": {
        "type": "Protozoan",
        "infection_site": "Blood",
        "description": "Tick-borne parasitic infection affecting red blood cells"
    },
    "Capillaria p": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Intestinal parasitic worm"
    },
    "Enterobius v": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Pinworm infection commonly affecting children"
    },
    "Epidermophyton floccosum": {
        "type": "Fungus",
        "infection_site": "Skin",
        "description": "Dermatophyte causing skin infections"
    },
    "Fasciolopsis buski": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Large intestinal fluke"
    },
    "Hookworm egg": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Parasitic worm affecting the small intestine"
    },
    "Hymenolepis diminuta": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Rat tapeworm that can infect humans"
    },
    "Hymenolepis nana": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Dwarf tapeworm infection"
    },
    "Leishmania": {
        "type": "Protozoan",
        "infection_site": "Systemic",
        "description": "Parasitic disease transmitted by sandflies"
    },
    "Opisthorchis viverrine": {
        "type": "Helminth",
        "infection_site": "Hepatic",
        "description": "Liver fluke infection"
    },
    "Paragonimus spp": {
        "type": "Helminth",
        "infection_site": "Pulmonary",
        "description": "Lung fluke infection"
    },
    "T. rubrum": {
        "type": "Fungus",
        "infection_site": "Skin",
        "description": "Common cause of athlete's foot and ringworm"
    },
    "Taenia spp": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Tapeworm infection"
    },
    "Trichuris trichiura": {
        "type": "Helminth",
        "infection_site": "Intestinal",
        "description": "Whipworm infection of the large intestine"
    }
}

SAMPLE_IMAGES_DIR = "data_samples"
NUM_DISPLAYED = 9

@st.cache_resource
def load_model_safely():
    try:
        model = load_model('models/model.keras')
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        st.error("Failed to load the model. Please check if the model file exists.")
        return None

@st.cache_data(show_spinner=False)
def load_sample_images(n=9):
    sample_images = []
    random_samples = np.random.choice(os.listdir(SAMPLE_IMAGES_DIR), n, replace=False)
    for img_name in random_samples:  # Load only the first 9 images
        if img_name.endswith(("jpg", "jpeg", "png")):
            image = Image.open(os.path.join(SAMPLE_IMAGES_DIR, img_name))
            sample_images.append((img_name, image))
    st.write(f"Loaded {len(sample_images)} sample images.")
    return sample_images


def preprocess_image(_image, target_size=(224, 224)):
    """
    Efficiently preprocess the image.
    """
    try:
        if _image.mode != "RGB":
            _image = _image.convert("RGB")
        image = _image.resize(target_size, Image.LANCZOS)
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array, None
    except Exception as e:
        return None, str(e)

def predict_image(model, img_array):
    """
    Optimized function for prediction.
    """
    try:
        prediction = model.predict(img_array, verbose=0)
        predicted_class = np.argmax(prediction, axis=1)[0]
        confidence_scores = prediction[0]
        return predicted_class, confidence_scores, None
    except Exception as e:
        return None, None, str(e)

def get_top_predictions(confidence_scores, top_k=3):
    """
    Get the top predictions.
    """
    top_indices = np.argsort(confidence_scores)[-top_k:][::-1]
    return [(CLASS_NAMES[i], confidence_scores[i]) for i in top_indices]

def display_parasite_info(parasite_name):
    """
    Display parasite information.
    """
    info = PARASITE_INFO[parasite_name]
    st.markdown(f"""
    ### {parasite_name}
    - **Type**: {info['type']}
    - **Infection Site**: {info['infection_site']}
    - **Description**: {info['description']}
    """)
