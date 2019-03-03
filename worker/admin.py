from django.db.models import Q
from django.contrib import admin
from django.forms import ValidationError, ModelForm
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from .models import WorkerBasicInfo, WorkerCondition, Resume, ProjectType, ChargeOfProcess, RoleInProject, Technology
from certification.models import User


class WorkerBasicInfoAdminForm(ModelForm):

    class Meta:
        model = WorkerBasicInfo
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


@admin.register(WorkerBasicInfo)
class WorkerBasicInfoAdmin(admin.ModelAdmin):
    form = WorkerBasicInfoAdminForm
    _link_format = "<a href='{}'>{}<\a>"

    list_display = ("id", 'full_name', 'account_name', 'is_activated', )
    list_filter = (NameFilter, 'is_activated',)

    def full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    def account_name(self, obj):
        account = obj.account
        url = reverse(
            f'admin:{account._meta.app_label}_{account._meta.model_name}_change', args=(account.pk,)
        )

        return format_html(self._link_format, url, str(account))

    full_name.admin_order_field = 'last_name'
    full_name.short_description = '個人名'

    account_name.admin_order_field = "account"
    account_name.short_description = "登録email"


class WorkerConditionAdminForm(ModelForm):

    class Meta:
        model = WorkerCondition
        fields = "__all__"

    def clean_worker(self):
        """workerが正しく設定できているかの追加確認
        """
        worker = self.cleaned_data["worker"]
        user = WorkerBasicInfo.objects.filter(pk=worker.id).first()

        if not user:
            raise ValidationError(_("you must set active worker"))

        return worker


@admin.register(WorkerCondition)
class WorkerConditionAdmin(admin.ModelAdmin):
    form = WorkerConditionAdminForm

    list_display = ("id", "worker_name", )

    _link_format = "<a href='{}'>{}<\a>"

    def worker_name(self, obj):

        worker = obj.worker
        url = reverse(
            f'admin:{worker._meta.app_label}_{worker._meta.model_name}_change', args=(worker.pk,)
        )
        return format_html(self._link_format, url, str(worker))

    worker_name.admin_order_field = 'worker'
    worker_name.short_description = "個人名"


class ResumeAdminForm(ModelForm):

    class Meta:
        model = Resume
        fields = "__all__"

    def clean_worker(self):
        """workerが正しく設定できているかの追加確認
        """
        worker = self.cleaned_data["worker"]
        user = WorkerBasicInfo.objects.filter(pk=worker.id).first()

        if not user:
            raise ValidationError(_("you must set active worker"))

        return worker


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    form = ResumeAdminForm

    list_display = ("id", "worker_name", "project_name",
                    "started_at", "ended_at")
    list_filter = ("started_at", "ended_at")

    _link_format = "<a href='{}'>{}<\a>"

    def worker_name(self, obj):

        worker = obj.worker
        url = reverse(
            f'admin:{worker._meta.app_label}_{worker._meta.model_name}_change', args=(worker.pk,)
        )
        return format_html(self._link_format, url, str(worker))

    worker_name.admin_order_field = 'worker'
    worker_name.short_description = "個人名"


@admin.register(RoleInProject)
class RoleInProjectAdmit(admin.ModelAdmin):
    list_display = ("id", "role_name")


@admin.register(ChargeOfProcess)
class ChargeOfProcessAdmin(admin.ModelAdmin):
    list_display = ("id", "process_name")


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "project_type")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "lower_name")
