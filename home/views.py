from django.shortcuts import render,HttpResponse,redirect
from django.shortcuts import get_object_or_404,Http404
from home.models import Farmer
from home.models import systemAdmin,adminCrop
from datetime import datetime
from datetime import date
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt,csrf_protect,requires_csrf_token

from django.db.models.functions import ExtractMonth
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request,"index.html")

#added on 16/04/2025
def category(request):
    crops=adminCrop.objects.all()
    crop_types = adminCrop.objects.values_list('crop_type', flat=True).distinct()
    return render(request,"category.html",{'crop_types':crop_types,'crops':crops})

#added on 17/04/2025
def everyCropProcess(request, crop_id):
    crop = adminCrop.objects.get(pk=crop_id)
    soils = adminSoil.objects.filter(crop_id=crop_id)
    sowings = adminSowing.objects.filter(crop_id=crop_id)
    fertilizers = adminFertilizer.objects.filter(crop_id=crop_id)
    weeds = adminWeed.objects.filter(crop_id=crop_id)
    pests = adminPest.objects.filter(crop_id=crop_id)
    diseases = adminDisease.objects.filter(crop_id=crop_id)
    harvestings = adminHarvesting.objects.filter(crop_id=crop_id)
    post_harvestings = adminPostHarvesting.objects.filter(crop_id=crop_id)
    seeds = adminSeed.objects.filter(admin_crop=crop_id)
    irrigations = adminIrrigation.objects.filter(crop_id=crop_id) 
    others = adminOthers.objects.filter(crop_id=crop_id)
    return render(request, "everyCropProcess.html", {
        'crop': crop,
        'soils': soils,
        'sowings': sowings,
        'fertilizers': fertilizers,
        'weeds': weeds,
        'pests': pests,
        'diseases': diseases,
        'harvestings': harvestings,
        'post_harvestings': post_harvestings,
        'seeds': seeds,
        'irrigations': irrigations,  
        'others': others,

    })


def registration(request):
    flag={
            'status':""
        }
    if request.method=="POST":        
        user_id=request.POST.get('user_id')
        user_name=request.POST.get('user_name')
        user_area=request.POST.get('user_area')
        user_village_city=request.POST.get('user_village_city')
        user_police_station=request.POST.get('user_police_station')
        user_district=request.POST.get('user_district')
        user_pincode=request.POST.get('user_pincode')
        user_state=request.POST.get('user_state')
        user_country=request.POST.get('user_country')
        user_dob=request.POST.get('user_dob')
        user_mobile_number=request.POST.get('user_mobile_number')
        user_email=request.POST.get('user_email')
        user_photo=request.FILES.get('user_photo') # changed the line in 17/04/2025
        
        user_password=request.POST.get('user_password')
        var=Farmer(user_id=user_id,user_name=user_name,user_area=user_area,user_village_city= user_village_city,user_police_station=user_police_station,user_district= user_district,user_pincode=user_pincode,user_state=user_state,user_country=user_country,user_dob=user_dob,user_mobile_number=user_mobile_number,user_email=user_email,user_photo=user_photo,user_password=user_password)
        var.save()
        if var:
            flag={
                'status':"Submitted successfully"
            }
        messages.success(request,"Your has been submitted successfully.")

    return render(request,"signUp.html",flag)
#created on 19/04/2025
from django.contrib.auth.hashers import check_password
def login(request):
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_password = request.POST.get('user_password')

        farmer = Farmer.objects.filter(user_id=user_id,user_password=user_password).first()
        if farmer:
            user_id = farmer.farmer_primary_id
            request.session['farmer_primary_id'] = user_id
            return render(request,"userLogin.html",{'farmer':farmer})
            # return redirect("index")

    return render(request,"userLogin.html")

from django.contrib.auth import logout
def logoutUser(request):    
    if 'farmer_primary_id' in request.session:
        del request.session['farmer_primary_id']
    return redirect("/")


#created on 19/04/2025
def profile(request):
    user_id = request.session.get('farmer_primary_id')
    if  user_id:
        farmer= Farmer.objects.get(farmer_primary_id=user_id)
        ongoing_projects=farmerProject.objects.filter(
            farmer_primary_id=farmer.farmer_primary_id,
            complete=False).order_by('starting_date')
        completed_projects=farmerProject.objects.filter(
            farmer_primary_id=farmer.farmer_primary_id,
            complete=True).order_by('starting_date')
        return render(request,"profile.html",{'farmer':farmer,
                                              'ongoing_projects':ongoing_projects,
                                              'completed_projects':completed_projects})
    return render(request,"profile.html")

# created on 26/05/25
from django.shortcuts import render
from django.db.models import Q
from .models import (
    adminCrop, adminSoil, adminSeed, adminSowing, adminIrrigation, adminFertilizer,
    adminPest, adminWeed, adminDisease, adminHarvesting, adminPostHarvesting, adminOthers,
    expertVideo, Farmer, ExpertFarmer, farmerQuery, farmerProject
)

def search_results(request):
    keyword = request.GET.get('q', '').strip()
    farmer_id = request.session.get('farmer_primary_id')

    crop_docs = adminCrop.objects.filter(Q(crop_name__icontains=keyword) | Q(crop_description__icontains=keyword))
    soils = adminSoil.objects.filter(Q(soil_type__icontains=keyword) | Q(description__icontains=keyword))
    seeds = adminSeed.objects.filter(Q(variety__icontains=keyword) | Q(description__icontains=keyword))
    sowings = adminSowing.objects.filter(Q(method__icontains=keyword) | Q(description__icontains=keyword))
    irrigations = adminIrrigation.objects.filter(Q(irrigation_method__icontains=keyword) | Q(description__icontains=keyword))
    fertilizers = adminFertilizer.objects.filter(Q(organic_compost__icontains=keyword) | Q(description__icontains=keyword))
    pests = adminPest.objects.filter(Q(pest_name__icontains=keyword) | Q(description__icontains=keyword))
    weeds = adminWeed.objects.filter(Q(weed_name__icontains=keyword) | Q(description__icontains=keyword))
    diseases = adminDisease.objects.filter(Q(disease_name__icontains=keyword) | Q(description__icontains=keyword))
    harvestings = adminHarvesting.objects.filter(Q(time__icontains=keyword) | Q(description__icontains=keyword))
    postharvests = adminPostHarvesting.objects.filter(Q(cleaning__icontains=keyword) | Q(description__icontains=keyword))
    others = adminOthers.objects.filter(Q(property_name__icontains=keyword) | Q(description__icontains=keyword))

    videos = expertVideo.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
    farmers = Farmer.objects.filter(Q(user_name__icontains=keyword) | Q(user_village_city__icontains=keyword))
    experts ={}
    queries = {}
    if farmer_id:
        experts = ExpertFarmer.objects.filter(Q(name__icontains=keyword) | Q(specialization__icontains=keyword))    
        queries = farmerQuery.objects.filter(Q(query_title__icontains=keyword) | Q(query_text__icontains=keyword))

    user_projects = farmerProject.objects.none()
    categories ={}
    if farmer_id:
        user_projects = farmerProject.objects.filter(farmer_primary_id=farmer_id).filter(
            Q(project_name__icontains=keyword) | Q(description__icontains=keyword)
        )
        categories = "crop,soil,seed,sowing,irrigation,fertilizer,pest,weed,disease,harvest,postharvest,others,video,farmer,expert,query,project".split(',')


    return render(request, 'search_results.html', {
        'keyword': keyword,
        'crop_docs': crop_docs, 'soils': soils, 'seeds': seeds, 'sowings': sowings,
        'irrigations': irrigations, 'fertilizers': fertilizers, 'pests': pests, 'weeds': weeds,
        'diseases': diseases, 'harvestings': harvestings, 'postharvests': postharvests, 'others': others,
        'videos': videos, 'farmers': farmers, 'experts': experts, 'queries': queries,
        'user_projects': user_projects,
        'categories':categories
    })




