from django.db.models import Q
from django.contrib import admin
from django.forms import ValidationError, ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from .models import Worker, WorkerBank, Resume
from certification.models import User


class WorkerAdminForm(ModelForm):

    class Meta:
        model = Worker
        fields = "__all__"

    def clean_account(self):
        """accountが正しく設定できているかの追加確認
        """

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


class NameFilter(admin.SimpleListFilter):
    title = _("name")
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        return ((True, _("Yes")), (False, _("No")))

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset

        if value == "True":
            return queryset.filter(~Q(last_name=None) & ~Q(first_name=None))

        return queryset.filter(Q(last_name=None) | Q(first_name=None))


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    form = WorkerAdminForm
    _user_link_format = "<a href='../../certification/user/{}/change'>{}<\a>"

    list_display = ('full_name', 'account_name', 'is_activate', )
    list_filter = (NameFilter, 'is_activate',)

    def full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    def account_name(self, obj):
        return format_html(self._user_link_format, obj.account.id, str(obj.account))

    full_name.admin_order_field = 'last_name'
    full_name.short_description = '個人名'

    account_name.admin_order_field = "account"
    account_name.short_description = "登録email"


class WorkerBankAdminForm(ModelForm):

    class Meta:
        model = WorkerBank
        fields = "__all__"

    def clean_worker(self):
        """accountが正しく設定できているかの追加確認
        """

        worker = self.cleaned_data["worker"]

        if not worker:
            raise ValidationError(_("you must set worker account"))

        return worker


@admin.register(WorkerBank)
class WorkerBankAdmin(admin.ModelAdmin):
    form = WorkerBankAdminForm

    list_display = ("id", "worker_name", "name", "is_activate", )

    _worker_link_format = "<a href='../../worker/worker/{}/change'>{}<\a>"

    def worker_name(self, obj):
        return format_html(self._worker_link_format, obj.worker.id, str(obj.worker))

    worker_name.admin_order_field = 'worker'
    worker_name.short_description = "個人名"


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
