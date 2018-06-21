# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from users.models import User, Company


class Category(models.Model):
    """Guarda las categorías de las preguntas del formulario
    """

    name = models.CharField("Nombre Categoría", max_length=255, unique=True)
    is_active = models.BooleanField("Es activo?", default=True)
    weight = models.IntegerField("Peso de la Categoría", default=0)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return "%s" % (self.name)


class Question(models.Model):
    """Guarda las preguntas separadas por categoria del formulario
    """

    TEXTO_ABIERTO = 'TA'
    SELECCION = 'SE'
    FECHA = 'FE'
    BOOLEANO = 'BO'
    QUESTION_TYPE = (
        (TEXTO_ABIERTO, 'Texto Abierto'),
        (SELECCION, 'Selección Multiple, única respuesta'),
        (FECHA, 'Fecha'),
        (BOOLEANO, 'Booleano'),
    )

    category = models.ForeignKey(
        Category,
        verbose_name="Categoría",
        related_name="related_questions",
        on_delete=models.CASCADE,
        blank=True, null=True)
    context = models.TextField(verbose_name="Pregunta",
                               help_text='Escribe la pregunta del formulario')
    question_type = models.CharField("Tipo de Pregunta", max_length=2, choices=QUESTION_TYPE)
    weight = models.IntegerField("Peso de la pregunta", default=0)
    is_active = models.BooleanField("Pregunta Activa?", default=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return "%s" % (self.context)


class QuestionChoice(models.Model):
    """Opciones de cada pregunta cuando es de selección multiple con única respuesta
    """

    question = models.ForeignKey(Question, verbose_name="Pregunta",
                                 on_delete=models.CASCADE,
                                 related_name="related_question_choices")
    value = models.CharField("Valor", max_length=255)
    weight = models.IntegerField(verbose_name="Peso de la opción de la pregunta")
    dependant_question = models.ManyToManyField(Question, verbose_name="Depende de otra pregunta?",
                                                related_name="related_dependant_questions",
                                                blank=True)

    class Meta:
        verbose_name = "Opcion de la Pregunta"
        verbose_name_plural = "Opciones de Pregunta"

    def __str__(self):
        return "%s" % (self.value)


class Form(models.Model):
    """Guarda el formulario de cada compañia
    """

    date = models.DateField("Fecha Diligenciamiento", auto_now=True)
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        related_name="related_users_forms",
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company,
        verbose_name="Compañia",
        related_name="related_company_forms",
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"

    def __str__(self):
        return "%s" % (self.user.email)


class Answer(models.Model):
    """Guarda las respuestas del formulario de un compañia
    """

    form = models.ForeignKey(
        Form,
        verbose_name="Formulario",
        on_delete=models.CASCADE,)
    question = models.ForeignKey(
        Question,
        verbose_name="Pregunta",
        on_delete=models.CASCADE,)
    value = models.TextField(verbose_name="Respueta",
                             help_text='Esta respuesta puede ser de texto abierto, un id del item\
                             de la respuesta, una fecha, o un True o False')
    choice = models.CharField("Id de la respuesta", max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"
        unique_together = ("form", "question")
    

    def __str__(self):
        return "%s" % (self.value)