#created on 23/04/25
from home.models import farmerConversation
def community(request):    
    sender_id=request.session.get('farmer_primary_id')
    sender=Farmer.objects.get(pk=sender_id)

    conversations = farmerConversation.objects.filter(
        Q(sender=sender) | Q(receiver=sender)
    )

    # Get all unique farmers involved in conversations with the logged-in farmer
    partner_ids = set()
    partner_latest_timestamp = {}
    for convo in conversations:
        # Identify the conversation partner
        partner = convo.receiver if convo.sender == sender else convo.sender

        # Skip if the partner is the logged-in farmer
        if partner == sender:
            continue
        if (partner not in partner_latest_timestamp) or (convo.timestamp > partner_latest_timestamp[partner]):
            partner_latest_timestamp[partner] = convo.timestamp

     # Sort partners by latest message timestamp in descending order
    sorted_partners = sorted(partner_latest_timestamp.items(), key=lambda x: x[1], reverse=True)
    # Fetch Farmer objects of those partners
    farmers= [partner for partner, timestamp in sorted_partners]
    
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'search':
            search_query = request.POST.get('query')
            if search_query:
                farmers = Farmer.objects.filter(user_name__icontains=search_query)
                messages.info(request, f'Search results for "{search_query}"')

    
    return render(request,"community.html",{'farmers':farmers})


from django.db.models import Q
from django.utils import timezone
def eachMessage(request,receiver_id):
    sender_id=request.session.get('farmer_primary_id')
    sender=Farmer.objects.get(pk=sender_id)

    conversations = farmerConversation.objects.filter(
        Q(sender=sender) | Q(receiver=sender)
    )

    # Get all unique farmers involved in conversations with the logged-in farmer
    partner_ids = set()
    partner_latest_timestamp = {}
    for convo in conversations:
        # Identify the conversation partner
        partner = convo.receiver if convo.sender == sender else convo.sender

        # Skip if the partner is the logged-in farmer
        if partner == sender:
            continue
        if (partner not in partner_latest_timestamp) or (convo.timestamp > partner_latest_timestamp[partner]):
            partner_latest_timestamp[partner] = convo.timestamp

     # Sort partners by latest message timestamp in descending order
    sorted_partners = sorted(partner_latest_timestamp.items(), key=lambda x: x[1], reverse=True)
    # Fetch Farmer objects of those partners
    farmers= [partner for partner, timestamp in sorted_partners]
    receiver=Farmer.objects.get(pk=receiver_id)
    sender_id=request.session.get('farmer_primary_id')
    sender=Farmer.objects.get(pk=sender_id)
    messages = farmerConversation.objects.filter(
        Q(sender=sender, receiver=receiver) |
        Q(sender=receiver, receiver=sender)
    ).order_by('timestamp')
    messages_counter=farmerConversation.objects.filter(
        Q(sender=sender, receiver=receiver) |
        Q(sender=receiver, receiver=sender)
    ).order_by('timestamp').count()
    if request.method == "POST":
        message_text = request.POST.get('message')
        var=farmerConversation(
            sender=sender,
            receiver=receiver,
            message=message_text
        ) 
        var.save()

    return render(request,"eachMessage.html",{'farmers':farmers,
                                              'receiver':receiver,
                                              'messages':messages,
                                              'messages_counter':messages_counter,
                                              'today': timezone.localdate(),})




#create on 20/04/2024
from home.models import farmerProject
def addProject(request):
    
    if request.method=="POST":
        project_name=request.POST.get('project_name')
        crop_type=request.POST.get('crop_type')
        crop_name=request.POST.get('crop_name')
        farm_size=request.POST.get('farm_size')
        farm_location=request.POST.get('farm_location')
        farm_address=request.POST.get('farm_address')
        soil_name=request.POST.get('soil_name')
        current_session=request.POST.get('current_session')
        starting_date=request.POST.get('starting_date')
        project_photo=request.FILES.get('project_photo')
        description=request.POST.get('description')
        farmer_primary_id=request.session.get('farmer_primary_id')
        farmer=Farmer.objects.get(pk=farmer_primary_id)
        obj=farmerProject(
            farmer_primary_id=farmer,
            project_name=project_name,
            crop_name=crop_name,
            crop_type=crop_type,
            farm_size=farm_size,
            farm_location=farm_location,
            farm_address=farm_address,
            soil_name=soil_name,
            current_session=current_session,
            starting_date=starting_date,
            description=description,
            project_photo=project_photo,
            complete=False
        )
        obj.save()
        return redirect("profile") 

    return render(request,"addProject.html")

# add on 21/04/2025
def ongoingProject(request,project_id):
    project=farmerProject.objects.get(pk=project_id)
    stages = [
        ('Prepare Soil', farmerSoil.objects.filter(project=project).first(), 'soil_image'),
        ('Sowing/Planting', farmerSowing.objects.filter(project=project).first(), 'sowing_image'),
        ('Irrigation', farmerIrrigation.objects.filter(project=project).first(), 'irrigation_image'),
        ('Fertilizer', farmerFertilizer.objects.filter(project=project).first(), 'fertilizer_image'),
        ('Weed Management', farmerWeed.objects.filter(project=project).first(), 'weed_image'),
        ('Pest Management', farmerPest.objects.filter(project=project).first(), 'pest_image'),
        ('Disease Management', farmerDisease.objects.filter(project=project).first(), 'disease_image'),
        ('Growth Stage', farmerGrowthStage.objects.filter(project=project).first(), 'growth_stage_image'),
        ('Harvesting', farmerHarvesting.objects.filter(project=project).first(), 'harvesting_image'),
        ('Post Harvesting', farmerPostHarvesting.objects.filter(project=project).first(), 'post_harvesting_image'),
        ('Others', farmerOthers.objects.filter(project=project).first(), 'property_image'),
    ]

    steps = []
    pie_labels = []
    pie_durations = []

    previous_updated = None

    for label, step, image_field in stages:
        if step and (step.expert_advise or step.ml_prediction or getattr(step, 'farmer_done', None)):
            step.stage_name = label
            step.image_url = getattr(step, image_field).url if getattr(step, image_field) else None
            steps.append(step)

            if previous_updated:
                duration = (step.updated_at - previous_updated).total_seconds() / 3600  # in hours
                pie_durations.append(round(duration, 2))
            else:
                pie_durations.append(0)

            pie_labels.append(label)
            previous_updated = step.updated_at

    # Dummy emergency alert system
    emergency_alerts = [
        {"message": "Heavy rainfall expected in your region", "date": "2025-05-18"},
        {"message": "Flood warning issued", "date": "2025-05-17"}
    ]

    context = {
        'project': project,
        'steps': steps,
        'pieLabels': pie_labels,
        'pieDurations': pie_durations,
        'emergency_alerts': emergency_alerts
    }

    return render(request,"ongoingProject.html",context)

# farmer project operation functions created on 06/05/2025
# register the models for farmer project's action
from home.models import farmerSoil ,farmerSowing,farmerIrrigation,farmerFertilizer,farmerWeed,farmerPest,farmerDisease,farmerGrowthStage,farmerHarvesting,farmerPostHarvesting,farmerOthers

# 1. SOIL

def ongoingProjectSoil(request,project_id):
    project = farmerProject.objects.get(pk=project_id)
    soils = farmerSoil.objects.filter(project=project)
    para={
        'project':project,
        'soils':soils
    }
        

    return render(request,"ongoingProjectSoil.html",para)

def submit_farmerSoil(request):
    if request.method == "POST":
        p_id=request.POST.get("project_id")
        project = farmerProject.objects.get(pk=p_id)
        soil_type = request.POST.get("soil_type")
        ph_level = request.POST.get("ph_level")
        nitrogen = request.POST.get("nitrogen")
        phosphorus = request.POST.get("phosphorus")
        potassium = request.POST.get("potassium")
        organic_matter = request.POST.get("organic_matter")
        temparature = request.POST.get("temparature")
        humidity = request.POST.get("humidity")
        amendments = request.POST.get("amendments")
        tools_used = request.POST.get("tools_used")
        soil_image = request.FILES.get("soil_image")

        current_datetime = datetime.now()
        # Save to database
        farmerSoil.objects.create(
            project=project,
            soil_type=soil_type,
            ph_level=ph_level,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            organic_matter=organic_matter,
            temparature=temparature,
            humidity=humidity,
            amendments=amendments,
            tools_used=tools_used,
            created_at=current_datetime,
            updated_at=current_datetime,
            soil_image=soil_image
        )

    return redirect("ongoingProjectSoil",project_id=p_id)
 
def ongoingProjectSoilUpdate(request,project_id,farmer_soil_id): # for updating existing recordes by farmer
    project = get_object_or_404(farmerProject, pk=project_id)
    soil = get_object_or_404(farmerSoil, pk=farmer_soil_id, project=project)
    return render(request,"ongoingProjectSoilUpdate.html")


