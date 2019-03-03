# coding: utf-8

from rest_framework import serializers

from .models import WorkerBasicInfo, WorkerCondition, Resume


class WorkerBasicInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerBasicInfo

        fields = (
            "is_activated",
            "last_name",
            "last_name_kana",
            "first_name",
            "first_name_kana",
            "address",
            "phone_number",
            "birth_day",
            "sex",
            "bank_name",
            "bank_office_code",
            "bank_account_type",
            "bank_account_number",
        )

    def validate(self, attrs):
        last_name = attrs["last_name"]
        first_name = attrs["first_name"]
        last_name_kana = attrs["last_name_kana"]
        first_name_kana = attrs["first_name_kana"]
        address = attrs["address"]

        is_activated = True

        if last_name is None or \
                last_name_kana is None or \
                first_name is None or \
                first_name_kana is None or \
                address is None:
            is_activated = False
        attrs["is_activated"] = is_activated

        return attrs


class WorkerConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerCondition

        fields = (
            "is_open",
            "experience",
            "work_style",
            "working_status",
            "hope_fee",
            "interested_work",
            "qiita_url",
            "github_url",
            "other_url",
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
