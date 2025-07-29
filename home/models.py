from django.db import models

# Create your models here.
class Farmer(models.Model):
    #create data table as user and set attributes features
    farmer_primary_id = models.AutoField(primary_key=True)  # Example primary key
    user_id = models.CharField(max_length=255,unique=True)
    user_name = models.CharField(max_length=255)
    user_area = models.CharField(max_length=255)
    user_village_city = models.CharField(max_length=255)
    user_police_station = models.CharField(max_length=255)
    user_district = models.CharField(max_length=255)
    user_pincode = models.CharField(max_length=10)
    user_state = models.CharField(max_length=255)
    user_country = models.CharField(max_length=255)
    user_dob = models.DateField()
    user_mobile_number = models.CharField(max_length=15)
    user_email = models.EmailField(unique=True)
    user_photo = models.ImageField(upload_to='user_photos/')
    user_password = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name

#create model for convertation between two farmer
#create on 23/04/25
class farmerConversation(models.Model):
    message_id=models.AutoField(primary_key=True)
    sender = models.ForeignKey(Farmer, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Farmer, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.sender} to {self.receiver} at {self.timestamp}'

class farmerQuery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    ]
    query_id=models.AutoField(primary_key=True)
    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE)
    expert = models.ForeignKey('ExpertFarmer', on_delete=models.SET_NULL, null=True, blank=True)
    query_title = models.CharField(max_length=200)
    query_text = models.TextField()
    query_image = models.ImageField(upload_to='query_images/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    solution_text = models.TextField(null=True, blank=True)
    solution_image = models.ImageField(upload_to='solution_images/', null=True, blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.query_title} by {self.farmer}"
    
# add on 20/04/2025 for storing the project details of a user/farmer create in our system and takes guide from us
class farmerProject(models.Model):
    project_id = models.AutoField(primary_key=True)  # Example primary key
    farmer_primary_id = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    crop_name = models.CharField(max_length=255)
    crop_type = models.CharField(max_length=255)
    farm_size = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255)
    farm_address = models.CharField(max_length=10)
    soil_name = models.CharField(max_length=255)
    current_session = models.CharField(max_length=255)
    starting_date = models.DateField()
    complete = models.BooleanField()
    description = models.TextField()
    project_photo = models.ImageField(upload_to='userProjectPhotos/')
    
    def __str__(self):
        return self.project_name
    
#creted on 06/05/2025
# 1. Soil Preparation 
  
