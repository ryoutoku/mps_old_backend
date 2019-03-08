# coding: utf-8

from rest_framework import serializers

from .models import WorkerBasicInfo, WorkerCondition, Resume, Technology


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


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology

        fields = (
            "name",
        )


class WorkerConditionSerializer(serializers.ModelSerializer):

    interested_work = TechnologySerializer(many=True)

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

    def update(self, instance, validated_data):
        instance.is_open = validated_data.get(
            "is_open", instance.is_open)
        instance.experience = validated_data.get(
            "experience", instance.experience)
        instance.work_style = validated_data.get(
            "work_style", instance.work_style)
        instance.working_status = validated_data.get(
            "working_status", instance.working_status)
        instance.hope_fee = validated_data.get(
            "hope_fee", instance.hope_fee)
        instance.qiita_url = validated_data.get(
            "qiita_url", instance.qiita_url)
        instance.github_url = validated_data.get(
            "github_url", instance.github_url)
        instance.other_url = validated_data.get(
            "other_url", instance.other_url)

        tech_list = validated_data.pop("interested_work")

        for tech_data in tech_list:
            tech = Technology.objects.filter(
                name__iexact=tech_data["name"]).first()

            if tech is None:
                tech = Technology.objects.create(name=tech_data["name"])
                tech.save()

            instance.interested_work.add(tech)
        instance.save()
        return instance


class ResumeSerializer(serializers.ModelSerializer):

    tools = TechnologySerializer(many=True)

    class Meta:
        model = Resume
        fields = (
            "id",
            "project_name",
            "started_at",
            "ended_at",
            "project_type",
            "charge_of_process",
            "role_in_project",
            "project_scale",
            "tools",
            "detail",
        )
