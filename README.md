#SecureSure Conversational AI agent
An AI powered car insurance assitant

## TABLE OF CONTENTS
-[FEATURES](#Features)
-[SETUP](#Setup)
-[FOLDER_STRUCTURE]

## FEATURES
This project uses
-Fine tuning of resnet18 model for image classification
-OCR-based document validation
-RAG based FAQ queries
-Sentence transformers to understand user queries

Flows Supported
-Accident claim
-Windowshield damage claim
-Lead generation
-FAQ's

## Setup
STEP 1: Clone the git repo locally

STEP 2: Navigate to the particular directory where this repo is cloned in your local system
```bash
cd securesure_bot
pip install -r requirements.txt #installs the required python libraries.
```
STEP 3: Install the required dependency "tesseract-ocr"
```bash
#if you are using a debian based linux system, 
sudo apt install tesseract-ocr
#else find equivalent command for your distribution
```
STEP 4: (optional) If you want to fine tune the model that classifies images of a windshield
You can:
-Add more images inside training_model/training_dataset for better fine-tuning
-Modify the number_of_iterations the training of weights happens for in the file training_model/train_model.py
-Once done run the script
```bash
python3 training_model/train_model.py
```
STEP 5: Run this AI agent locally
```bash
uvicorn main:app --reload
```