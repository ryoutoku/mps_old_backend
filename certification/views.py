from django.views.generic import TemplateView, CreateView
from datetime import datetime
from django.utils.timezone import utc
from .models import User, SignUpToken
from .forms import UserModelForm

from django.http import HttpResponseRedirect


class UserCreateView(CreateView):

    model = User
    form_class = UserModelForm
    template_name = "./signup/index.html"
    success_url = "./success"
    failure_url = "./failure"

    def get(self, request, **kwargs):

        token = request.GET.get("token", default=None)

        if token is None:
            return HttpResponseRedirect(self.failure_url)

        expiration_date = SignUpToken.objects.filter(token=token).first()

        if expiration_date is None:
            return HttpResponseRedirect(self.failure_url)

        now = datetime.utcnow()
        print(expiration_date)
        print(now)

        if expiration_date <= now:
            HttpResponseRedirect(self.failure_url)

        return super().get(request, **kwargs)


class SuccessView(TemplateView):
    template_name = "./signup/success.html"


class FailureView(TemplateView):
    template_name = "./signup/failure.html"
