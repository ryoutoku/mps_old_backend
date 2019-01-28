from django.contrib import admin
from .models import Worker, WorkerBank, Resume

from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        print(request)
        print(obj)
        print(form)
        print(change)
        raise ValidationError(
            _('Invalid value:'),
            code='invalid',
            params={'value': '42'},
        )
        super().save_model(request, obj, form, change)


@admin.register(WorkerBank)
class WorkerBankAdmin(admin.ModelAdmin):
    pass


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