# 2. SOWING 
from .models import farmerSowing

def ongoingProjectSowing(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    sowings = farmerSowing.objects.filter(project=project)
    return render(request, "ongoingProjectSowing.html", {'project': project, 'sowings': sowings})

def submit_farmerSowing(request):
    if request.method == "POST":
        p_id = request.POST.get("project_id")
        project = get_object_or_404(farmerProject, pk=p_id)
        soil = get_object_or_404(farmerSoil, project=project)

        seed_variety = request.POST.get("seed_variety")
        seed_treatment = request.POST.get("seed_treatment")
        sowing_time = request.POST.get("sowing_time")
        seed_rate = request.POST.get("seed_rate")
        sowing_method = request.POST.get("sowing_method")
        row_spacing = request.POST.get("row_spacing")
        sowing_depth = request.POST.get("sowing_depth")
        equipment_used = request.POST.get("equipment_used")
        sowing_image = request.FILES.get("sowing_image")

        now = datetime.now()

        farmerSowing.objects.create(
            project=project,
            seed_variety=seed_variety,
            seed_treatment=seed_treatment,
            sowing_time=sowing_time,
            seed_rate=seed_rate,
            sowing_method=sowing_method,
            row_spacing=row_spacing,
            sowing_depth=sowing_depth,
            equipment_used=equipment_used,
            created_at=now,
            updated_at=now,
            sowing_image=sowing_image
        )
        soil.is_completed=True
        soil.save()

        return redirect("ongoingProjectSowing", project_id=p_id)


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import farmerProject, farmerIrrigation, farmerFertilizer, farmerWeed, farmerPest, farmerDisease, farmerGrowthStage, farmerHarvesting, farmerPostHarvesting, farmerOthers
from datetime import datetime

# 3. IRRIGATION

def ongoingProjectIrrigation(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    irrigations = farmerIrrigation.objects.filter(project=project)
    return render(request, "ongoingProjectIrrigation.html", {'project': project, 'irrigations': irrigations})

def submit_farmerIrrigation(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        now = datetime.now()
        farmerIrrigation.objects.create(
            project=project,
            method=request.POST.get("method"),
            frequency=request.POST.get("frequency"),
            water_quality=request.POST.get("water_quality"),
            water_quantity=request.POST.get("water_quantity"),
            created_at=now,
            updated_at=now,
            irrigation_image=request.FILES.get("irrigation_image")
        )
    return redirect("ongoingProjectIrrigation", project_id=project.project_id)

# 4. FERTILIZER

def ongoingProjectFertilizer(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    fertilizers = farmerFertilizer.objects.filter(project=project)
    return render(request, "ongoingProjectFertilizer.html", {'project': project, 'fertilizers': fertilizers})

def submit_farmerFertilizer(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        now = datetime.now()
        farmerFertilizer.objects.create(
            project=project,
            fertilizer_type=request.POST.get("fertilizer_type"),
            name=request.POST.get("name"),
            dosage=request.POST.get("dosage"),
            application_time=request.POST.get("application_time"),
            application_method=request.POST.get("application_method"),
            created_at=now,
            updated_at=now,
            fertilizer_image=request.FILES.get("fertilizer_image")
        )
    return redirect("ongoingProjectFertilizer", project_id=project.project_id)

# 5. WEED

def ongoingProjectWeed(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    weeds = farmerWeed.objects.filter(project=project)
    return render(request, "ongoingProjectWeed.html", {'project': project, 'weeds': weeds})

def submit_farmerWeed(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        now = datetime.now()
        farmerWeed.objects.create(
            project=project,
            weed_name=request.POST.get("weed_name"),
            weed_type=request.POST.get("weed_type"),
            life_cycle=request.POST.get("life_cycle"),
            control_method=request.POST.get("control_method"),
            herbicide_used=request.POST.get("herbicide_used"),
            created_at=now,
            updated_at=now,
            weed_image=request.FILES.get("weed_image")
        )
    return redirect("ongoingProjectWeed", project_id=project.project_id)

# 6. PEST

def ongoingProjectPest(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    pests = farmerPest.objects.filter(project=project)
    return render(request, "ongoingProjectPest.html", {'project': project, 'pests': pests})

def submit_farmerPest(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        now = datetime.now()
        farmerPest.objects.create(
            project=project,
            pest_name=request.POST.get("pest_name"),
            symptoms=request.POST.get("symptoms"),
            preventive_measures=request.POST.get("preventive_measures"),
            pesticide_used=request.POST.get("pesticide_used"),
            organic_control=request.POST.get("organic_control"),
            created_at=now,
            updated_at=now,
            pest_image=request.FILES.get("pest_image")
        )
    return redirect("ongoingProjectPest", project_id=project.project_id)

# 7. DISEASE

def ongoingProjectDisease(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    diseases = farmerDisease.objects.filter(project=project)
    return render(request, "ongoingProjectDisease.html", {'project': project, 'diseases': diseases})

def submit_farmerDisease(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        now = datetime.now()
        farmerDisease.objects.create(
            project=project,
            disease_name=request.POST.get("disease_name"),
            symptoms=request.POST.get("symptoms"),
            cause=request.POST.get("cause"),
            treatment=request.POST.get("treatment"),
            risk_factors=request.POST.get("risk_factors"),
            created_at=now,
            updated_at=now,
            disease_image=request.FILES.get("disease_image")
        )
    return redirect("ongoingProjectDisease", project_id=project.project_id)

# 8. GROWTH

def ongoingProjectGrowth(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    growths = farmerGrowthStage.objects.filter(project=project)
    return render(request, "ongoingProjectGrowth.html", {'project': project, 'growths': growths})

def submit_farmerGrowth(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        sowing = get_object_or_404(farmerSowing, project=project)
        sowing.is_completed=True
        sowing.save()
        now = datetime.now()
        farmerGrowthStage.objects.create(
            project=project,
            stage_name=request.POST.get("stage_name"),
            expected_days=request.POST.get("expected_days"),
            growth_stage_description=request.POST.get("growth_stage_description"),
            created_at=now,
            updated_at=now,
            growth_stage_image=request.FILES.get("growth_stage_image")
        )
    return redirect("ongoingProjectGrowth", project_id=project.project_id)

# 9. HARVESTING

def ongoingProjectHarvesting(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    harvestings = farmerHarvesting.objects.filter(project=project)
    return render(request, "ongoingProjectHarvesting.html", {'project': project, 'harvestings': harvestings})

def submit_farmerHarvesting(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        growth = get_object_or_404(farmerGrowthStage, project=project)
        growth.is_completed=True
        growth.save()
        now = datetime.now()
        farmerHarvesting.objects.create(
            project=project,
            maturity_signs=request.POST.get("maturity_signs"),
            harvesting_time=request.POST.get("harvesting_time"),
            method=request.POST.get("method"),
            tools=request.POST.get("tools"),
            crop_loss_percent=request.POST.get("crop_loss_percent"),
            created_at=now,
            updated_at=now,
            harvesting_image=request.FILES.get("harvesting_image")
        )
    return redirect("ongoingProjectHarvesting", project_id=project.project_id)

# 10. POST HARVESTING

def ongoingProjectPostHarvesting(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    postharvests = farmerPostHarvesting.objects.filter(project=project)
    return render(request, "ongoingProjectPostHarvesting.html", {'project': project, 'postharvests': postharvests})

def submit_farmerPostHarvesting(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        harvesting = get_object_or_404(farmerHarvesting, project=project)
        harvesting.is_completed=True
        harvesting.save()
        now = datetime.now()
        farmerPostHarvesting.objects.create(
            project=project,
            cleaning=request.POST.get("cleaning"),
            sorting=request.POST.get("sorting"),
            drying_method=request.POST.get("drying_method"),
            packaging=request.POST.get("packaging"),
            storage_method=request.POST.get("storage_method"),
            storage_duration=request.POST.get("storage_duration"),
            storage_equipment=request.POST.get("storage_equipment"),
            created_at=now,
            updated_at=now,
            post_harvesting_image=request.FILES.get("post_harvesting_image")
        )
    return redirect("ongoingProjectPostHarvesting", project_id=project.project_id)

# 11. OTHERS

def ongoingProjectOthers(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    others = farmerOthers.objects.filter(project=project)
    return render(request, "ongoingProjectOthers.html", {'project': project, 'others': others})

def submit_farmerOthers(request):
    if request.method == "POST":
        project = get_object_or_404(farmerProject, pk=request.POST.get("project_id"))
        now = datetime.now()
        farmerOthers.objects.create(
            project=project,
            property_name=request.POST.get("property_name"),
            description=request.POST.get("description"),
            created_at=now,
            updated_at=now,
            property_image=request.FILES.get("property_image")
        )
    return redirect("ongoingProjectOthers", project_id=project.project_id)





def video(request):
    videos = expertVideo.objects.all()
    return render(request, "video.html", {"videos": videos})

def playingRecordedVideo(request, video_id):
    video = get_object_or_404(expertVideo, video_id=video_id)

    # Optional: update view count
    video.views += 1
    video.save()

    # You can also fetch recommended videos (e.g., same category)
    recommended_videos = expertVideo.objects.exclude(video_id=video_id)[:3]

    return render(request, "playingRecordedVideo.html", {
        "video": video,
        "recommended_videos": recommended_videos
    })


def about(request): # add on 17/04/2025

    return render(request,"about.html")

def expertForUser(request): # add on 18/04/2025
    experts=ExpertFarmer.objects.all()
    return render(request,"expert.html",{'experts':experts})

from home.models import farmerQuery
def userQuery(request):# add on 25/04/2025
    farmer_id=request.session.get('farmer_primary_id')
    farmer=Farmer.objects.get(pk=farmer_id)
    queries = farmerQuery.objects.filter(farmer=farmer).order_by('submitted_at')
    return render(request,"userQuery.html", {'queries': queries})

def addQuery(request):# add on 25/04/2025
    if request.method == 'POST':
        query_title = request.POST.get('query_title')
        query_text = request.POST.get('query_text')
        query_image = request.FILES.get('query_image')
        farmer_id=request.session.get('farmer_primary_id')
        farmer=Farmer.objects.get(pk=farmer_id)
        farmerQuery.objects.create(
            farmer=farmer,
            query_title=query_title,
            query_text=query_text,
            query_image=query_image,
            submitted_at=datetime.now(),
            status='pending'
        )
        return redirect("userQuery")
    return render(request,"addQuery.html")

#admin view
def adminHome(request):
    # Project Tasks By Status
    completed=farmerPostHarvesting.objects.filter(is_completed=True).values('project_id').distinct().count()
    work_in_progress=farmerSowing.objects.values('project_id').distinct().count()
    created_project=farmerProject.objects.all().count()
    planed_project=farmerSoil.objects.values('project_id').distinct().count()
    task_status=[completed,work_in_progress,created_project,planed_project]

    # Project Tasks Created vs Completed

    # created Projects
    jan_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=1).values('project_id').distinct().count()
    feb_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=2).values('project_id').distinct().count()
    mar_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=3).values('project_id').distinct().count()
    apr_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=4).values('project_id').distinct().count()
    may_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=5).values('project_id').distinct().count()
    jun_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=6).values('project_id').distinct().count()
    jul_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=7).values('project_id').distinct().count()
    aug_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=8).values('project_id').distinct().count()
    sep_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=9).values('project_id').distinct().count()
    oct_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=10).values('project_id').distinct().count()
    nov_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=11).values('project_id').distinct().count()
    dec_created=farmerProject.objects.annotate(month=ExtractMonth('starting_date')).filter(month=12).values('project_id').distinct().count()
    monthly_created_project=[jan_created,feb_created,mar_created,apr_created,may_created,jun_created,
                             jul_created,aug_created,sep_created,oct_created,nov_created,dec_created]
    
    # Completed Projects
    jan_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=1).filter(is_completed=True).values('project_id').distinct().count()
    feb_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=2).filter(is_completed=True).values('project_id').distinct().count()
    mar_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=3).filter(is_completed=True).values('project_id').distinct().count()
    apr_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=4).filter(is_completed=True).values('project_id').distinct().count()
    may_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=5).filter(is_completed=True).values('project_id').distinct().count()
    jun_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=6).filter(is_completed=True).values('project_id').distinct().count()
    jul_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=7).filter(is_completed=True).values('project_id').distinct().count()
    aug_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=8).filter(is_completed=True).values('project_id').distinct().count()
    sep_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=9).filter(is_completed=True).values('project_id').distinct().count()
    oct_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=10).filter(is_completed=True).values('project_id').distinct().count()
    nov_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=11).filter(is_completed=True).values('project_id').distinct().count()
    dec_completed=farmerPostHarvesting.objects.annotate(month=ExtractMonth('updated_at')).filter(month=12).filter(is_completed=True).values('project_id').distinct().count()
    monthly_completed_project=[jan_completed,feb_completed,mar_completed,apr_completed,may_completed,jun_completed,
                             jul_completed,aug_completed,sep_completed,oct_completed,nov_completed,dec_completed]

    # Monthly Workload     
        #   completed_project will same as previous section so don't need recalculate
        # projects in working progress        
    jan_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=1).values('project_id').distinct().count()
    feb_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=2).values('project_id').distinct().count()
    mar_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=3).values('project_id').distinct().count()
    apr_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=4).values('project_id').distinct().count()
    may_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=5).values('project_id').distinct().count()
    jun_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=6).values('project_id').distinct().count()
    jul_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=7).values('project_id').distinct().count()
    aug_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=8).values('project_id').distinct().count()
    sep_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=9).values('project_id').distinct().count()
    oct_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=10).values('project_id').distinct().count()
    nov_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=11).values('project_id').distinct().count()
    dec_progress=farmerSowing.objects.annotate(month=ExtractMonth('updated_at')).filter(month=12).values('project_id').distinct().count()
    monthly_progress_project=[jan_progress,feb_progress,mar_progress,apr_progress,may_progress,jun_progress,
                             jul_progress,aug_progress,sep_progress,oct_progress,nov_progress,dec_progress]
    
        #  projects are started  
    jan_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=1).values('project_id').distinct().count()
    feb_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=2).values('project_id').distinct().count()
    mar_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=3).values('project_id').distinct().count()
    apr_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=4).values('project_id').distinct().count()
    may_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=5).values('project_id').distinct().count()
    jun_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=6).values('project_id').distinct().count()
    jul_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=7).values('project_id').distinct().count()
    aug_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=8).values('project_id').distinct().count()
    sep_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=9).values('project_id').distinct().count()
    oct_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=10).values('project_id').distinct().count()
    nov_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=11).values('project_id').distinct().count()
    dec_started=farmerSoil.objects.annotate(month=ExtractMonth('updated_at')).filter(month=12).values('project_id').distinct().count()
    monthly_started_project=[jan_started,feb_started,mar_started,apr_started,may_started,jun_started,
                             jul_started,aug_started,sep_started,oct_started,nov_started,dec_started]
    
        # planed are the same as created project , so take the value from previos section

    # Fermer Performance
   
    farmers_performance=Farmer.objects.annotate(
    project_count=Count('farmerproject'),
    total_started_project=Count(
            'farmerproject__farmersoil', distinct=True
        ),
        total_progress_project=Count(
            'farmerproject__farmersowing', distinct=True
        ),
        total_completed_project=Count(
            'farmerproject__farmerpostharvesting',
            filter=Q(farmerproject__farmerpostharvesting__is_completed=True),
            distinct=True
        )
    ).values(
        'farmer_primary_id', 'user_id', 'user_name', 'project_count','total_started_project',
        'total_progress_project',
        'total_completed_project'
    ).order_by('-project_count')
    farmers_performance=farmers_performance[:6] # contain only top 6 values

    # Experts's performance
    expert_performance=ExpertFarmer.objects.annotate(
                        query_count=Count('farmerquery')
                        ).order_by('-query_count').values(
                            'name', 'expert_id', 'gender', 'experience_year','expert_photo','specialization', 'query_count'
                        )

    context={
        'task_status': task_status,
        'monthly_created_project':monthly_created_project,
        'monthly_completed_project':monthly_completed_project,
        'monthly_started_project':monthly_started_project,
        'monthly_progress_project':monthly_progress_project,
        'farmers_performance':farmers_performance,
        'expert_performance':expert_performance,
        'farmer_count': Farmer.objects.count(),
        'expert_count': ExpertFarmer.objects.count(),
        'crop_type_count': adminCrop.objects.values_list('crop_type', flat=True).distinct().count(),
        'tutorial_doc_count': adminCrop.objects.count(),
        'video_tutorial_count': expertVideo.objects.count(),
        'query_count': farmerQuery.objects.count(),
        'solution_count': farmerQuery.objects.filter(answered_at__isnull=False).count(),
        'connection_count': farmerConversation.objects.values('sender', 'receiver').distinct().count() # Assuming 100% connectivity
  
    }
    return render(request,"systemAdminIndex.html",context)

