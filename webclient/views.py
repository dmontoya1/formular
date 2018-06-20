# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView


class HomePageView(TemplateView):
    template_name = 'home/home.html'


class StartGathering(TemplateView):

    template_name = 'gathering/start_gathering.html'


class GatheringForm(TemplateView):

    template_name = 'gathering/gathering_form.html'