# 🔬 Skin Cancer Classification & Clinical Severity Assessment System
[![Status](https://img.shields.io/badge/status-active-success?style=flat-square)](#)
[![Python](https://img.shields.io/badge/python-3.x-blue?style=flat-square&logo=python)](#)
[![TensorFlow](https://img.shields.io/badge/tensorflow-latest-orange?style=flat-square&logo=tensorflow)](#)
[![Flask](https://img.shields.io/badge/flask-latest-lightgrey?style=flat-square&logo=flask)](#)
## 📖 Detailed Project Description
This project introduces an advanced clinical Decision Support System (DSS) tailored for dermatological diagnostics. Skin cancer, being one of the most prevalent forms of malignancy, requires early and highly accurate detection to improve patient survival rates. Traditional visual inspections by dermatologists can be subjective and time-consuming. To address this, we developed a comprehensive diagnostic pipeline that leverages deep transfer learning models to automatically classify dermoscopic images into one of 9 distinct skin lesion categories, aligning with the ISIC (International Skin Imaging Collaboration) standards.
Beyond basic image classification, this system pioneers a holistic, patient-centric approach by integrating a **Clinical Severity Assessment** module. By gathering key demographic and historical patient data—such as age, gender, symptom duration, BMI, and infection history—the system employs Linear Discriminant Analysis (LDA) and Long Short-Term Memory (LSTM) networks to calculate an overarching severity score (High, Medium, or Low). 
This dual-pipeline architecture ensures that medical professionals not only receive a highly accurate visual pathology classification but also a contextual urgency rating, facilitating rapid triage and prioritized patient care. The entire backend is securely managed via relational databases, wrapped in a user-friendly Flask web portal designed for seamless interaction between patients and clinicians.
## 🌟 Architecture & Workflow
```mermaid
graph TD
    A[Patient Portal] --> B[Inputs]
    B --> B1[Upload Skin Lesion Image]
    B --> B2[Input Demographic Metadata]
    
    B1 --> C1[Deep Learning Classifiers: MobileNet, ResNet50, CNN]
    B2 --> C2[Linear Discriminant Analysis Classifier / LSTM]
    
    C1 --> D1[9-Class Classification Output]
    C2 --> D2[Clinical Severity Score: High, Medium, Low]
    
    D1 & D2 --> E[Consolidated Report Generator]
    E --> F[Secure SQLite/MySQL database log]
1. 🖼️ Deep Learning Image Classifier
Supported Architectures:
MobileNet (mobilenet_fixed.keras): Highly optimized transfer learning model (
20.2
 MB
20.2 MB weights file) with Depthwise Conv2D adjustments for seamless execution under modern Keras 3. It provides rapid inference suitable for edge devices.
ResNet50 (ResNet50.h5): Pre-trained deep residual network (
128.2
 MB
128.2 MB weights file) that utilizes skip connections to solve the vanishing gradient problem, ensuring highly robust feature extraction.
Custom CNN (CNN.h5): Deep convolutional neural network (
268.8
 MB
268.8 MB weights file) trained entirely from scratch on our dataset to extract highly localized, domain-specific spatial features.
Target Classes: Classifies images into 9 distinct dermatological pathologies:
Actinic Keratosis
Basal Cell Carcinoma
Dermatofibroma
Melanoma
Nevus
Pigmented Benign Keratosis
Seborrheic Keratosis
Squamous Cell Carcinoma
Vascular Lesion
2. 🗎 Clinical Severity Assessment
Feature Extraction: Predicts case urgency (High, Medium, Low) using Linear Discriminant Analysis (LDA) and an alternate LSTM model.
Variables Evaluated:
Patient Age & Gender
Symptom Duration (Days)
Body Mass Index (BMI)
Smoking History
Recent Infection History
3. 🖥️ Web Portal & Data Management
Security & Signup: Complete physician/patient registration system with secure session handling.
Relational Backend: Logged diagnostics and patient metrics stored inside SQLite/MySQL databases for medical auditing.
🛠️ Rebuilt Model Structure (Saved Outputs)
To handle modern Keras environments, the standard mobilenet.h5 weights are dynamically loaded into a rebuilt architecture. The network composition is structured as follows:



MobileNet Base (Input: 256x256x3) -> [Non-trainable layers] 
  └── GlobalAveragePooling2D() 
  └── Dense(1024, Activation: ReLU)
  └── Dense(512, Activation: ReLU)
  └── Dense(256, Activation: ReLU)
  └── Dense(128, Activation: ReLU)
  └── Dense(64, Activation: ReLU)
  └── BatchNormalization()
  └── Dropout(rate=0.2)
  └── Dense(9, Activation: Sigmoid) [Classification Layer]
Saved Output Weights Assets:
CNN.h5 (Size: 268.8 MB): Trained from scratch for local spatial extraction.
ResNet50.h5 (Size: 128.2 MB): Deep feature extraction with residual skip connections.
mobilenet_fixed.keras (Size: 20.2 MB): Portable web-assembly/mobile-ready weights.
LSTM.h5 (Size: 1.5 MB): Multi-step longitudinal analysis of patient symptom timelines.
LinearDiscriminantAnalysis.sav (Size: 1.3 KB): Extracted weights mapping clinical variables to severity vectors.
⚙️ Installation & Usage Guide
Prerequisites
Python 3.10+
TensorFlow/Keras 2.x / 3.x
SQLite3 or MySQL
Getting Started
Clone the Project

bash


git clone https://github.com/rajavardhantalathoti/skin-cancer-dcnn.git
cd skin-cancer-dcnn
Set up the Database Initialize the SQLite database with the clinical schemas:

bash


python init_sqlite_db.py
Install dependencies

bash


pip install -r requirements.txt
Model Compatibility Checks Run the diagnostics tool to inspect and fix model structure layer imports (fixes old H5 file formats):

bash


python diagnostic_models.py
python fix_model_compatibility.py
Launch Web Dashboard Navigate to the front-end code folder and launch:

bash


cd "AN ENHANCED TECHNIQUE OF SKIN CANCER CLASSIFICATION USING DEEP CONVOLUTIONAL NEURAL NETWORK WITH TRANSFER LEARNING MODELS/CODE/FRONT END"
python app.py
Open http://localhost:5000 to start diagnostic tests.

📂 Project Structure


Skin cancer detection using DCNN/
├── dermatology.db                 # SQLite DB logs
├── init_sqlite_db.py              # Schema initialization script
├── rebuild_model.py               # Model repair & validation utility
├── diagnostic_models.py           # Integrity checking scripts
├── fix_model_compatibility.py     # Deprecated DepthwiseConv2D converter
├── requirements.txt               # Dependencies
│
└── AN ENHANCED TECHNIQUE.../      # Main Project Subdirectory
    ├── CODE/
    │   ├── FRONT END/             # Flask Front-End Application
    │   │   ├── app.py             # App routing and model loaders
    │   │   ├── templates/         # Patient upload portals & dashboards
    │   │   ├── static/            # Static assets & disease image registers
    │   │   └── models/            # MobileNet.h5, LSTM & LDA models
    │   │
    │   └── BACK END/              # Background pipelines & model storage
    │       └── models/            # CNN.h5, ResNet50.h5, mobilenet_fixed.keras
    │
    └── TRANSFER LEARNING MODELS/  # Alternate weights & architecture validation
    └── TRANSFER LEARNING MODELS/  # Alternate weights & architecture validation
