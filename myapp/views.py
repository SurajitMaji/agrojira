from django.shortcuts import render
from .forms import FertilizerForm
from .forms import CropForm
from .forms import PesticideForm
import joblib
import pandas as pd
import numpy as np
import pickle
import os

# Load models only once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
classifier_path = os.path.join(BASE_DIR, 'ml_models/classifier.pkl')
fertilizer_path = os.path.join(BASE_DIR, 'ml_models/fertilizer.pkl')

with open(classifier_path, 'rb') as f:
    classifier = pickle.load(f)

with open(fertilizer_path, 'rb') as f:
    fertilizer_label_encoder = pickle.load(f)

# Dictionaries for encoding
soil_dict = {"Black": 0, "Clayey": 1, "Loamy": 2, "Red": 3, "Sandy": 4}
fertilizer_crop_dict = {
    "Barley": 0, "Cotton": 1, "Ground Nuts": 2, "Maize": 3, "Millets": 4,
    "Oil seeds": 5, "Paddy": 6, "Pulses": 7, "Sugarcane": 8, "Tobacco": 9, "Wheat": 10
}

def fertilizer_tool_view(request):
    result = None
    if request.method == 'POST':
        form = FertilizerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            input_dict = {
                'Temparature': [int(data['temperature'])],
                'Humidity': [int(data['humidity'])],
                'Moisture': [int(data['moisture'])],
                'Soil_Type': [soil_dict[data['soil_type']]],
                'Crop_Type': [fertilizer_crop_dict[data['crop_type']]],
                'Nitrogen': [int(data['nitrogen'])],
                'Potassium': [int(data['potassium'])],
                'Phosphorous': [int(data['phosphorus'])],
            }

            input_df = pd.DataFrame(input_dict)
            prediction = classifier.predict(input_df)[0]
            fertilizer_name = fertilizer_label_encoder.classes_[prediction]
            result = f" Recommended Fertilizer: {fertilizer_name}"
    else:
        form = FertilizerForm()

    return render(request, 'myapp/fertilizer_tool.html', {'form': form, 'result': result})
crop_model_path = os.path.join(BASE_DIR, 'ml_models/naive_bayes_model.pkl')

with open(crop_model_path, 'rb') as f:
    model = pickle.load(f)

# Crop dictionary
crop_dict = {
    1: 'rice', 2: 'maize', 3: 'jute', 4: 'cotton', 5: 'coconut',
    6: 'papaya', 7: 'orange', 8: 'apple', 9: 'muskmelon', 10: 'watermelon',
    11: 'grapes', 12: 'mango', 13: 'banana', 14: 'pomegranate',
    15: 'lentil', 16: 'blackgram', 17: 'mungbean', 18: 'mothbeans',
    19: 'pigeonpeas', 20: 'kidneybeans', 21: 'chickpea', 22: 'coffee'
}

def crop_recommendation_view(request):
    result = None
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            input_features = np.array([[
                data['nitrogen'], data['phosphorous'], data['potassium'],
                data['temperature'], data['humidity'], data['ph'], data['rainfall']
            ]])
            prediction = model.predict(input_features)[0]
            crop_name = crop_dict.get(prediction, "Unknown Crop")
            result = f"🌱 Recommended Crop: {crop_name.capitalize()}"
    else:
        form = CropForm()
    
    return render(request, 'myapp/crop_recommendation.html', {'form': form, 'result': result})
xgb_model = joblib.load(os.path.join(BASE_DIR, 'ml_models/pesticide_model.pkl'))
le_crop = joblib.load(os.path.join(BASE_DIR, 'ml_models/le_crop.pkl'))
le_pest = joblib.load(os.path.join(BASE_DIR, 'ml_models/le_pest.pkl'))
le_pesticide = joblib.load(os.path.join(BASE_DIR, 'ml_models/le_pesticide.pkl'))
le_app_method = joblib.load(os.path.join(BASE_DIR, 'ml_models/le_app_method.pkl'))
le_dosage = joblib.load(os.path.join(BASE_DIR, 'ml_models/le_dosage.pkl'))

def pesticide_recommendation_view(request):
    result = None
    crop_choices = [(c, c) for c in le_crop.classes_]
    pest_choices = [(p, p) for p in le_pest.classes_]

    if request.method == 'POST':
        form = PesticideForm(request.POST, crop_choices=crop_choices, pest_choices=pest_choices)
        if form.is_valid():
            crop_input = form.cleaned_data['crop']
            pest_input = form.cleaned_data['pest']

            crop_encoded = le_crop.transform([crop_input])[0]
            pest_encoded = le_pest.transform([pest_input])[0]

            input_df = pd.DataFrame([[crop_encoded, pest_encoded]], columns=['Crop', 'Pest'])

            pred = xgb_model.predict(input_df)

            pesticide_pred = le_pesticide.inverse_transform([int(pred[0][0])])[0]
            app_method_pred = le_app_method.inverse_transform([int(pred[0][1])])[0]
            dosage_pred = le_dosage.inverse_transform([int(pred[0][2])])[0]

            result = {
                'pesticide': pesticide_pred,
                'method': app_method_pred,
                'dosage': dosage_pred
            }
    else:
        form = PesticideForm(crop_choices=crop_choices, pest_choices=pest_choices)
    return render(request, 'myapp/pesticide_tool.html', {'form': form, 'result': result})