from .models import Farmer
def fermersList(request):
    farmers = Farmer.objects.all()  # Retrieve all products
    return render(request,"fermersList.html",{'farmers':farmers})


def update_farmer(request, pk): 
    try:
        farmer = Farmer.objects.filter(pk=pk).first()
    except ExpertFarmer.DoesNotExist:
        raise Http404("Farmer not found")
    flag={
            'status':""
        }
    if request.method=="POST":        
        farmer.user_name=request.POST.get('user_name')
        farmer.user_area=request.POST.get('user_area')
        farmer.user_village_city=request.POST.get('user_village_city')
        farmer.user_police_station=request.POST.get('user_police_station')
        farmer.user_district=request.POST.get('user_district')
        farmer.user_pincode=request.POST.get('user_pincode')
        farmer.user_state=request.POST.get('user_state')
        farmer.user_country=request.POST.get('user_country')
        farmer.user_dob=request.POST.get('user_dob')
        farmer.user_mobile_number=request.POST.get('user_mobile_number')
        #if photo changed then update the user_photo field otherwise don't need to update
        user_photo = request.FILES.get('user_photo') # update in two lines om 17/04/2025      
        if user_photo:
            farmer.user_photo = user_photo
        farmer.user_password=request.POST.get('user_password')
        farmer.save()
        if farmer:
            flag={
                'status':"Updated successfully"
            }
            return render(request,'farmer_update.html',flag)
    return render(request, 'farmer_update.html', {'f': farmer})

