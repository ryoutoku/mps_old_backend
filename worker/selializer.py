# coding: utf-8

from rest_framework import serializers

from .models import Worker, Resume, WorkerBank


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = (
            "last_name",
            "first_name",
            "working_status",
            "work_style",
            "hope_fee",
            "open_status",
            "interested_work",
            "qiita_url",
            "github_url"
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
            "pk",
            "project_name",
            "started_at",
            "ended_at",
            "position",
            "scale",
            "tools",
            "details",
        )
