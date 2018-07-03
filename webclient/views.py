# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_xhtml2pdf.utils import generate_pdf

from rest_framework.authentication import BasicAuthentication 

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, View, ListView

from api.helpers import CsrfExemptSessionAuthentication
from gathering.models import Form, Answer
from users.models import UserToken, Company


class HomePageView(TemplateView):
    """ Index de la plataforma
    """

    template_name = 'home/home.html'


class StartGathering(LoginRequiredMixin, TemplateView):
    """Vista antes de comenzar el formulario
    """

    template_name = 'gathering/start_gathering.html'
    login_url = '/'
    redirect_field_name = 'next'


class GatheringForm(LoginRequiredMixin, TemplateView):
    """ Vista del Formulario
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    template_name = 'gathering/gathering_form.html'
    login_url = '/'
    redirect_field_name = 'next'

    def post(self, request, *args, **kwargs):
        company_id = request.POST['company_id']
        context = {
            'company': company_id
        }
        return render(request, 'gathering/gathering_form.html', context)


class SelectCompany(LoginRequiredMixin, TemplateView):
    """Vista para seleccionar la empresa a la cual se le hará 
    la toma de requerimientos
    """

    template_name = 'gathering/select_company.html'
    login_url = '/'
    redirect_field_name = 'next'


class LoginView(View):
    """Iniciar Sesión 
    """

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            url = reverse('webclient:start-gathering')
            login(request, user)
        else:
            response = {'error': 'Correo y/o contraseña incorrectas.'}
            return JsonResponse(response, status=400)

        return JsonResponse(url, safe=False)


class ResetPasswordView(TemplateView):
    """Vista para Recuperar la constraseña
    """

    template_name = 'users/reset_password.html'

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = get_user_model().objects.filter(email=email)[0]
            user.set_password(password)
            user.save()
            user_token = UserToken.objects.get(user=user)
            user_token.is_use_token = True
            user_token.save()
            
            messages.add_message(
                request,
                messages.ERROR, 
                "!Felicitaciones!, tu contraseña se ha cambiado correctamente, ahora puedes ingresar con tu nueva contraseña"
            )
            return HttpResponseRedirect(reverse('webclient:home'))
            
        except MultiValueDictKeyError:
            messages.add_message(
                request,
                messages.ERROR, 
                "No hemos podido cambiar tu contraseña debido a un error inesperado"
            )
        return HttpResponseRedirect(reverse('webclient:home'))		

    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            try:
                user = UserToken.objects.get(is_use_token=False, password_activation_token=token)
            except UserToken.DoesNotExist:
                messages.add_message(
                    request,
                    messages.ERROR, 
                    "Lo sentimos el enlace al que intenta acceder ha dejado de funcionar"
                )
                return HttpResponseRedirect(reverse('webclient:home'))

            context = self.get_context_data(user.user)
            return self.render_to_response(context)

        except MultiValueDictKeyError as e:
            return HttpResponseRedirect(reverse('webclient:home'))

        context = self.get_context_data()
        return self.render_to_response(context)
    
    def get_context_data(self,user=None, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        context['user'] = user
        return context
    

class FormHistory(LoginRequiredMixin, ListView):

    model = Form
    login_url = '/'
    redirect_field_name = 'next'
    template_name = 'gathering/form_history.html'

    def get_queryset(self):
        queryset = super(FormHistory, self).get_queryset()
        queryset = Form.objects.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            pass
        else:
            user = request.user
            forms = Form.objects.filter(user=user)
            if not forms:
                redirect_url = 'webclient:start-gathering'
                return redirect(reverse(redirect_url))
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def export_form_pdf(request, form_id=None):
    """Función para descargar el formulario en pdf
    """
    form = Form.objects.get(pk=form_id)
    context = {
        'headers': (
            'Pregunta',
            'Respuesta',
        ),
        'answers': Answer.objects.filter(form=form).order_by('question__category__name'),
        'company': form.company,
        'date': form.date
    }
    report_template_name = 'forms/forms.html'
	
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="form.pdf"'
    result = generate_pdf(report_template_name, file_object=response, context=context)
    return response


def send_form_email(request, form_id=None):
    """Función para enviar un email con el formulario
    """

    form = Form.objects.get(pk=form_id)
    context = {
        'headers': (
            'Categoría',
            'Pregunta',
            'Respuesta',
        ),
        'answers': Answer.objects.filter(form=form).exclude(question__question_type='TA').order_by('question__category__name'),
        'answers_ta': Answer.objects.filter(form=form, question__question_type='TA').order_by('question__category__name'),
        'company': form.company,
        'date': form.date
    }
    template = 'emails/form-email.html'
    body = loader.get_template(template).render(context)
    message = EmailMessage("Detalle de Formulario", body, "no-reply@formular.com", [settings.EMAIL_USER])
    message.content_subtype = 'html'
    message.send()

    messages.add_message(
        request,
        messages.ERROR, 
        "Correo enviado correctamente!"
    )

    return HttpResponseRedirect(reverse('webclient:form-history'))	
