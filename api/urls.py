# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views

app_name = 'api'
urlpatterns = [
    path('', include('webclient.urls'), name='webclient'),
    path('api-key/', views.ApiKeyDetailView.as_view(), name='api-key'),
    path('gathering/', include('gathering.urls', namespace="api-gathering")),
    path('users/', include('users.urls', namespace="api-users")),
]