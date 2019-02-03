# coding: utf-8

from rest_framework import serializers

from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "resume_id",
            "detail",
        )

    resume_id = serializers.IntegerField(required=True)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "question_id",
            "detail",
        )

    question_id = serializers.IntegerField(required=True)