# DELETE (Remove Data)
def delete_farmer(request, pk=0):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        farmer.delete()
        return redirect('fermersList')
    return render(request, 'farmer_confirm_delete.html', {'farmer': farmer})

# add expert

from .models import ExpertFarmer
def addExpert(request):
    var={
            'status':""
         }
    if request.method == 'POST':
        expert_id = request.POST.get('expert_id')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        experience_year = request.POST.get('experience_year')
        specialization = request.POST.get('specialization')
        farm_size = request.POST.get('farm_size')
        address = request.POST.get('address')
        crops_grown = request.POST.get('crops_grown')
        soil_type = request.POST.get('soil_type')
        irrigation_system = request.POST.get('irrigation_system')
        fertilizers_used = request.POST.get('fertilizers_used')
        pest_control_methods = request.POST.get('pest_control_methods')
        equipments_owned= request.POST.get('equipments_owned')
        farming_techniques= request.POST.get('farming_techniques')
        certifications= request.POST.get('certifications')
        sustainable_practices= request.POST.get('sustainable_practices')
        technologies_used= request.POST.get('technologies_used')
        weather_adaptibility= request.POST.get('weather_adaptibility')
        goverment_subsides= request.POST.get('goverment_subsides')
        expert_photo=request.FILES('expert_photo') # changed the line in 17/04/2025
        
        # Save data to database
        expert = ExpertFarmer(
            expert_id=expert_id,
            name=name,
            dob=dob,
            gender=gender,
            mobile_number=mobile_number,
            email=email,
            experience_year=experience_year,
            specialization=specialization,
            farm_size=farm_size,
            expert_address=address,
            crops_grown=crops_grown,
            soil_type=soil_type,
            irrigation_system=irrigation_system,
            fertilizers_used=fertilizers_used,
            pest_control_methods=pest_control_methods,
            equipments_owned= equipments_owned,
            farming_techniques= farming_techniques,
            certifications= certifications,
            sustainable_practices= sustainable_practices,
            technologies_used= technologies_used,
            weather_adaptibility= weather_adaptibility,
            goverment_subsides= goverment_subsides,
            expert_photo=expert_photo
        )
        expert.save()
        if expert:
            var={
                'status':"Submitted successfully"
            }    

    return render(request,"addExpert.html",var)

def expertsList(request):
    expertFarmers = ExpertFarmer.objects.all()  # Retrieve ex
    return render(request,"expertList.html",{'expertFarmers':expertFarmers})

def update_expert(request, expert_id):
    expert = get_object_or_404(ExpertFarmer, pk=expert_id)
    flag={
            'status':""
        }
    if request.method == 'POST':
        expert.name = request.POST.get('name')
        expert.dob = request.POST.get('dob')
        expert.gender = request.POST.get('gender')
        expert.mobile_number = request.POST.get('mobile_number')
        # expert.email = request.POST.get('email')  # don't update email if unique and used as identifier
        expert.experience_year = request.POST.get('experience_year')
        expert.specialization = request.POST.get('specialization')
        expert.farm_size = request.POST.get('farm_size')
        expert.expert_address = request.POST.get('address')
        expert.crops_grown = request.POST.get('crops_grown')
        expert.soil_type = request.POST.get('soil_type')
        expert.irrigation_system = request.POST.get('irrigation_system')
        expert.fertilizers_used = request.POST.get('fertilizers_used')
        expert.pest_control_methods = request.POST.get('pest_control_methods')
        expert.equipments_owned = request.POST.get('equipments_owned')
        expert.farming_techniques = request.POST.get('farming_techniques')
        expert.certifications = request.POST.get('certifications')
        expert.sustainable_practices = request.POST.get('sustainable_practices')
        expert.technologies_used = request.POST.get('technologies_used')
        expert.weather_adaptibility = request.POST.get('weather_adaptibility')
        expert.goverment_subsides = request.POST.get('goverment_subsides')

        # Handle image update
        if 'expert_photo' in request.FILES:
            expert.expert_photo = request.FILES['expert_photo']

        expert.save()
        if expert:
            flag={
                'status':"Updated successfully"
            }
        return render(request, 'update_expert.html', flag)

    return render(request, 'update_expert.html', {'expert': expert})

def delete_expert(request, expert_id):
    expert = get_object_or_404(ExpertFarmer, pk=expert_id)
    if request.method == 'POST':
        expert.delete()
        return redirect('expertsList')
    return render(request, 'delete_expertFarmer.html', {'expert': expert})



  
def projectsFromAdmin(request):
    crops = adminCrop.objects.all()  # Retrieve ex
    return render(request,"projectsListAdmin.html",{'crops':crops})

def adminAddCrop(request):
    admins = systemAdmin.objects.all()  # Retrieve ex
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')  # This should be the ID of the admin

        # Retrieve the systemAdmin instance
        try:
            admin_instance = systemAdmin.objects.get(admin_id=admin_id)
        except systemAdmin.DoesNotExist:
            return redirect(request,"adminAddCrop")
        crop_name = request.POST['crop_name']
        admin_id = admin_instance
        crop_type = request.POST['crop_type']
        crop_duration = request.POST['crop_duration']
        crop_season = request.POST['crop_season']
        upload_date = date.today()
        crop_image = request.FILES['crop_image']
        crop_description = request.POST['crop_description']

        new_crop = adminCrop(
            crop_name=crop_name,
            admin_id=admin_id,
            crop_type=crop_type,
            crop_duration=crop_duration,
            upload_date=upload_date,
            crop_season=crop_season,
            crop_image=crop_image,
            crop_description=crop_description
        )
        new_crop.save()
        return redirect('projectsFromAdmin')  # Redirect after POST

    # This handles GET requests to show the form
    return render(request, "admin/addCrop.html",{'admins':admins})





# from .models import adminCrop
def adminEachProject(request,crop_id):
    crop = get_object_or_404(adminCrop, pk=crop_id)
    soils=adminSoil.objects.filter(crop_id=crop)
    seeds=adminSeed.objects.filter(admin_crop=crop)
    sowings=adminSowing.objects.filter(crop_id=crop)
    irrigations=adminIrrigation.objects.filter(crop_id=crop)
    fertilizers=adminFertilizer.objects.filter(crop_id=crop)
    pests=adminPest.objects.filter(crop_id=crop)
    weeds=adminWeed.objects.filter(crop_id=crop)
    diseases=adminDisease.objects.filter(crop_id=crop)
    harvestings=adminHarvesting.objects.filter(crop_id=crop)
    postHarvestings=adminPostHarvesting.objects.filter(crop_id=crop)
    return render(request,"admin/adminEachProject.html",{'crop':crop,'soils':soils,'seeds':seeds,'sowings':sowings,'irrigations':irrigations,'fertilizers':fertilizers,
                                                        'pests':pests,'weeds':weeds,'diseases':diseases,'harvestings':harvestings,'postHarvestings':postHarvestings })