from .models import farmerProject 
class farmerSoil(models.Model):
    farmer_soil_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)    
    soil_type = models.CharField(max_length=255)
    ph_level = models.FloatField(null=True, blank=True)
    nitrogen =models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    organic_matter = models.FloatField(null=True, blank=True)
    amendments = models.TextField(blank=True)
    tools_used = models.TextField(blank=True)
    temparature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)

    is_completed = models.BooleanField(default=False)    
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True) 
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")    
    soil_image = models.ImageField(upload_to='farmer_soils/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_soil_id

# 2. Sowing/Planting
class farmerSowing(models.Model):
    farmer_sowing_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    seed_variety = models.CharField(max_length=255)
    seed_treatment = models.TextField(blank=True)
    sowing_time = models.CharField(max_length=255)
    seed_rate = models.FloatField(help_text="kg/acre")
    sowing_method = models.CharField(max_length=255)
    row_spacing = models.CharField(max_length=255)
    sowing_depth = models.CharField(max_length=255)
    equipment_used = models.TextField(blank=True)   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    sowing_image = models.ImageField(upload_to='farmer_sowings/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_sowing_id

# 3. Irrigation
class farmerIrrigation(models.Model):
    farmer_irrigation_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    method = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    water_quality = models.CharField(max_length=255, blank=True)
    water_quantity = models.CharField(max_length=255)   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    irrigation_image = models.ImageField(upload_to='farmer_irrigations/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_irrigation_id

# 4. Fertilizer
class farmerFertilizer(models.Model):
    farmer_fertilizer_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    fertilizer_type = models.CharField(max_length=255)  # e.g. Organic, Chemical
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    application_time = models.CharField(max_length=255)
    application_method = models.TextField()   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    fertilizer_image = models.ImageField(upload_to='farmer_fertilizers/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_fertilizer_id

# 5. Weed Management
class farmerWeed(models.Model):
    farmer_weed_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    weed_name = models.CharField(max_length=255)
    weed_type = models.CharField(max_length=255)
    life_cycle = models.CharField(max_length=255)
    control_method = models.TextField()
    herbicide_used = models.CharField(max_length=255, blank=True)   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    weed_image = models.ImageField(upload_to='farmer_weeds/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_weed_id

# 6. Pest Management
class farmerPest(models.Model):
    farmer_pest_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    pest_name = models.CharField(max_length=255)
    symptoms = models.TextField()
    preventive_measures = models.TextField()
    pesticide_used = models.CharField(max_length=255)
    organic_control = models.TextField(blank=True)   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    pest_image = models.ImageField(upload_to='farmer_pests/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_pest_id

# 7. Disease Management
class farmerDisease(models.Model):
    farmer_disease_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    disease_name = models.CharField(max_length=255)
    symptoms = models.TextField()
    cause = models.CharField(max_length=255)
    treatment = models.TextField()
    risk_factors = models.TextField(blank=True)   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    disease_image = models.ImageField(upload_to='farmer_diseases/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_disease_id

# 8. Growth Stage Monitoring
class farmerGrowthStage(models.Model):
    farmer_growth_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=255)
    expected_days = models.IntegerField()
    growth_stage_description = models.TextField()   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    growth_stage_image = models.ImageField(upload_to='farmer_growth_stages/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_growth_id

# 9. Harvesting
class farmerHarvesting(models.Model):
    farmer_harvesting_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    maturity_signs = models.TextField()
    harvesting_time = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    tools = models.TextField()
    crop_loss_percent = models.FloatField()   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    harvesting_image = models.ImageField(upload_to='farmer_harvestings/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_harvesting_id

# 10. Post Harvesting
class farmerPostHarvesting(models.Model):
    farmer_post_harvesting_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    cleaning = models.TextField()
    sorting = models.TextField()
    drying_method = models.TextField()
    packaging = models.TextField()
    storage_method = models.TextField()
    storage_duration = models.CharField(max_length=255)
    storage_equipment = models.TextField()   
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    ml_prediction = models.CharField(max_length=200, blank=True)
    ml_confidence = models.FloatField(null=True, blank=True, help_text="Confidence score from 0 to 1")
    is_completed = models.BooleanField(default=False)
    post_harvesting_image = models.ImageField(upload_to='farmer_post_harvesting/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_post_harvesting_id

# 11. Additional Metadata
class farmerOthers(models.Model):
    farmer_other_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(farmerProject, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    description = models.TextField()  
    created_at = models.DateField()
    updated_at = models.DateField()
    expert_advise = models.TextField(blank=True, null=True)
    property_image = models.ImageField(upload_to='farmer_others/', blank=True)
    def __str__(self):
        try:
            return f"{self.project.farmer_primary_id.user_name} - {self.project.project_name}"
        except:
            return self.farmer_other_id
        
# expert farmer model
class ExpertFarmer(models.Model):

    expert_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    experience_year = models.DateField()
    specialization = models.CharField(max_length=255,default='')
    farm_size = models.FloatField()
    expert_address = models.CharField(max_length=255,null=True, blank=True)
    crops_grown = models.TextField()
    soil_type = models.CharField(max_length=255,default='')
    irrigation_system = models.CharField(max_length=255,default='')
    fertilizers_used = models.TextField(null=True, blank=True)
    pest_control_methods = models.TextField()
    equipments_owned= models.CharField(max_length=255,default='')
    farming_techniques=models.CharField(max_length=255,default='')
    certifications=models.CharField(max_length=255,default='')
    sustainable_practices=models.CharField(max_length=255,default='')
    technologies_used=models.CharField(max_length=255,default='')
    weather_adaptibility=models.CharField(max_length=255,default='')
    goverment_subsides=models.CharField(max_length=255,default='')
    expert_photo= models.ImageField(upload_to='expertPhotos/') 
    
    def __str__(self):
        return self.name
    
class systemAdmin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=255)
    admin_dob = models.CharField(max_length=100)
    admin_gender = models.CharField(max_length=100)
    admin_address = models.CharField(max_length=100)
    admin_password = models.CharField(max_length=100)
    admin_photo = models.ImageField(upload_to='admin_images/')
    
    def _str_(self):
        return self.name

class adminCrop(models.Model):
    crop_id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(systemAdmin, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=255)
    crop_duration = models.PositiveIntegerField()
    crop_season = models.CharField(max_length=100)
    upload_date = models.CharField(max_length=100)
    crop_image = models.ImageField(upload_to='crop_images/')
    crop_description = models.TextField()

    def __str__(self):
        return self.crop_name

class adminSoil(models.Model):
    soil_id = models.AutoField(primary_key=True)
    soil_type = models.CharField(max_length=100)
    nutrients = models.TextField()
    structure = models.CharField(max_length=100)
    water_holding_capacity = models.FloatField()
    drainage = models.CharField(max_length=100)
    organic_matter = models.FloatField()
    soil_depth = models.FloatField()
    equipments = models.TextField()
    soil_image = models.ImageField(upload_to='soil_images/')
    description = models.TextField()
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)

    def _str_(self):
        return self.soil_type

class adminSeed(models.Model):
    seed_id = models.AutoField(primary_key=True)
    admin_crop = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    variety = models.CharField(max_length=100)
    rate_per_area = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    germination_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    purity_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    moisture_content = models.DecimalField(max_digits=5, decimal_places=2)
    equipments = models.CharField(max_length=255)
    seed_image = models.ImageField(upload_to='seed_images/')
    description = models.TextField()

    def _str_(self):
        return f"{self.variety} - {self.admin_crop.crop_name}"

class adminSowing(models.Model):
    sowing_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    method = models.CharField(max_length=100)
    spacing = models.CharField(max_length=100)
    depth = models.CharField(max_length=100)
    best_time = models.CharField(max_length=100)
    land_preparation = models.TextField()
    soil_moisture = models.CharField(max_length=100)
    sowing_tools = models.CharField(max_length=255)
    seed_coverage = models.CharField(max_length=255)
    pre_sowing_irrigation = models.TextField()
    post_sowing_practice = models.TextField()
    sowing_image = models.ImageField(upload_to='sowing_images/')
    description = models.TextField()

    def _str_(self):
        return f"{self.method} - {self.crop_id.crop_name}"

class adminIrrigation(models.Model):
    irrigation_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    irrigation_method = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    rate_per_area = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    irrigation_timing = models.CharField(max_length=100)
    water_quantity = models.CharField(max_length=100)
    water_quality = models.CharField(max_length=100)
    drainage_considerations = models.TextField()
    control_system = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    irrigation_image = models.ImageField(upload_to='irrigation_images/')
    description = models.TextField()

    def _str_(self):
        return f"{self.irrigation_method} - {self.crop_id.crop_name}"

class adminFertilizer(models.Model):
    fertilizer_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    organic_compost = models.CharField(max_length=200)
    chemical_urea = models.CharField(max_length=200)
    chemical_dap = models.CharField(max_length=200)
    nurient_composition = models.TextField()
    application_method = models.CharField(max_length=200)
    application_timing = models.CharField(max_length=200)
    application_frequency = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    storage = models.CharField(max_length=200)
    equipments = models.CharField(max_length=200)
    fertilizer_image = models.ImageField(upload_to='fertilizer_images/')
    description = models.TextField()

    def _str_(self):
        return f"Fertilizer for {self.crop_id.crop_name}"
    
class adminPest(models.Model):
    pest_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    pest_name = models.CharField(max_length=200)
    pest_type = models.CharField(max_length=200)
    pest_life_cycle = models.TextField()
    symptoms = models.TextField()
    affected_plant_parts = models.CharField(max_length=200)
    pest_seasonality = models.CharField(max_length=200)
    pest_damage_level = models.CharField(max_length=200)
    detection_method = models.TextField()
    control_measures = models.TextField()
    recommended_pesticides = models.TextField()
    resistance_risk = models.CharField(max_length=200)
    environment_effect = models.TextField()
    friendly_tips = models.TextField()
    equipments = models.CharField(max_length=200)
    pest_image = models.ImageField(upload_to='pest_images/')
    description = models.TextField()

    def _str_(self):
        return self.pest_name

class adminWeed(models.Model):
    weed_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    weed_name = models.CharField(max_length=100)
    weed_type = models.CharField(max_length=100)
    growth_habit = models.CharField(max_length=100)
    life_cycle = models.CharField(max_length=100)
    time_of_appearence = models.CharField(max_length=100)
    affected_crop_growth_stage = models.CharField(max_length=100)
    area_of_infestation = models.TextField()
    competitive_impact_on_crop = models.TextField()
    leaf_shape = models.CharField(max_length=100)
    leaf_color = models.CharField(max_length=100)
    root_structure = models.TextField()
    control_measures = models.TextField()
    herbicide_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    application_time = models.CharField(max_length=100)
    herbicide_resistance_risk = models.TextField()
    weed_dispersal_method = models.TextField()
    environment_effect = models.TextField()
    equipments = models.CharField(max_length=100)
    weed_image = models.ImageField(upload_to='weed_images/')
    description = models.TextField()

    def _str_(self):
        return self.weed_name

class adminDisease(models.Model):
    disease_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    disease_name = models.CharField(max_length=100)
    causal_organism = models.CharField(max_length=100)
    mode_of_transmission = models.CharField(max_length=100)
    symptoms = models.TextField()
    affected_plant_parts = models.TextField()
    disease_cycle = models.TextField()
    favorable_condition_for_disease = models.TextField()
    seasonality = models.CharField(max_length=100)
    method_of_diagnosis = models.TextField()
    control_measures = models.TextField()
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    application_method = models.CharField(max_length=100)
    impact_on_crop_quality = models.TextField()
    resistance_risk = models.CharField(max_length=100)
    geographic_spread = models.TextField()
    environment_effect_of_medicine = models.TextField()
    equipments = models.CharField(max_length=200)
    disease_image = models.ImageField(upload_to='disease_images/')
    description = models.TextField()

    def _str_(self):
        return self.disease_name
    
class adminHarvesting(models.Model):
    harvesting_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    time = models.CharField(max_length=100)
    drying = models.TextField()
    storage = models.TextField()
    optimal_harvesting_period = models.CharField(max_length=100)
    method_of_harvesting = models.CharField(max_length=100)
    equipments = models.TextField()
    labor_requirement = models.CharField(max_length=100)
    yield_quantity = models.CharField(max_length=100)
    moisture_content = models.CharField(max_length=100)
    post_harvesting_handling = models.TextField()
    transportation_requirement = models.TextField()
    challenges = models.TextField()
    crop_loss_percentage = models.CharField(max_length=50)
    market_readiness = models.CharField(max_length=100)
    safty_practice = models.TextField()
    harvesting_image = models.ImageField(upload_to='harvesting_images/')
    description = models.TextField()

    def _str_(self):
        return f"{self.cropId.crop_name} Harvesting"

class adminPostHarvesting(models.Model):
    post_harvesting_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    cleaning = models.TextField()
    sorting = models.TextField()
    drying = models.TextField()
    curing = models.TextField()
    packaging = models.TextField()
    storage = models.TextField()
    waste_management = models.TextField()
    market_preparation = models.TextField()
    equipments = models.TextField()
    post_harvesting_image = models.ImageField(upload_to='post_harvest_images/')
    description = models.TextField()

    def _str_(self):
        return f"{self.crop_id.crop_name} - Post Harvesting Info"
    
class adminOthers(models.Model):
    others_id = models.AutoField(primary_key=True)
    crop_id = models.ForeignKey(adminCrop, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100)
    property_image = models.ImageField(upload_to='others_images/')
    description = models.TextField()

    def _str_(self):
        return self.property_name




    
# creating models for expert pannel on 19/04/2025
from django.db import models

class expertVideo(models.Model):
    
    video_id = models.AutoField(primary_key=True)
    expert_id = models.ForeignKey('ExpertFarmer', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='expertVideos/')  # OR use video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='expertThumbnails/', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    views = models.IntegerField(default=0) 
    def __str__(self):
        return self.title
