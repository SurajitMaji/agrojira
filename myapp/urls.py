from django.urls import path
from .views import fertilizer_tool_view
from .views import crop_recommendation_view
from .views import pesticide_recommendation_view
urlpatterns = [
    path('fertilizer-tool/', fertilizer_tool_view, name='fertilizer_tool'),
    path('crop-recommendation/', crop_recommendation_view, name='crop_recommendation'),
    path('pesticide-tool/', pesticide_recommendation_view, name='pesticide_tool'),
]
