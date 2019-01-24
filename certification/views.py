from django.views.generic import TemplateView, CreateView
from django.utils.timezone import utc
from django.http import HttpResponseRedirect
from django.contrib import messages

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


class UserCreateView(SignUpBaseCreateView):
    worker = 1
    form_class = WorkerModelForm

    def get(self, request, **kwargs):
        print(request.GET)
        return super().get(request, self.worker, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return HttpResponseRedirect(self.success_url)


class CompanyCreateView(SignUpBaseCreateView):
    company = 0
    form_class = CompanyModelForm

    def get(self, request, **kwargs):
        return super().get(request, self.company, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return HttpResponseRedirect(self.success_url)


class SuccessView(TemplateView):
    template_name = "./signup/success.html"


class FailureView(TemplateView):
    template_name = "./signup/failure.html"
