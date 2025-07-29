"""
URL configuration for agriculture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home import views
admin.site.site_header=""
admin.site.site_site_title=""
admin.site.index_title="Welcome to project of Surajit, Sreyashree and Mamoni"

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #user/fermer urls
    path('',views.index,name='home'),
    path('registration',views.registration,name='registration'),
    path('video',views.video,name='video'),
    path('playingRecordedVideo/<int:video_id>/',views.playingRecordedVideo,name='playingRecordedVideo'),
    path('category',views.category,name='category'),
    path('everyCropProcess/<int:crop_id>/',views.everyCropProcess,name='everyCropProcess'),
    path('about',views.about,name='about'), # add on 17/04/2025 by surajit
    path('expertForUser',views.expertForUser,name='expertForUser'), # add on 18/04/2025 by surajit
    path('login',views.login,name='login'),    # add on 18/04/2025 by surajit    
    path('community',views.community,name='community'), # add on 23/04/2025 by surajit
    path('eachMessage/<int:receiver_id>/',views.eachMessage,name='eachMessage'), # add on 23/04/2025 by surajit
    path('profile',views.profile,name='profile'), # add on 19/04/2025 by surajit
    path('logoutUser',views.logoutUser,name='logoutUser'), # add on 19/04/2025 by surajit
    path('addUserProject',views.addProject,name='addProject'), # add on 20/04/2025 by surajit
    path('ongoingProject/<int:project_id>/',views.ongoingProject,name='ongoingProject'), # add on 21/04/2025 by surajit
    path('userQuery',views.userQuery,name='userQuery'), # add on 25/04/2025 by surajit
    path('addQuery',views.addQuery,name='addQuery'), # add on 25/04/2025 by surajit
    
    # farmer project operation urls created on 06/05/2025

    path('ongoingProjectSoil/<int:project_id>/',views.ongoingProjectSoil,name='ongoingProjectSoil'),
    path('submit_farmerSoil',views.submit_farmerSoil,name='submit_farmerSoil'), # add on 09/05/2025 by surajit 
    path('ongoingProjectSoilUpdate/<int:project_id>/<int:farmer_soil_id>/',views.ongoingProjectSoilUpdate,name='ongoingProjectSoilUpdate'),
    path('ongoingProjectSowing/<int:project_id>/',views.ongoingProjectSowing,name='ongoingProjectSowing'),
    path('submit_farmerSowing',views.submit_farmerSowing,name='submit_farmerSowing'), # add on 15/05/2025 by surajit 
    path('ongoingProjectIrrigation/<int:project_id>/',views.ongoingProjectIrrigation,name='ongoingProjectIrrigation'),
    path('submit_farmerIrrigation',views.submit_farmerIrrigation,name='submit_farmerIrrigation'), # add on 15/05/2025 by surajit 
    path('ongoingProjectFertilizer/<int:project_id>/',views.ongoingProjectFertilizer,name='ongoingProjectFertilizer'),
    path('submit_farmerFertilizer',views.submit_farmerFertilizer,name='submit_farmerFertilizer'), # add on 15/05/2025 by surajit 
    path('ongoingProjectWeed/<int:project_id>/',views.ongoingProjectWeed,name='ongoingProjectWeed'),
    path('submit_farmerWeed',views.submit_farmerWeed,name='submit_farmerWeed'), # add on 15/05/2025 by surajit 
    path('ongoingProjectPest/<int:project_id>/',views.ongoingProjectPest,name='ongoingProjectPest'),
    path('submit_farmerPest',views.submit_farmerPest,name='submit_farmerPest'), # add on 15/05/2025 by surajit 
    path('ongoingProjectDisease/<int:project_id>/',views.ongoingProjectDisease,name='ongoingProjectDisease'),
    path('submit_farmerDisease',views.submit_farmerDisease,name='submit_farmerDisease'), # add on 09/05/2025 by surajit 
    path('ongoingProjectGrowth/<int:project_id>/',views.ongoingProjectGrowth,name='ongoingProjectGrowth'),
    path('submit_farmerGrowth',views.submit_farmerGrowth,name='submit_farmerGrowth'), # add on 15/05/2025 by surajit 
    path('ongoingProjectHarvesting/<int:project_id>/',views.ongoingProjectHarvesting,name='ongoingProjectHarvesting'),
    path('submit_farmerHarvesting',views.submit_farmerHarvesting,name='submit_farmerHarvesting'), # add on 15/05/2025 by surajit 
    path('ongoingProjectPostHarvesting/<int:project_id>/',views.ongoingProjectPostHarvesting,name='ongoingProjectPostHarvesting'),
    path('submit_farmerPostHarvesting',views.submit_farmerPostHarvesting,name='submit_farmerPostHarvesting'), # add on 15/05/2025 by surajit 
    path('ongoingProjectOthers/<int:project_id>/',views.ongoingProjectOthers,name='ongoingProjectOthers'),
    path('submit_farmerOthers',views.submit_farmerOthers,name='submit_farmerOthers'), # add on 15/05/2025 by surajit 
    path('search/', views.search_results, name='search_results'), # add on 26/05/2025 by surajit 


    # admin urls
    path('adminHome',views.adminHome,name='adminHome'),
    path('fermersList',views.fermersList,name='fermersList'),
    path('update/<int:pk>/', views.update_farmer, name='update_farmer'),
    path('delete/<int:pk>/', views.delete_farmer, name='delete_farmer'),
    path('expertsList', views.expertsList, name='expertsList'),
    path('addExpert', views.addExpert, name='addExpert'),
    path('update_expert/<int:expert_id>/', views.update_expert, name='update_expert'),
    path('delete_expert/<int:expert_id>/', views.delete_expert, name='delete_expert'),  
    path('projectsFromAdmin', views.projectsFromAdmin, name='projectsFromAdmin'), 
    path('adminEachProject/<int:crop_id>/', views.adminEachProject, name='adminEachProject'), 
    path('delete_adminCrop/<int:crop_id>/', views.delete_adminCrop, name='delete_adminCrop'),


    # crop deatails 

    path('adminAddCrop', views.adminAddCrop, name='adminAddCrop'), 
    path('adminAddSeed/<int:crop_id>/', views.adminAddSeed, name='adminAddSeed'),
    path('adminAddSeed/', views.adminAddSeed, name='adminAddSeed'),
    path('adminAddSoil/<int:crop_id>/', views.adminAddSoil, name='adminAddSoil'),
    path('adminAddSoil/', views.adminAddSoil, name='adminAddSoil'),  # default/fallback route
    path('adminAddSeed', views.adminAddSeed, name='adminAddSeed'), 
    path('adminAddSowing', views.adminAddSowing, name='adminAddSowing'), 
    path('adminAddIrrigation', views.adminAddIrrigation, name='adminAddIrrigation'), 
    path('adminAddFertilizer/<int:crop_id>/', views.adminAddFertilizer, name='adminAddFertilizer'), 
    path('adminAddFertilizer', views.adminAddFertilizer, name='adminAddFertilizer'), 
    path('adminAddPest', views.adminAddPest, name='adminAddPest'), 
    path('adminAddWeed', views.adminAddWeed, name='adminAddWeed'), 
    path('adminAddDisease', views.adminAddDisease, name='adminAddDisease'),
    path('adminAddDisease/<int:crop_id>/', views.adminAddDisease, name='adminAddDisease'), 
    path('adminAddHarvesting', views.adminAddHarvesting, name='adminAddHarvesting'), 
    path('adminAddHarvesting/<int:crop_id>/', views.adminAddHarvesting, name='adminAddHarvesting'), 
    path('adminAddPostHarvesting/<int:crop_id>/', views.adminAddPostHarvesting, name='adminAddPostHarvesting'),
    path('adminAddPostHarvesting/', views.adminAddPostHarvesting, name='adminAddPostHarvesting'),
    path('adminAddOthers', views.adminAddOthers, name='adminAddOthers'),


    path('queryForAdmin', views.queryForAdmin, name='queryForAdmin'), 
    path('adminProflie', views.adminProflie, name='adminProflie'),
    path('adminLogout', views.adminLogout, name='adminLogout'),



    #expert 
    path('expert', views.expert, name='expert'),
    path('expertLogin', views.expertLogin, name='expertLogin'),
    path('expertVideoView', views.expertVideoView, name='expertVideoView'),
    path('expert/addVideo', views.expertAddVideo, name='expertAddVideo'),
    path('expertLogout', views.expertLogout, name='expertLogout'),
    path('expertPlayVideo/<int:video_id>/', views.expertPlayVideo, name='expertPlayVideo'),
    path('expertVideoUpdate/<int:video_id>/', views.expertVideoUpdate, name='expertVideoUpdate'),
    path('expertVideoUpdated', views.expertVideoUpdated, name='expertVideoUpdated'),
    path('getAdvise', views.getAdvise, name='getAdvise'),
    path('expert/giveAdvise/<int:project_id>/', views.giveAdvise, name='giveAdvise'),
    # path('expert/submit_expert_advice', views.submit_expert_advice, name='submit_expert_advice'), # add on 22/05/25
    path('answerQuestion', views.answerQuestion, name='answerQuestion'),
    path('submitAnswer', views.submitAnswer, name='submitAnswer'), # add on 24/05/25




    # management team
    path('managementTeam', views.managementTeam, name='managementTeam'), # add on 24/05/25

    # chat bot 
    path('aiChatBot', views.aiChatBot, name='aiChatBot'),
    path('dialogflow-webhook/', views.dialogflow_webhook, name='dialogflow_webhook')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