def delete_adminCrop(request):

    return render(request,)

from django.shortcuts import render, redirect
from .models import adminCrop, adminSoil
def adminAddSoil(request,crop_id=None):
    crops = adminCrop.objects.all()
    # crop = get_object_or_404(adminCrop, pk=crop_id)
    if request.method == 'POST':
        selected_crop_id = request.POST.get('admin_crop')

        # Validate that crop_id is not empty
        if not selected_crop_id:
            messages.error(request, "Please select a crop.")
            return render(request, 'admin/addSoil.html', {'crops': crops,'crop_id': crop_id})

        selected_crop = adminCrop.objects.get(pk=selected_crop_id)

        soil = adminSoil(
            crop_id=selected_crop,
            soil_type=request.POST.get('soil_type'),
            nutrients=request.POST.get('nutrients'),
            structure=request.POST.get('structure'),
            water_holding_capacity=request.POST.get('water_holding_capacity'),
            drainage=request.POST.get('drainage'),
            organic_matter=request.POST.get('organic_matter'),
            soil_depth=request.POST.get('soil_depth'),
            equipments=request.POST.get('equipments'),
            description=request.POST.get('description'),
            soil_image=request.FILES['soil_image']
        )
        soil.save()
        return render(request, "admin/adminEachProject.html", {'crops': crops})

    return render(request, 'admin/addSoil.html', {'crops': crops,'crop_id':crop_id})

from .models import adminCrop, adminSeed
from django.shortcuts import render, redirect

def adminAddSeed(request,crop_id=None):
    crops = adminCrop.objects.all()

    if request.method == 'POST':
        selected_crop_id = request.POST.get('admin_crop')
        
        # Check if crop_id is valid
        if selected_crop_id:
            try:
                selected_crop = adminCrop.objects.get(pk=crop_id)

                seed = adminSeed(
                    admin_crop=selected_crop,
                    variety=request.POST.get('variety'),
                    rate_per_area=request.POST.get('rate_per_area'),
                    source=request.POST.get('source'),
                    germination_percentage=request.POST.get('germination_percentage'),
                    purity_percentage=request.POST.get('purity_percentage'),
                    moisture_content=request.POST.get('moisture_content'),
                    equipments=request.POST.get('equipments'),
                    seed_image=request.FILES.get('seed_image'),
                    description=request.POST.get('description'),
                )
                seed.save()
                seeds = adminSeed.objects.filter(admin_crop=selected_crop)
                return render(request, "admin/adminEachProject.html", {'crop':selected_crop,    'seeds': seeds})
            except adminCrop.DoesNotExist:
                # Handle the case where the crop does not exist
                return render(request, 'admin/addSeed.html', {'crops': crops, 'error': 'Selected crop does not exist.','crop_id':crop_id})
        else:
            # Handle the case where crop_id is empty
            return render(request, 'admin/addSeed.html', {'crops': crops, 'error': 'Please select a valid crop.','crop_id':crop_id})

    return render(request, 'admin/addSeed.html', {'crops': crops,'crop_id':crop_id})  # Pass the crops to the template


from .models import adminSowing, adminCrop  # Ensure adminCrop is imported

def adminAddSowing(request,crop_id=None):
    crops = adminCrop.objects.all()
    if request.method == 'POST':
        crop_id = request.POST.get('admin_crop')
        crop = adminCrop.objects.get(pk=crop_id)
        sowing = adminSowing(
            crop_id=crop,
            method=request.POST.get('method'),
            spacing=request.POST.get('spacing'),
            depth=request.POST.get('depth'),
            best_time=request.POST.get('best_time'),
            land_preparation=request.POST.get('land_preparation'),
            soil_moisture=request.POST.get('soil_moisture'),
            sowing_tools=request.POST.get('sowing_tools'),
            seed_coverage=request.POST.get('seed_coverage'),
            pre_sowing_irrigation=request.POST.get('pre_sowing_irrigation'),
            post_sowing_practice=request.POST.get('post_sowing_practice'),
            sowing_image=request.FILES['sowing_image'],
            description=request.POST.get('description'),
        )
        sowing.save()
    
        return render(request, "admin/adminEachProject.html", {'crop': crop_id}) 

    # Handle GET request
    crops = adminCrop.objects.all()  # Fetch all crops
    return render(request, 'admin/addSowing.html', {'crops': crops})  # Pass crops to the template


from .models import adminIrrigation
def adminAddIrrigation(request,crop_id=None):
    crops = adminCrop.objects.all()
    if request.method == 'POST':
        crop_id = request.POST.get('admin_crop')
        crop = adminCrop.objects.get(pk=crop_id)
        irrigation = adminIrrigation(
            crop_id=crop,
            irrigation_method=request.POST['irrigation_method'],
            variety=request.POST['variety'],
            rate_per_area=request.POST['rate_per_area'],
            source=request.POST['source'],
            irrigation_timing=request.POST['irrigation_timing'],
            water_quantity=request.POST['water_quantity'],
            water_quality=request.POST['water_quality'],
            drainage_considerations=request.POST['drainage_considerations'],
            control_system=request.POST['control_system'],
            equipment=request.POST['equipment'],
            irrigation_image=request.FILES['irrigation_image'],
            description=request.POST['description'],
        )
        irrigation.save()

        return render(request,"admin/adminEachProject.html",{'crop':crop_id}) 

    return render(request, 'admin/addIrrigation.html', {'crops': crops})

from .models import adminFertilizer
def adminAddFertilizer(request,crop_id=None):
    crops = adminCrop.objects.all()
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop')
        crop = get_object_or_404(adminCrop, pk=crop_id)
        new_fertilizer = adminFertilizer(
            crop_id=crop,
            organic_compost=request.POST['organic_compost'],
            chemical_urea=request.POST['chemical_urea'],
            chemical_dap=request.POST['chemical_dap'],
            nurient_composition=request.POST['nurient_composition'],
            application_method=request.POST['application_method'],
            application_timing=request.POST['application_timing'],
            application_frequency=request.POST['application_frequency'],
            dosage=request.POST['dosage'],
            storage=request.POST['storage'],
            equipments=request.POST['equipments'],
            fertilizer_image=request.FILES['fertilizer_image'],
            description=request.POST['description'],
        )
        new_fertilizer.save()

        return render(request,"admin/adminEachProject.html",{'crop':crop_id}) 


    return render(request, 'admin/addFertilizer.html', {'crops': crops})

from .models import adminPest
def adminAddPest(request,crop_id=None):
    crops=adminCrop.objects.all()
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop')
        crop = adminCrop.objects.get(pk=crop_id)
        pest = adminPest(
            crop_id=crop,
            pest_name=request.POST['pest_name'],
            pest_type=request.POST['pest_type'],
            pest_life_cycle=request.POST['pest_life_cycle'],
            symptoms=request.POST['symptoms'],
            affected_plant_parts=request.POST['affected_plant_parts'],
            pest_seasonality=request.POST['pest_seasonality'],
            pest_damage_level=request.POST['pest_damage_level'],
            detection_method=request.POST['detection_method'],
            control_measures=request.POST['control_measures'],
            recommended_pesticides=request.POST['recommended_pesticides'],
            resistance_risk=request.POST['resistance_risk'],
            environment_effect=request.POST['environment_effect'],
            friendly_tips=request.POST['friendly_tips'],
            equipments=request.POST['equipments'],
            pest_image=request.FILES['pest_image'],
            description=request.POST['description'],
        )
        pest.save()

        return render(request,"admin/adminEachProject.html",{'crop':crop}) 

    return render(request, 'admin/addPest.html', {'crops': crops})
        
     
