from django.contrib import admin
from home.models import Farmer,ExpertFarmer,farmerProject,farmerConversation,farmerQuery

# Register your models here.
#user site
admin.site.register(Farmer)
admin.site.register(farmerProject)
admin.site.register(farmerConversation)
admin.site.register(farmerQuery)

# register the models for farmer project's action
from home.models import farmerSoil,farmerSowing,farmerIrrigation,farmerFertilizer,farmerWeed,farmerPest,farmerDisease,farmerGrowthStage,farmerHarvesting,farmerPostHarvesting,farmerOthers

admin.site.register(farmerSoil)
admin.site.register(farmerSowing)
admin.site.register(farmerIrrigation)
admin.site.register(farmerFertilizer)
admin.site.register(farmerWeed)
admin.site.register(farmerPest)
admin.site.register(farmerDisease)
admin.site.register(farmerGrowthStage)
admin.site.register(farmerHarvesting)
admin.site.register(farmerPostHarvesting)
admin.site.register(farmerOthers)

#admin site
admin.site.register(ExpertFarmer)
from home.models import systemAdmin,adminCrop,adminSoil,adminSeed,adminSowing
from home.models import adminIrrigation,adminFertilizer,adminPest,adminWeed,adminSowing,adminDisease
from home.models import adminHarvesting,adminPostHarvesting,adminOthers

admin.site.register(systemAdmin)
admin.site.register(adminCrop)
admin.site.register(adminSoil)
admin.site.register(adminSeed)
admin.site.register(adminSowing)
admin.site.register(adminIrrigation)
admin.site.register(adminFertilizer)
admin.site.register(adminPest)
admin.site.register(adminWeed)
admin.site.register(adminDisease)
admin.site.register(adminHarvesting)
admin.site.register(adminPostHarvesting)
admin.site.register(adminOthers)


#expert site
from home.models import expertVideo
#models for expert
admin.site.register(expertVideo)

