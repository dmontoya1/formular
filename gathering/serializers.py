# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from users.models import User, Company
from .models import Category, Question, QuestionChoice, Form, Answer


class CategorySerializer(serializers.ModelSerializer):
    """Serializador para las categorías
    """

    class Meta:
        model = Category
        fields = ('id', 'name',)


class QuestionSerializer(serializers.ModelSerializer):
    """Serializador para las preguntas
    """

    category = CategorySerializer(many=False, read_only=False)

    class Meta:
        model = Question
        fields = ('id', 'category', 'context', 'question_type', 'weight',)


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """Serializador para las opciones de las preguntas, cuando ésta pregunta
    es de tipo "SELECCION"
    """

    class Meta:
        model = QuestionChoice
        fields = ('id', 'question', 'value', 'weight')


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Serializador para las preguntas por id
    """

    related_question_choices = QuestionChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'category', 'context', 'question_type', 'related_question_choices',
                  'weight',)


class FormSerializer(serializers.ModelSerializer):
    """Serializador para los Formularios
    """

    date = serializers.DateField(required=False)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False
    )

    class Meta:
        model = Form
        fields = ('id', 'date', 'company')


class AnswerSerializer(serializers.ModelSerializer):
    """Serializador para las respuestas de un formulario
    """

    form = FormSerializer(many=False, read_only=True)
    question = QuestionSerializer(many=False, read_only=False)

    class Meta:
        model = Answer
        fields = ('value', 'form', 'question')


class FullQuestionChoiceDQSerializer(serializers.ModelSerializer):
    """Serializador para las opciones de respuestas de las preguntas
    """

    class Meta:
        model = QuestionChoice
        fields = ('id', 'value', 'weight')

    
class FullQuestionDQSerializer(serializers.ModelSerializer):
    """Serializador para las preguntas con todas sus opciones (Cuando las tenga)
    """

    related_question_choices = FullQuestionChoiceDQSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'context', 'question_type', 'weight', 'related_question_choices')


class FullQuestionChoiceSerializer(serializers.ModelSerializer):
    """Serializador para las opciones de respuestas de las preguntas
    """

    dependant_question = FullQuestionDQSerializer(many=True, required=False)

    class Meta:
        model = QuestionChoice
        fields = ('id', 'value', 'weight')


class FullQuestionsSerializer(serializers.ModelSerializer):
    """Serializador para las preguntas con todas sus opciones (Cuando las tenga)
    """

    related_question_choices = FullQuestionChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'context', 'question_type', 'weight', 'related_question_choices')

