# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template import loader
from django.shortcuts import render, get_object_or_404, reverse

from .models import UserToken
from .serializers import UserSerializer


class PasswordResetView(APIView):
    """Api para olvidó su contraseña de un usuario
    """

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    queryset = UserToken.objects.all()

    def get_object(self):
        email = self.request.data.get('email')
        user = get_object_or_404(get_user_model(), email=email)
        try:
            obj = UserToken.objects.get(user=user)
        except:
            obj = UserToken.objects.create(user=user)
        return obj

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        token = uuid.uuid1().hex
        user.password_activation_token = token
        user.is_use_token = False
        user.save()
        url = 'http://{}{}?token={}'.format(request.get_host(), reverse('webclient:recover_password'), token)
        ctx = {
            "title": "Recuperar contraseña",
            "content": "Hola! Solicitaste recuperar tu contraseña . Para cambiarla has click en el siguiente botón",
            "url": url,
            "action": "Recuperar"
        }
        body = loader.get_template('emails/email.html').render(ctx)
        message = EmailMessage('Cambio de contraseña', body, settings.EMAIL_USER, [user.user.email])
        message.content_subtype = 'html'
        message.send()
        return Response(
            {
                "detail":"Se ha enviado un correo para restablecer su contraseña"
            },
            status=status.HTTP_200_OK
		)
