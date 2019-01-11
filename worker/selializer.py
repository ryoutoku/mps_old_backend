# coding: utf-8

from rest_framework import serializers

from .models import Worker, Career


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = (
            "last_name",
            "fist_name",
            "mail_address",
            "working_status",
            "work_style",
            "hope_fee",
            "open_status",
            "interested_work",
            "bank_name",
            "bank_office_code",
            "bank_account_type",
            "bank_account_number",
        )


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            "project_name",
            "started_at",
            "ended_at",
            "position",
            "scale",
            "tools",
            "details",
        )