from .models import adminWeed
def adminAddWeed(request,crop_id=None):
    crops=adminCrop.objects.all()       
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop')
        crop = get_object_or_404(adminCrop, pk=crop_id) 
        weed=adminWeed(
            crop_id=crop,
            weed_name=request.POST.get('weed_name'),
            weed_type=request.POST.get('weed_type'),
            growth_habit=request.POST.get('growth_habit'),
            life_cycle=request.POST.get('life_cycle'),
            time_of_appearence=request.POST.get('time_of_appearence'),
            affected_crop_growth_stage=request.POST.get('affected_crop_growth_stage'),
            area_of_infestation=request.POST.get('area_of_infestation'),
            competitive_impact_on_crop=request.POST.get('competitive_impact_on_crop'),
            leaf_shape=request.POST.get('leaf_shape'),
            leaf_color=request.POST.get('leaf_color'),
            root_structure=request.POST.get('root_structure'),
            control_measures=request.POST.get('control_measures'),
            herbicide_name=request.POST.get('herbicide_name'),
            dosage=request.POST.get('dosage'),
            application_time=request.POST.get('application_time'),
            herbicide_resistance_risk=request.POST.get('herbicide_resistance_risk'),
            weed_dispersal_method=request.POST.get('weed_dispersal_method'),
            environment_effect=request.POST.get('environment_effect'),
            equipments=request.POST.get('equipments'),
            weed_image=request.FILES.get('weed_image'),
            description=request.POST.get('description')
        )
        weed.save()

        return render(request,"admin/adminEachProject.html",{'crop':crop})  

    return render(request, 'admin/addWeed.html', {'crops': crops})


from .models import adminDisease
from django.shortcuts import get_object_or_404
def adminAddDisease(request):
    crops=adminCrop.objects.all()   
    
    if request.method == 'POST':
        crop_id = request.POST.get('admin_crop')
        if crop_id:
         crop = get_object_or_404(adminCrop, pk=crop_id)
         data = request.POST
         image = request.FILES.get('disease_image')

        adminDisease.objects.create(
            crop_id=crop,
            disease_name=data.get('disease_name'),
            causal_organism=data.get('causal_organism'),
            mode_of_transmission=data.get('mode_of_transmission'),
            symptoms=data.get('symptoms'),
            affected_plant_parts=data.get('affected_plant_parts'),
            disease_cycle=data.get('disease_cycle'),
            favorable_condition_for_disease=data.get('favorable_condition_for_disease'),
            seasonality=data.get('seasonality'),
            method_of_diagnosis=data.get('method_of_diagnosis'),
            control_measures=data.get('control_measures'),
            medicine_name=data.get('medicine_name'),
            dosage=data.get('dosage'),
            application_method=data.get('application_method'),
            impact_on_crop_quality=data.get('impact_on_crop_quality'),
            resistance_risk=data.get('resistance_risk'),
            geographic_spread=data.get('geographic_spread'),
            environment_effect_of_medicine=data.get('environment_effect_of_medicine'),
            equipments=data.get('equipments'),
            disease_image=image,
            description=data.get('description')
        )

        return render(request,"admin/adminEachProject.html",{'crop':crop}) 
    return render(request, 'admin/addDisease.html', {
        'crops': crops,
                      'error': 'Please select a crop before submitting the form.'})
            

    return render(request, 'admin/addDisease.html', {'crops': crops})                               
                                                     
                                                     


from .models import adminHarvesting
def adminAddHarvesting(request):
        
    crops = adminCrop.objects.all()
    if request.method == 'POST':
        crop_id = request.POST.get('admin_crop')
        crop = get_object_or_404(adminCrop, pk=crop_id)
        harvesting = adminHarvesting(
            crop_id=crop,
            time=request.POST['time'],
            drying=request.POST['drying'],
            storage=request.POST['storage'],
            optimal_harvesting_period=request.POST['optimal_harvesting_period'],
            method_of_harvesting=request.POST['method_of_harvesting'],
            equipments=request.POST['equipments'],
            labor_requirement=request.POST['labor_requirement'],
            yield_quantity=request.POST['yield_quantity'],
            moisture_content=request.POST['moisture_content'],
            post_harvesting_handling=request.POST['post_harvesting_handling'],
            transportation_requirement=request.POST['transportation_requirement'],
            challenges=request.POST['challenges'],
            crop_loss_percentage=request.POST['crop_loss_percentage'],
            market_readiness=request.POST['market_readiness'],
            safty_practice=request.POST['safty_practice'],
            harvesting_image=request.FILES['harvesting_image'],
            description=request.POST['description']
        )
        harvesting.save()
        return render(request,"admin/adminEachProject.html",{'crop':crop})  

    return render(request, 'admin/addHarvesting.html', {'crops': crops})


from .models import adminPostHarvesting, adminCrop
from django.shortcuts import render

def adminAddPostHarvesting(request,crop_id=None):
    crops = adminCrop.objects.all()  # Get all crops for the form

    if request.method == 'POST':
        crop_id = request.POST.get('admin_crop')
        try:
            crop = adminCrop.objects.get(pk=crop_id)

            post = adminPostHarvesting(
                crop_id=crop,
                cleaning=request.POST.get('cleaning'),
                sorting=request.POST.get('sorting'),
                drying=request.POST.get('drying'),
                curing=request.POST.get('curing'),
                packaging=request.POST.get('packaging'),
                storage=request.POST.get('storage'),
                waste_management=request.POST.get('waste_management'),
                market_preparation=request.POST.get('market_preparation'),
                equipments=request.POST.get('equipments'),
                post_harvesting_image=request.FILES['post_harvesting_image'],
                description=request.POST.get('description')
            )
            post.save()

            return render(request, "admin/adminEachProject.html", {'crop': crop})
        except adminCrop.DoesNotExist:
            return render(request, 'admin/addPostHarvesting.html', {
                'crops': crops,
                'error': 'Selected crop does not exist.'
            })

    return render(request, 'admin/addPostHarvesting.html', {'crops': crops})

from .models import adminOthers
def adminAddOthers(request,crop_id=None):
    crops=adminCrop.objects.all()
    
    if request.method == 'POST':
            
        crop_id=crop,
        crop_id = request.POST.get('admin_crop')
        crop = adminCrop.objects.get(pk=crop_id)
        property_name=request.POST.get('property_name')
        
        post_harvesting_image=request.FILES['post_harvesting_image'],
        description=request.POST.get('description')
        others=others(
            crop_id=crop_id,
            property_name=property_name,
            post_harvesting_image=post_harvesting_image,
            description=description
        )
        others.save()

        return render(request,"admin/adminEachProject.html",{'crop':crop}) 

    return render(request, 'admin/addOthers.html', {'crops': crops})

def queryForAdmin(request):

    return render(request,"queryForAdmin.html")

def adminProflie(request):

    return render(request,"adminProflie.html")

def adminLogout(request):

    return render(request,"adminLogout.html")




#expert view design


