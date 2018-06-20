# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

app_name = 'api'
urlpatterns = [
    url(r'^api-key/', views.ApiKeyDetailView.as_view(), name='api-key'),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^manager/', include('manager.urls', namespace="api-manager")),
    url(r'^pathologies_tracking/', include('pathologies_tracking.urls', namespace="api-pathologies_tracking")),
    url(r'^users/', include('users.urls')),
]