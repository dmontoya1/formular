# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
	"""Serializador para el model de Usuario
	"""

	email = serializers.EmailField(validators=[
		UniqueValidator(
			queryset=get_user_model().objects.all(),
			message="Ya existe un usuario con este email",
		)]
	)

	class Meta:
		model = get_user_model()
		fields = ('email', 'username')

	
	def update(self, instance, validated_data):
		instance.email = validated_data['email']
		instance.username = validated_data['email']
		instance.save()
		return instance
