from __future__ import print_function
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
import requests
import warnings
warnings.filterwarnings('ignore')
from json import *
from flask_cors import CORS, cross_origin
import joblib
import CNN
import torch
from torchvision.io import read_image
import torchvision.transforms as TF
from PIL import Image
import os


@app.route("/leaf", methods=["POST"])
@cross_origin()
def members1():
    print("hello from leaf")
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({'error': 'No file part'})
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        
        allowed_extensions = {'jpg'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Only JPG files are allowed'})
        
        os.makedirs("images", exist_ok=True)
        file.save('images/leaf.jpg')
        print("File saved")
        
        new_img = Image.open('images/leaf.jpg').convert('RGB').resize((224, 224))
        img = TF.ToTensor()(new_img)
        img = img.unsqueeze(0)
        img = img / 255.0
        
        # Load the model and make a prediction
        model = CNN.CNN(39)
        model.load_state_dict(torch.load('plant_disease_model_1_latest.pt', map_location=torch.device('cpu')))
        prediction = model(img).detach().numpy()
        predicted_class_idx = np.argmax(prediction[0])
        
        class_labels = [
            'Apple___Apple_scab',
            'Apple___Black_rot',
            'Apple___Cedar_apple_rust',
            'Apple___healthy',
            'Background_without_leaves',
            'Blueberry___healthy',
            'Cherry___Powdery_mildew',
            'Cherry___healthy',
            'Corn___Cercospora_leaf_spot Gray_leaf_spot',
            'Corn___Common_rust',
            'Corn___Northern_Leaf_Blight',
            'Corn___healthy',
            'Grape___Black_rot',
            'Grape___Esca_(Black_Measles)',
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
            'Grape___healthy',
            'Orange___Haunglongbing_(Citrus_greening)',
            'Peach___Bacterial_spot',
            'Peach___healthy',
            'Pepper,_bell___Bacterial_spot',
            'Pepper,_bell___healthy',
            'Potato___Early_blight',
            'Potato___Late_blight',
            'Potato___healthy',
            'Raspberry___healthy',
            'Soybean___healthy',
            'Squash___Powdery_mildew',
            'Strawberry___Leaf_scorch',
            'Strawberry___healthy',
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy'
        ]

        predicted_label = class_labels[predicted_class_idx]

        
        return jsonify({"leaf status": predicted_label})
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to process the request."})


if __name__ == "__main__":
    app.run(debug=True)
