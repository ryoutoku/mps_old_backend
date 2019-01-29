from django.contrib import admin
from django.forms import ValidationError, ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Worker, WorkerBank, Resume
from certification.models import User


class WorkerAdminForm(ModelForm):

    class Meta:
        model = Worker
        fields = "__all__"

    def clean_account(self):

        account = self.cleaned_data["account"]
        user = User.objects.filter(email=account).first()

        if not user:
            raise ValidationError(_("you must set active account"))

        if not user.is_active:
            raise ValidationError(_("you must set active account"))

        if user.is_staff or user.is_superuser:
            raise ValidationError(_("you must set general account"))

        if hasattr(user, 'company'):
            raise ValidationError(_("you must set worker account"))

        return account


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    form = WorkerAdminForm

    list_display = ('full_name', 'account', 'is_activate', )

    def full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    full_name.admin_order_field = 'last_name'


@admin.register(WorkerBank)
class WorkerBankAdmin(admin.ModelAdmin):
    pass


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
