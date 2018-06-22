# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from users.models import User, Company
from .models import Category, Question, QuestionChoice, Form, Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administración de las Categorías
    """

    model = Category
    icon = '<i class="material-icons">dns</i>'
    search_fields = (
        'name',
    )
    list_display = (
        'name', 'is_active'
    )


class QuestionChoiceAdmin(admin.StackedInline):
    """Administración de los Items de las preguntas de selección múltiple
    """

    model = QuestionChoice
    extra = 0
    fk_name = "question"
    fieldsets = (
        (None, {
            'fields': (
                'value', 'weight', 'dependant_question', 'id'
            ),
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Administración de Preguntas
    """

    model = Question
    icon = '<i class="material-icons">assignment</i>'
    inlines = [QuestionChoiceAdmin]
    search_fields = (
        'category__name', 'context', 'question_type', 'weight'
    )
    list_display = (
        'context', 'category', 'question_type', 'weight', 'is_active',
    )
    list_filter = ('question_type', 'category__name',)

    class Media:
        js = ('assets/js/admin/question_admin.js',)



class AnswerAdmin(admin.TabularInline):
    """Administración de Respuestas de los pacientes al formulario
    """

    model = Answer
    extra = 0

    can_delete = False

    def has_add_permission(self, request):
        return False
    
    fieldsets = (
        (None, {
            'fields': (
                'question', 'value',
            ),
        }),
    )
    
    readonly_fields = ('question', 'value',)



@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """Administración de formularios de los pacientes
    """

    class Media:
        js = ('assets/js/admin/forms_admin.js',)


    model = Form
    icon = '<i class="material-icons">assignment</i>'
    inlines = [AnswerAdmin,]
    search_fields = (
        'date', 'user__first_name', 'user__last_name',
    )
    list_display = (
        'date', 'user', 'company',
    )


    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        return True
