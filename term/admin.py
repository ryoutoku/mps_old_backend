from django.db.models import Q
from django.contrib import admin
from django.forms import ValidationError, ModelForm
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from .models import ServiceOfTerm, PrivacyPolicy


@admin.register(ServiceOfTerm)
class ServiceOfTermAdmin(admin.ModelAdmin):

    list_display = ("target_type", 'create_at', "context")
    list_filter = ('create_at',)


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):

    list_display = ("target_type", 'create_at', "context")
    list_filter = ('create_at',)
