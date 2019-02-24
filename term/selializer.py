# coding: utf-8

from rest_framework import serializers

from .models import ServiceOfTerm, PrivacyPolicy


class ServiceOfTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOfTerm
        fields = (
            "context"
        )


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = (
            "context"
        )
