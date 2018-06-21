# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
	path('reset-password/', views.PasswordResetView.as_view(), name='reset_password'),
	path('companies/', views.CompaniesListCreate.as_view(), name='company'),
]