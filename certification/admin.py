from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User, SignUpToken
from django import forms

from company.models import Company
from worker.models import Worker

import secrets


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', )


class MyUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'joined_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'worker',
                    'company', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser',
                   'is_active', 'groups')
    search_fields = ('email', 'is_superuser', 'is_active')
    ordering = ('email',)

    def worker(self, obj):
        if obj.worker is not None:
            return obj.worker.name
        return None

    def company(self, obj):
        if obj.company is not None:
            return obj.company.name
        return None


admin.site.register(User, MyUserAdmin)


@admin.register(SignUpToken)
class SignUpTokenAdmin(admin.ModelAdmin):
    """Singup用アクセストークンを管理する
    """

    list_display = ('token', 'expiration_date')

    fieldsets = [
        ("expiration_date", {'fields': ['expiration_date']}),
    ]

    def save_model(self, request, obj, form, change):

        if not obj.token:
            obj.token = secrets.token_hex(4)

        super().save_model(request, obj, form, change)
