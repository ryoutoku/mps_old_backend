from django.contrib import admin
from .models import Negotiation


@admin.register(Negotiation)
class NegotiationAdmin(admin.ModelAdmin):
    pass
