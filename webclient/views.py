# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.shortcuts import render, reverse
from django.views.generic import TemplateView, View, ListView


class HomePageView(TemplateView):
    template_name = 'home/home.html'


class StartGathering(TemplateView):

    template_name = 'gathering/start_gathering.html'


class GatheringForm(TemplateView):

    template_name = 'gathering/gathering_form.html'


class LoginView(View):
    """Iniciar Sesión 
    """

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            url = reverse('webclient:start-gathering')
            login(request, user)
        else:
            response = {'error': 'Correo y/o contraseña incorrectas.'}
            return JsonResponse(response, status=400)

        return JsonResponse(url, safe=False)
