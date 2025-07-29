from django import forms

class FertilizerForm(forms.Form):
    temperature = forms.FloatField(label='Temperature (°C)')
    humidity = forms.FloatField(label='Humidity (%)')
    moisture = forms.FloatField(label='Moisture (%)')
    
    soil_type = forms.ChoiceField(choices=[
        ('Black', 'Black'), ('Clayey', 'Clayey'), ('Loamy', 'Loamy'),
        ('Red', 'Red'), ('Sandy', 'Sandy')
    ])
    
    crop_type = forms.ChoiceField(choices=[
        ('Barley', 'Barley'), ('Cotton', 'Cotton'), ('Ground Nuts', 'Ground Nuts'),
        ('Maize', 'Maize'), ('Millets', 'Millets'), ('Oil seeds', 'Oil seeds'),
        ('Paddy', 'Paddy'), ('Pulses', 'Pulses'), ('Sugarcane', 'Sugarcane'),
        ('Tobacco', 'Tobacco'), ('Wheat', 'Wheat')
    ])
    
    nitrogen = forms.FloatField(label='Nitrogen Level')
    potassium = forms.FloatField(label='Potassium Level')
    phosphorus = forms.FloatField(label='Phosphorus Level')
class CropForm(forms.Form):
    nitrogen = forms.FloatField(label='Nitrogen (N)', min_value=0)
    phosphorous = forms.FloatField(label='Phosphorous (P)', min_value=0)
    potassium = forms.FloatField(label='Potassium (K)', min_value=0)
    temperature = forms.FloatField(label='Temperature (°C)', min_value=-10, max_value=60)
    humidity = forms.FloatField(label='Humidity (%)', min_value=0, max_value=100)
    ph = forms.FloatField(label='Soil pH', min_value=0, max_value=14)
    rainfall = forms.FloatField(label='Rainfall (mm)', min_value=0)
# forms.py

# from django import forms

class PesticideForm(forms.Form):
    crop = forms.ChoiceField(label='Crop')
    pest = forms.ChoiceField(label='Pest')

    def __init__(self, *args, crop_choices=None, pest_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if crop_choices:
            self.fields['crop'].choices = crop_choices
        if pest_choices:
            self.fields['pest'].choices = pest_choices
