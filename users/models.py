# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Guarda los datos de los usuarios de la plataforma
    """

    CEDULA_CIUDADANIA = 'CC'
    CEDULA_EXTRANJERA = 'CE'
    PASAPORTE = 'PP'
    TARJETA_IDENTIDAD = 'TI'
    DOCUMENTO_EXTRANJERO = "DE"
    NIT = 'NT'
    COMERCIANTE = 'CO'
    ADMINISTRADOR = 'AD'
    DOCUMENT_TYPE = (
        (CEDULA_CIUDADANIA, 'Cédula de ciudadania'),
        (CEDULA_EXTRANJERA, 'Cédula de extranjería'),
        (PASAPORTE, 'Pasaporte'),
        (TARJETA_IDENTIDAD, 'Tarjeta de identidad'),
        (DOCUMENTO_EXTRANJERO, 'Documento de id. extranjero'),
        (NIT, 'Nit'),
    )
    USER_TYPE = (
        (COMERCIANTE, 'Comerciante'),
        (ADMINISTRADOR, 'Administrador')
    )

    password = models.CharField("Password", max_length=128, blank=True, null=True)
    document_type = models.CharField("Tipo Documento", max_length=2, choices=DOCUMENT_TYPE,
                                     blank=True, null=True)
    document_id = models.CharField("Número Documento", max_length=15, unique=True,
                                   blank=True, null=True)
    user_type = models.CharField("Tipo Usuario", max_length=2, choices=USER_TYPE)
    cellphone = models.CharField("Celular", max_length=10, blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Company(models.Model):
    """Guarda los datos de la companía
    """

    name = models.CharField("Nombre", max_length=255)
    nit = models.CharField("NIT", max_length=12)
    email = models.EmailField("Email", max_length=254)
    phone_number = models.CharField("Número telefónico", max_length=10)
    address = models.CharField("Dirección", max_length=255)
    contact_person_name = models.CharField("Nombre persona de contacto", max_length=255)
    contact_person_email = models.EmailField("Email persona de contacto", max_length=255)
    contact_person_charge = models.CharField("Cargo persona de contacto", max_length=255)
    contact_person_phone = models.CharField("Número telefónico persona de contacto", max_length=10)
    website = models.URLField("Sitio Web", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Companía"
        verbose_name_plural = "Compañías"
