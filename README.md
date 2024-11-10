<p align="center">
    <img src="images/app_screanshot_v1.png" alt="Cover - App screanshot" width="600"/>
</p>

[![Installation and Usage Badge](https://img.shields.io/badge/Installation%20--%20Usage-README-red)](README.md) 
[![Project Workflow](https://img.shields.io/badge/Project_Workflow-README-blue)](README-Workflow.md)

# Microscopic Medical Parasitology Classification

An AI-powered application designed to assist medical professionals in diagnosing parasitic infections through microscopic images. This project leverages a deep learning model trained to classify 15 types of parasites, offering a valuable tool in medical parasitology, early diagnosis, and public health.



## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup and Usage](#setup-and-usage)
  - [Using Docker](#using-docker)
  - [Local Installation](#local-installation)
- [Dataset and Model Details](#dataset-and-model-details)
- [Training Process](#training-process)
- [Conclusion](#conclusion)



## Overview

Microscopic analysis plays a crucial role in detecting parasitic infections, but it’s resource-intensive and requires specialized expertise. This project aims to support healthcare professionals by classifying microscopic images of parasites using a trained deep learning model. The model, developed through fine-tuning ResNet101V2, accurately identifies 15 types of parasites, making diagnostics more accessible and efficient.

---

## Project Structure

```bash
.
├── app.py                       # Main application file
├── data_samples/                # Sample images for testing
├── Dockerfile                   # Docker setup for app deployment
├── download_model.py            # Script to download model file
├── images/                      # Images for README and application
├── models/                      # Model directory
│   └── model.keras              # trained keras model
├── README.md                    # Project README
├── requirements.txt             # Python dependencies for the app
└── utils.py                     # Helper functions for the application
```

## Usage Instructions

This application can be run using **Docker** or by setting up a **local environment**. Follow the steps below for each method.

### Using Docker

<br>

<p align="left">
    <img src="images/docker.png" alt="docker logo image" width="150"/>
</p>

Running the application with Docker is straightforward and provides an isolated environment. Make sure Docker is installed and running on your machine.

1. **Pull the Docker Image**:

   Pull the pre-built Docker image from Docker Hub:

   ```bash
   docker pull sayedgamal/micro-parasite-classifier:v1.0
   ```

2. **Run the Docker Container**:

   Launch the container using the command below. This command will expose the app on port 8501 of your localhost:

   ```bash
   docker run -d -p 8501:8501 sayedgamal/micro-parasite-classifier:v1.0
   ```

3. **Access the Application**:

   Open a web browser and navigate to `http://localhost:8501` to access the Streamlit application.

---

<br>
<br>

## Using Local Installation

Follow these steps to set up and run the application locally. Ensure you have `pip` installed.

<p align="left">
    <img src="images/vnev.png" alt="Virtual Environment image" width="150"/>
</p>

### 1. Clone the Repository

```bash
git clone https://github.com/sayedgamal99/Microscopic-Medical-Parasitology-Classification.git
cd Microscopic-Medical-Parasitology-Classification
```

### 2. Set Up Virtual Environment

It's recommended to use a virtual environment to avoid package conflicts:

```bash
# Create virtual environment
python -m venv micro_env

# Activate virtual environment
# For Windows:
micro_env\Scripts\activate
# For Unix or MacOS:
source micro_env/bin/activate
```

### 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Download the Model

The model files are hosted on Kaggle. Follow these steps to download them:

1. **Get Kaggle API Credentials**:

   - Go to [You Kaggle Acount](https://www.kaggle.com/account)
   - Scroll down to the "API" section
   - Click "Create New API Token" to download `kaggle.json`
   - Place the downloaded `kaggle.json` file in the project root directory

2. **Run the Download Script**:
   ```bash
   python download_model.py
   ```
   This script will:
   - Verify your Kaggle credentials
   - Install the Kaggle package if needed
   - Download and extract the model files to the `models` directory

### 5. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

### 6. Access the Application

Open your web browser and navigate to:

- URL: `http://localhost:8501`
- The application should load automatically and be ready for use

<br>
<br>

With either method, you’ll have full access to the parasite classification interface. Use the interface to upload images, classify, and explore results using the deep learning model.

---
