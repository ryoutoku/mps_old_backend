# coding: utf-8

from rest_framework import serializers

from .models import Company, Project


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "name",
            "staff_name",
            "phone_number",
            "mail_address",
            "address",
            "closest_station_1",
            "closest_station_2",
            "needs_paper_invoice",
            "company_url",
            "start_office_hours",
            "end_office_hours",
            "contact_staff",
            "contact_staff_mail_address",
            "pr_comment",
            "pr_photo_1",
            "pr_photo_2",
        )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
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
