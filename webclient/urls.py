from django.urls import path, include
from .views import (
    HomePageView
)

app_name = 'webclient'
urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]
