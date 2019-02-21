# coding: utf-8

from rest_framework import serializers

from .models import Worker, Resume, WorkerBank


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = (
            "last_name",
            "first_name",
            "address",
            "working_status",
            "work_style",
            "hope_fee",
            "interested_work",
            "qiita_url",
            "github_url",
            "phone_number",
            "experience",
            "is_open",
            "is_activate",
            "sex",
            "birth_day"
        )


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerBank
        fields = (
            "name",
            "office_code",
            "account_type",
            "account_number"
        )


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            "id",
            "project_name",
            "started_at",
            "ended_at",
            "position",
            "scale",
            "tools",
            "details",
        )
