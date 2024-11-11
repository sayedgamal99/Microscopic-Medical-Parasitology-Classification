import os
import logging
import tensorflow as tf
from tensorflow.keras.models import load_model
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
CLASS_NAMES = {
    0: "Ascariasis", 1: "Babesia", 2: "Capillaria p", 3: "Enterobius v",
    4: "Epidermophyton floccosum", 5: "Fasciolopsis buski", 6: "Hookworm egg",
    7: "Hymenolepis diminuta", 8: "Hymenolepis nana", 9: "Leishmania",
    10: "Opisthorchis viverrine", 11: "Paragonimus spp", 12: "T. rubrum",
    13: "Taenia spp", 14: "Trichuris trichiura"
}

PARASITE_INFO = {
    "Ascariasis": {
        "scientific_name": "Ascaris lumbricoides",
        "description": "Ascariasis is caused by the roundworm Ascaris lumbricoides, which is one of the most common human parasitic infections.",
        "health_effects": [
            "Abdominal pain",
            "Nausea and vomiting",
            "Intestinal blockages",
            "Nutritional deficiencies"
        ],
        "prevalence": ["Common in tropical and subtropical regions", "Higher prevalence in rural areas"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is through stool examination or detection of eggs in feces.",
        "prevention": [
            "Proper sanitation and hygiene",
            "Avoiding ingestion of contaminated food or water"
        ]
    },
    "Babesia": {
        "scientific_name": "Babesia spp.",
        "description": "Babesia is a protozoan parasite that infects red blood cells, leading to a disease known as babesiosis.",
        "health_effects": [
            "Fever",
            "Chills",
            "Fatigue",
            "Headache"
        ],
        "prevalence": ["Endemic in parts of North America, Europe, and Asia", "Associated with tick bites"],
        "risk_level": "High",
        "diagnosis": "Diagnosis is through blood smear or PCR detection of Babesia DNA.",
        "prevention": [
            "Avoiding tick exposure",
            "Using insect repellent",
            "Proper use of tick control for pets"
        ]
    },
    "Capillaria p": {
        "scientific_name": "Capillaria philippinensis",
        "description": "Capillariasis is caused by the parasitic roundworm Capillaria philippinensis, primarily affecting the intestines.",
        "health_effects": [
            "Abdominal pain",
            "Diarrhea",
            "Fatigue",
            "Anorexia"
        ],
        "prevalence": ["Found in Southeast Asia, especially the Philippines"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is made by stool examination or tissue biopsy.",
        "prevention": [
            "Avoiding consumption of raw or undercooked fish",
            "Ensuring proper sanitation"
        ]
    },
    "Enterobius v": {
        "scientific_name": "Enterobius vermicularis",
        "description": "Enterobiasis, caused by the pinworm Enterobius vermicularis, is one of the most common intestinal parasitic infections in children.",
        "health_effects": [
            "Itching around the anus",
            "Restlessness",
            "Insomnia",
            "Irritability"
        ],
        "prevalence": ["Worldwide, especially in children in crowded living conditions"],
        "risk_level": "Low",
        "diagnosis": "Diagnosis is through the 'tape test' or stool examination.",
        "prevention": [
            "Regular hand washing",
            "Washing bed linens and pajamas frequently",
            "Maintaining good hygiene"
        ]
    },
    "Epidermophyton floccosum": {
        "scientific_name": "Epidermophyton floccosum",
        "description": "Epidermophyton floccosum is a dermatophyte fungus causing superficial infections in the skin, hair, and nails.",
        "health_effects": [
            "Athlete's foot",
            "Ringworm",
            "Itchy, red skin lesions"
        ],
        "prevalence": ["Common in warm, humid environments"],
        "risk_level": "Low",
        "diagnosis": "Diagnosis is by microscopic examination of skin scrapings or fungal culture.",
        "prevention": [
            "Maintaining good foot hygiene",
            "Avoiding shared use of towels or footwear"
        ]
    },
    "Fasciolopsis buski": {
        "scientific_name": "Fasciolopsis buski",
        "description": "Fasciolopsiasis is caused by the large intestinal fluke Fasciolopsis buski, which primarily infects humans in parts of Asia.",
        "health_effects": [
            "Abdominal pain",
            "Diarrhea",
            "Nausea",
            "Fever"
        ],
        "prevalence": ["Endemic in Southeast Asia, particularly in rural areas of China and India"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is through stool examination or serology.",
        "prevention": [
            "Avoiding consumption of raw aquatic plants",
            "Ensuring proper sanitation"
        ]
    },
    "Hookworm egg": {
        "scientific_name": "Ancylostoma duodenale, Necator americanus",
        "description": "Hookworm infections are caused by hookworms that attach to the intestines and feed on blood, causing anemia.",
        "health_effects": [
            "Abdominal pain",
            "Anemia",
            "Fatigue",
            "Itchy rash at the site of larval entry"
        ],
        "prevalence": ["Common in tropical and subtropical regions", "Prevalence is higher in areas with poor sanitation"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is through stool examination for hookworm eggs.",
        "prevention": [
            "Wearing shoes to avoid contact with contaminated soil",
            "Proper sanitation and hygiene"
        ]
    },
    "Hymenolepis diminuta": {
        "scientific_name": "Hymenolepis diminuta",
        "description": "Hymenolepis diminuta is a tapeworm that can infect humans through the consumption of infected beetles or fleas.",
        "health_effects": [
            "Abdominal discomfort",
            "Diarrhea",
            "Nausea"
        ],
        "prevalence": ["Rare in humans, more common in rodents"],
        "risk_level": "Low",
        "diagnosis": "Diagnosis is through stool examination for eggs or adult tapeworms.",
        "prevention": [
            "Avoiding consumption of infected beetles or fleas",
            "Ensuring proper food hygiene"
        ]
    },
    "Hymenolepis nana": {
        "scientific_name": "Hymenolepis nana",
        "description": "Hymenolepis nana, or the dwarf tapeworm, can infect humans, particularly children, through the consumption of contaminated food or water.",
        "health_effects": [
            "Abdominal pain",
            "Diarrhea",
            "Itching around the anus"
        ],
        "prevalence": ["Common in areas with poor sanitation, particularly in children"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is through stool examination for eggs.",
        "prevention": [
            "Improved sanitation and hygiene",
            "Washing hands regularly"
        ]
    },
    "Leishmania": {
        "scientific_name": "Leishmania spp.",
        "description": "Leishmaniasis is caused by a protozoan parasite of the genus Leishmania, transmitted by sandflies.",
        "health_effects": [
            "Skin sores",
            "Fever",
            "Enlarged spleen and liver",
            "Weight loss"
        ],
        "prevalence": ["Endemic in parts of Asia, Africa, and Latin America"],
        "risk_level": "High",
        "diagnosis": "Diagnosis is through skin biopsy or PCR testing.",
        "prevention": [
            "Avoiding sandfly bites",
            "Use of insect repellent"
        ]
    },
    "Opisthorchis viverrine": {
        "scientific_name": "Opisthorchis viverrini",
        "description": "Opisthorchiasis is caused by the liver fluke Opisthorchis viverrini, which affects the bile ducts.",
        "health_effects": [
            "Abdominal pain",
            "Fever",
            "Jaundice",
            "Liver damage"
        ],
        "prevalence": ["Endemic in Southeast Asia, especially Thailand, Vietnam, and Laos"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is through stool examination or blood tests.",
        "prevention": [
            "Avoiding raw or undercooked freshwater fish",
            "Improving sanitation"
        ]
    },
    "Paragonimus spp": {
        "scientific_name": "Paragonimus spp.",
        "description": "Paragonimiasis is caused by the lung fluke Paragonimus, which can lead to respiratory symptoms.",
        "health_effects": [
            "Cough",
            "Chest pain",
            "Blood-tinged sputum",
            "Lung infection"
        ],
        "prevalence": ["Endemic in Asia, Africa, and Latin America"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is through sputum examination or serology.",
        "prevention": [
            "Avoiding consumption of raw or undercooked crustaceans",
            "Ensuring proper food hygiene"
        ]
    },
    "T. rubrum": {
        "scientific_name": "Trichophyton rubrum",
        "description": "Trichophyton rubrum is a dermatophyte fungus responsible for skin infections like athlete's foot and ringworm.",
        "health_effects": [
            "Itchy skin lesions",
            "Redness and scaling",
            "Skin inflammation"
        ],
        "prevalence": ["Common worldwide, particularly in warm and humid conditions"],
        "risk_level": "Low",
        "diagnosis": "Diagnosis is made through skin scraping or fungal culture.",
        "prevention": [
            "Maintaining good skin hygiene",
            "Avoiding sharing towels or footwear"
        ]
    },
    "Taenia spp": {
        "scientific_name": "Taenia spp.",
        "description": "Taeniasis is caused by tapeworms from the genus Taenia, which can infect the intestines.",
        "health_effects": [
            "Abdominal pain",
            "Nausea",
            "Diarrhea",
            "Weight loss"
        ],
        "prevalence": ["Found in regions where undercooked beef or pork is consumed"],
        "risk_level": "Low",
        "diagnosis": "Diagnosis is through stool examination for eggs or adult tapeworms.",
        "prevention": [
            "Properly cooking meat",
            "Improved sanitation"
        ]
    },
    "Trichuris trichiura": {
        "scientific_name": "Trichuris trichiura",
        "description": "Trichuriasis is caused by the whipworm Trichuris trichiura, which primarily affects the intestines.",
        "health_effects": [
            "Abdominal pain",
            "Diarrhea",
            "Blood in stool",
            "Anemia"
        ],
        "prevalence": ["Common in tropical regions with poor sanitation"],
        "risk_level": "Moderate",
        "diagnosis": "Diagnosis is through stool examination for eggs.",
        "prevention": [
            "Improved sanitation and hygiene",
            "Washing hands regularly"
        ]
    }
}





SAMPLE_IMAGES_DIR = "data_samples"
NUM_DISPLAYED = 7

@st.cache_resource
def load_model_safely():
    """Load the TensorFlow model safely with exception handling."""
    try:
        model = load_model('models/model.keras')
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        st.error("Failed to load the model. Please check if the model file exists.")
        return None

@st.cache_data(show_spinner=False)
def load_sample_images(n=NUM_DISPLAYED):
    """Load a random sample of images from the sample images directory."""
    sample_images = []
    try:
        random_samples = np.random.choice(os.listdir(SAMPLE_IMAGES_DIR), n, replace=False)
        for img_name in random_samples:
            if img_name.lower().endswith(("jpg", "jpeg", "png")):
                image = Image.open(os.path.join(SAMPLE_IMAGES_DIR, img_name))
                sample_images.append((img_name, image))
        logger.info(f"Loaded {len(sample_images)} sample images.")
    except Exception as e:
        logger.error(f"Error loading sample images: {str(e)}")
        st.error("Failed to load sample images. Please check the directory and image files.")
    return sample_images

def preprocess_image(_image, target_size=(224, 224)):
    """
    Preprocesses an image for prediction.
    
    Args:
        _image: A PIL image object to be processed.
        target_size: Desired size for the image.

    Returns:
        Tuple: (processed image array, error message)
    """
    try:
        if _image.mode != "RGB":
            _image = _image.convert("RGB")
        image = _image.resize(target_size, Image.LANCZOS)
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array, None
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None, str(e)

def predict_image(model, img_array):
    """
    Predicts the class of an image using a trained model.

    Args:
        model: The trained TensorFlow model.
        img_array: Preprocessed image array ready for prediction.

    Returns:
        Tuple: (predicted class, confidence scores, error message)
    """
    try:
        prediction = model.predict(img_array, verbose=0)
        predicted_class = np.argmax(prediction, axis=1)[0]
        confidence_scores = prediction[0]
        return predicted_class, confidence_scores, None
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return None, None, str(e)

def get_top_predictions(confidence_scores, top_k=3):
    """
    Get the top predictions based on confidence scores.

    Args:
        confidence_scores: Array of confidence scores from the model.
        top_k: Number of top predictions to retrieve.

    Returns:
        List of tuples containing class names and their confidence scores.
    """
    top_indices = np.argsort(confidence_scores)[-top_k:][::-1]
    return [(CLASS_NAMES[i], confidence_scores[i]) for i in top_indices]

def display_parasite_info(parasite_name):
    """
    Display information about a specific parasite.

    Args:
        parasite_name: The name of the parasite to display information for.
    """
    if parasite_name in PARASITE_INFO:
        info = PARASITE_INFO[parasite_name]
        st.markdown(f"""
        ### {parasite_name}
        - **Scientific Name**: {info.get('scientific_name', 'N/A')}
        - **Description**: {info.get('description', 'N/A')}
        - **Health Effects**: {', '.join(info.get('health_effects', []))}
        - **Diagnosis**: {info.get('diagnosis', 'N/A')}
        - **Prevalence**: {', '.join(info.get('prevalence', []))}
        - **Risk Level**: {info.get('risk_level', 'Unknown')}
        - **Prevention**: {', '.join(info.get('prevention', []))}
        """)
    else:
        st.error("No information available for this parasite.")
