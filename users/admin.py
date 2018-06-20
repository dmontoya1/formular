# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as django_user_admin
from django.contrib.auth.forms import UserChangeForm as django_change_form
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import User, Company


class UserChangeForm(django_change_form):
    class Meta(django_change_form.Meta):
        model = User


class UserAdmin(django_user_admin):
    """Administrador de Usuarios
    """

    form = UserChangeForm
    model = User
    icon = '<i class="material-icons">wc</i>'
    search_fields = (
        'first_name', 'last_name', 'email', 'cellphone',
        'document_id'
    )
    list_display = (
        'username', 'email', 'user_type', 'first_name', 'last_name',
    )

    fieldsets = (
        (None,
         {'fields':
          ('user_type', 'username', 'password')}),
        (_('Información Personal'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Persmisos'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups')}),
        (_('Información Adicional'),
         {'fields': ('document_type', 'document_id', 'cellphone',)})
    )

    def get_queryset(self, request):
        """
        Función para reemplazar el queryset por defecto de django.
        """
        query = super(UserAdmin, self).get_queryset(request)
        return query.all().exclude(is_superuser=True)


class CompanyAdmin(admin.ModelAdmin):
    """Clase para la administración de las compañías
    """

    model = Company
    icon = '<i class="material-icons">beenhere</i>'
    search_fields = (
        'name', 'nit'
    )
    list_display = (
        'name', 'nit', 'email', 'contact_person_name'
    )


admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
