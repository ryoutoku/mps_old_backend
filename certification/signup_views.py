from django.views.generic import TemplateView, CreateView
from django.utils.timezone import utc
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from rest_framework import views, permissions, authentication

from rest_framework import generics

from datetime import datetime
from .models import User, SignUpToken
from .forms import WorkerModelForm, CompanyModelForm


class SignUpBaseCreateView(CreateView):

    model = User
    form_class = None
    template_name = "./signup/index.html"
    success_url = "./success"
    failure_url = "./failure"

    def get(self, request, attribute, **kwargs):
        token = request.GET.get("token", default=None)

        if token is None:
            return HttpResponseRedirect(self.failure_url)

        signup_token = SignUpToken.objects.filter(
            token=token, attribute=attribute).first()

        tmp = SignUpToken.objects.filter(token=token).first()
        if signup_token is None:
            return HttpResponseRedirect(self.failure_url)

        now = datetime.utcnow().replace(tzinfo=utc)
        if signup_token.expiration_date <= now:
            HttpResponseRedirect(self.failure_url)

        return super().get(request, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(user.password)
        user.save()
        return HttpResponseRedirect(self.success_url)


class WorkerCreateView(SignUpBaseCreateView):
    worker = 1
    form_class = WorkerModelForm

    def get(self, request, **kwargs):
        return super().get(request, self.worker, **kwargs)


class CompanyCreateView(SignUpBaseCreateView):
    company = 0
    form_class = CompanyModelForm

    def get(self, request, **kwargs):
        return super().get(request, self.company, **kwargs)


class SuccessView(TemplateView):
    template_name = "./signup/success.html"


class FailureView(TemplateView):
    template_name = "./signup/failure.html"


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return