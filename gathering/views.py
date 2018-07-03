# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render

from api.helpers import get_api_user

from .models import Category, Question, QuestionChoice, Form, Answer
from .serializers import CategorySerializer, QuestionSerializer, QuestionChoiceSerializer,\
                         FormSerializer, AnswerSerializer, QuestionDetailSerializer,\
                         FullQuestionsSerializer
from users.models import Company


class CategoryList(generics.ListAPIView):
    """Api para obtener las categorias de preguntas
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True).order_by('weight')


class QuestionList(generics.ListAPIView):
    """Api para obtener las preguntas de una categoría en 
    específico
    """

    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all().order_by('weight')
        category_id = self.kwargs['category_id']
        if category_id:
            queryset = queryset.filter(category=category_id, is_active=True)
        return queryset


class QuestionChoicesList(generics.ListAPIView):
    """Api para obtener la lista de opciones de una pregunta cuando
    es de tipo "SELECCION"
    """

    serializer_class = QuestionChoiceSerializer

    def get_queryset(self):
        queryset = QuestionChoice.objects.all().order_by('weight')
        question_id = self.kwargs['question_id']
        if question_id:
            queryset = queryset.filter(question=question_id)
        return queryset


class QuestionDetail(generics.ListAPIView):
    """Api para obtener los datos de una pregunta por id
    con los items
    """

    serializer_class = QuestionDetailSerializer

    def get_queryset(self):
        queryset = Question.objects.all().order_by('weight')
        question_id = self.kwargs['question_id']
        if question_id:
            queryset = queryset.filter(pk=question_id, is_active=True)
        return queryset


class FormList(generics.ListAPIView):
    """Api para listar los formularios de un paciente
    """

    serializer_class = FormSerializer

    def get_queryset(self):
        queryset = Form.objects.all().order_by('date')
        company_id = self.kwargs['company_id']
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset


class FullQuestions(generics.ListAPIView):
    """Api para retornar todas las categorías con sus preguntas
    """

    serializer_class = FullQuestionsSerializer

    def get_queryset(self):
        queryset = Question.objects.all().order_by('weight')
        category_id = self.kwargs['category_id']
        if category_id:
            queryset = queryset.filter(category=category_id, is_active=True)
        return queryset


class AnswerCreate(APIView):
    """Api para crear las respuestas de un formulario de un paciente
    """

    def post(self, request):
        user = get_api_user(request)
        for answer in request.data:
            if answer['question'] == 'company_id':
                company = Company.objects.get(id=answer['value'])
                form = Form(
                    user=user,
                    company=company
                )
                form.save()
        
        answer_questions = []
        if form is not None:
            questions = Question.objects.all()
            for answer in request.data:
                if answer['question'] != 'company_id':
                    question = Question.objects.get(pk=answer['question'])
                    if question.question_type != Question.SELECCION:
                        instance = Answer(
                            form=form,
                            question=question,
                            value=answer['value']
                        )
                        instance.save()
                        answer_questions.append(instance.question)
                    elif question.question_type == Question.BOOLEANO:
                        instance = Answer(
                            form=form,
                            question=question,
                            value=True,
                        )
                        instance.save()
                        answer_questions.append(instance.question)
                    else:
                        choice = QuestionChoice.objects.get(pk=answer['value'])
                        instance = Answer(
                            form=form,
                            question=question,
                            value=str(choice.value),
                            choice=answer['value']
                        )
                        instance.save()
                        answer_questions.append(instance.question)
            
            questions = Question.objects.all()
            no_answers = []
            [no_answers.append(x) for x in questions if x not in answer_questions]

            for a in no_answers:
                instance = Answer(
                    form=form,
                    question=a,
                    value='off'
                )
                instance.save()

            response = {'detail': "Formulario creado correctamente"}
            stat = status.HTTP_201_CREATED
        else:
            response = {'detail': "Ocurrió un error inesperado"}
            stat = status.HTTP_400_BAD_REQUEST

        return Response(response, status=stat)


class AnswersFormDetail(generics.ListAPIView):
    """Api para listar las respuestas de un formulario
    """

    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = Answer.objects.all()
        form_id = self.kwargs['form_id']
        if form_id:
            queryset = queryset.filter(form=form_id).order_by('question__name')
        return queryset
