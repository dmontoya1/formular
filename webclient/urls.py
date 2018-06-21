from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


app_name = 'webclient'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('start-gathering/', views.StartGathering.as_view(), name="start-gathering"),
    path('gathering-form/', views.GatheringForm.as_view(), name="gathering-form"),
    path('form-history/', views.FormHistory.as_view(), name="form-history"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    path('recover-password/', views.ResetPasswordView.as_view(), name='recover_password'),
]
