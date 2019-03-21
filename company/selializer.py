# coding: utf-8

from rest_framework import serializers

from .models import CompanyBasicInfo, CompanyStaff, Project


class CompanyBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBasicInfo
        fields = (
            "is_activated",
            "name",
            "representative_last_name",
            "representative_first_name",
            "establishment_date",
            "capital",
            "sales",
            "employee_number",
            "average_age",
            "phone_number",
            "address",
            "closest_station_1",
            "closest_station_2",
            "corporate_url",
            "pr_comment",
            "pr_photo_1",
            "pr_photo_2",
            "needs_paper_invoice",
        )

    def validate(self, attrs):
        name = attrs["name"]
        phone_number = attrs["phone_number"]
        address = attrs["address"]

        is_activated = True

        if name is None or \
                phone_number is None or \
                address is None:
            is_activated = False
        attrs["is_activated"] = is_activated

        return attrs


class CompanyStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStaff
        fields = (
            "staff_last_name",
            "staff_first_name",
            "staff_department",
            "staff_mail_address",
        )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "min_fee",
            "max_fee",
            "workplace",
            "closest_station",
            "start_term",
            "end_term",
            "start_time",
            "end_time",
            "rest_time",
            "garments",
            "restroom",
            "conditions",
            "content",
            "appeal",
            "required_skills",
            "preferred_skills",
        )
