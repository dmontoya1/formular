# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views

app_name = 'gathering'
urlpatterns = [
    path('categories/<int:category_id>/full_questions/', views.FullQuestions.as_view(), name='questions-full-list'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:category_id>/questions/', views.QuestionList.as_view(), name='question-list'),
    path('questions/<int:question_id>/choices/', views.QuestionChoicesList.as_view(), name='question-choice-list'),
    path('question/<int:question_id>/', views.QuestionDetail.as_view(), name='question-detail'),
    path('forms/<int:company_id>/', views.FormList.as_view(), name='form-list'),
    path('answer/', views.AnswerCreate.as_view(), name='answer-create'),
]