#create on 18/04/2025
def expertLogin(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        expert = ExpertFarmer.objects.filter(
        email=email,
        mobile_number=mobile,
        name=name
        ).first()

        if expert:
            expert_id = expert.expert_id
            # Success, expert found!
            # You can now set it in session or redirect
            request.session['expert_id'] = expert_id
            return redirect('expert')
        else:
            # Expert not found
            return render(request, 'expert/login.html', {'error': 'Invalid login details.'})
        
    return render(request,"expert/login.html")

# created on 17/04/2025
def  expert(request):
    if not request.session.get('expert_id'):
        return redirect('expertLogin')
    else:
        expert_id=request.session.get('expert_id');
        expert=ExpertFarmer.objects.filter(pk=expert_id).first()
    return render(request,"expert/index.html",{'expert':expert})

def expertLogout(request):
    if 'expert_id' in request.session:
        del request.session['expert_id']
    return redirect("expertLogin") 

    

#add on 19/04/2025
def expertVideoView(request):
    expert_id=request.session.get('expert_id')
    videos=expertVideo.objects.filter(expert_id=expert_id)

    return render(request,"expert/video.html",{'videos':videos});

#add on 19/04/2025

from .models import expertVideo
def expertAddVideo(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        duration = request.POST.get('duration')
        category = request.POST.get('category')
        # takes expert id from session variable
        expert_id=request.session.get('expert_id')
        expert=ExpertFarmer.objects.filter(pk=expert_id).first()

        new_video = expertVideo(
            title=title,
            expert_id=expert,
            description=description,
            video_file=video_file,
            thumbnail=thumbnail,
            duration=duration,
            category=category,
            views=0  # default
        )
        new_video.save()
        return redirect("expertVideoView");  # or redirect to success page

    return render(request,"expert/addVideo.html")


#add on 20/04/2025
def expertPlayVideo(request,video_id):
    video=expertVideo.objects.filter(video_id=video_id).first()
    # video_link=video.video_file.url
    return render(request,"expert/playVideo.html",{'video':video})

#created on 20/04/2025
def expertVideoUpdate(request,video_id):    
    video = expertVideo.objects.filter(pk=video_id).first()
    

    return render(request,"expert/videoUpdate.html",{'video':video})

#after updating the record
def expertVideoUpdated(request):

    if request.method == 'POST':
        video_id=request.POST.get('video_id')
        video = expertVideo.objects.filter(pk=video_id).first()

        video.title = request.POST.get('title')
        video.description = request.POST.get('description')
        if request.FILES.get('video_file'):         
            video.video_file = request.FILES.get('video_file')
        if request.FILES.get('thumbnail'):
            video.thumbnail = request.FILES.get('thumbnail')
        video.duration = request.POST.get('duration')
        video.category = request.POST.get('category')      
        video.save()
        return redirect("expertVideoView");  
    return redirect("expertVideoView")

# created pm 24/04/2025
def getAdvise(request):
    projects = farmerProject.objects.filter(complete=False)

    # Annotate each project with current stage label (dummy for now)
    for project in projects:
        context = {}
        if farmerSoil.objects.filter(project=project,is_completed=False, expert_advise__isnull=True).exists():
            project.current_stage = "Soil Preparation"
            # Replace this with logic
        elif farmerSowing.objects.filter(project=project,is_completed=False,expert_advise='').exists():
            project.current_stage = "Sow Seeds"

        elif farmerGrowthStage.objects.filter(project=project, is_completed=False, expert_advise__isnull=True).exists():
            project.current_stage = "Growth"

        elif farmerHarvesting.objects.filter(project=project, is_completed=False, expert_advise__isnull=True).exists():
            project.current_stage = "Harvesting"

        elif farmerPostHarvesting.objects.filter(project=project, is_completed=False, expert_advise__isnull=True).exists():
            project.current_stage = "Post Harvesting"

        else:
            project.current_stage = "Planned"
        
        context={
            'projects':projects
        }
    return render(request, "expert/getAdvise.html",context)

# created on 19/05/2025
from django.shortcuts import render, get_object_or_404
from .models import (
    farmerProject, Farmer, farmerSoil, farmerSowing, farmerIrrigation, farmerFertilizer,
    farmerWeed, farmerPest, farmerDisease, farmerGrowthStage, farmerHarvesting,
    farmerPostHarvesting, farmerOthers
)
from django.utils import timezone

def giveAdvise(request, project_id):
    project = get_object_or_404(farmerProject, pk=project_id)
    farmer = project.farmer_primary_id

    # stages with is_completed field
    stages_with_completion = [
        ("Soil Preparation", farmerSoil),
        ("Sowing", farmerSowing),
        # ("Irrigation", farmerIrrigation),
        # ("Fertilizer", farmerFertilizer),
        # ("Weed Management", farmerWeed),
        # ("Pest Management", farmerPest),
        # ("Disease Management", farmerDisease),
        ("Growth Monitoring", farmerGrowthStage),
        ("Harvesting", farmerHarvesting),
        ("Post-Harvesting", farmerPostHarvesting),
    ]

    # stage without is_completed (handle differently)
    other_stage = ("Others", farmerOthers)

    completed = []
    next_stage = None

    for name, model in stages_with_completion:
        if model.objects.filter(project=project, is_completed=True).exists():
            completed.append(name)
        elif next_stage is None:
            next_stage = name

    # handle 'Others' if all other stages completed
    if next_stage is None:
        next_stage = other_stage[0]
        if other_stage[1].objects.filter(project=project).exists():
            completed.append(next_stage)
            next_stage = None  # all done

    if request.method == 'POST' and next_stage:
        suggestion = request.POST.get("expert_suggestion")

        stage_model = dict(stages_with_completion + [other_stage])[next_stage]
        obj = stage_model.objects.filter(project=project).first()

        if obj:
            obj.expert_advise = suggestion
            obj.save()
        else:
            # Create with required defaults
            kwargs = {
                "project": project,
                "expert_advise": suggestion,
                "created_at": timezone.now().date(),
                "updated_at": timezone.now().date()
            }
            if hasattr(stage_model, 'is_completed'):
                kwargs['is_completed'] = False
            stage_model.objects.create(**kwargs)

        return render(request, "expert/giveAdvise.html", {
            "project": project,
            "farmer": farmer,
            "completed": completed,
            "next_stage": next_stage,
            "success": True,
            "obj":obj
        })

    return render(request, "expert/giveAdvise.html", {
        "project": project,
        "farmer": farmer,
        "completed": completed,
        "next_stage": next_stage
    })



# created pm 24/04/2025
def answerQuestion(request):


    queries = farmerQuery.objects.filter(status='pending').order_by('submitted_at')
    return render(request,"expert/answerQuestion.html",{'queries':queries})

from django.http import JsonResponse
def submitAnswer(request):
    if request.method == "POST":
        query_id = request.POST.get("question_id")
        answer_text = request.POST.get("answer")

        try:
            query = farmerQuery.objects.get(query_id=query_id)
            query.solution_text = answer_text
            query.status = 'answered'
            query.answered_at = datetime.now()

            # If solution image is uploaded
            if 'solution_image' in request.FILES:
                query.solution_image = request.FILES['solution_image']

            query.save()
            return redirect(expert)
        except farmerQuery.DoesNotExist:
            return redirect(expert)
        
    return redirect(expert)

def managementTeam(request):

    return render(request, 'managementTeam.html')



# // functions for AI chat bot 
from django.http import JsonResponse
from .models import adminCrop, farmerProject

def get_crop_info(request):
    crop_name = request.GET.get('crop_name')
    crop = adminCrop.objects.filter(crop_name__iexact=crop_name).first()
    if crop:
        return JsonResponse({
            'description': crop.description,
            'soil': crop.soil_type,
            # add other stages
        })
    return JsonResponse({'error': 'Crop not found'}, status=404)
# views.py
import json
from django.http import JsonResponse
from .models import adminCrop, farmerProject

# def dialogflow_webhook(request):
#     data = json.loads(request.body)
#     intent = data['queryResult']['intent']['displayName']
#     parameters = data['queryResult']['parameters']

#     if intent == 'GetCropDetails':
#         crop_name = parameters.get('crop')
#         crop = adminCrop.objects.filter(crop_name__iexact=crop_name).first()
#         if crop:
#             msg = f"{crop.crop_name} details:\nSoil: {crop.soil_type},\nSowing: {crop.sowing_method},\nIrrigation: {crop.irrigation_type},\nHarvest: {crop.harvest_time}"
#         else:
#             msg = "Sorry, I couldn't find details for that crop."

#     elif intent == 'CheckProjectStatus':
#         crop_name = parameters.get('crop')
#         project = farmerProject.objects.filter(crop_name__iexact=crop_name).first()
#         if project:
#             msg = f"Your {crop_name} project is at stage {project.current_stage}, {project.completion_percentage}% completed."
#         else:
#             msg = f"No project found for {crop_name}."

#     elif intent == 'AddProject':
#         crop_name = parameters.get('crop')
#         # You may use request.user if authentication is applied
#         farmerProject.objects.create(crop_name=crop_name, current_stage='Soil', completion_percentage=0)
#         msg = f"Project for {crop_name} has been added."

#     elif intent == 'AskExpert':
#         crop_name = parameters.get('crop')
#         msg = f"Your question about {crop_name} has been forwarded to the expert. They will get back to you soon."

#     else:
#         msg = "I didn't understand that. Try asking about crop info, project status, or expert advice."

#     return JsonResponse({
#         "fulfillmentText": msg
#     })

def dialogflow_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        intent = data.get('queryResult', {}).get('intent', {}).get('displayName')

        # Check if the intent is GetCropCount
        if intent == "GetCropCount":
            crop_count = adminCrop.objects.count()
            response_text = f"I can provide details for {crop_count} different crops."
        else:
            response_text = "Sorry, I didn't understand that. Can you rephrase?"

        return JsonResponse({
            "fulfillmentText": response_text
        })

    return JsonResponse({"fulfillmentText": "Invalid request method."})

def aiChatBot(request):
   
    return render(request,'aiChatBot.html')







