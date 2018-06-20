from django.urls import path, include
from .views import (
    HomePageView,
    StartGathering,
    GatheringForm
)

app_name = 'webclient'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('start-gathering/', StartGathering.as_view(), name="start-gathering"),
    path('gathering-form/', GatheringForm.as_view(), name="gathering-form"),
]
