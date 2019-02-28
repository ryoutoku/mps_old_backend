# coding: utf-8

from rest_framework import serializers

from .models import WorkerBasicInfo, WorkerCondition, Resume


class WorkerBasicInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerBasicInfo

        fields = (
            "is_activate",
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

    def validate_is_activate(self, is_activate):
        """activateはシリアライズ時にはチェックしない
        """
        return is_activate


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
