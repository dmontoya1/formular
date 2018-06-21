# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

def processor(request):

    context = {
                'Api_Key': settings.API_KEY,
              }
    return context
