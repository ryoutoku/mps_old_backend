# coding: utf-8
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from .models import Question, Answer
from worker.models import Worker, Resume
from company.models import Company
from .selializer import QuestionSerializer, AnswerSerializer

from utility.permission import CustomDictPermission, IsWorker
from utility.exception import ResumeIDNotFoundException, QuestionIDNotFoundException


class CanUseQuestion(CustomDictPermission):

    SAFE_PETTERN = {
        "worker": ["GET", 'DELETE', 'HEAD', 'OPTIONS'],
        "company": ["GET", "POST", "HEAD", "OPTIONS"]
    }


class QuestionViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and CanUseQuestion, )

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if hasattr(self.request.user, "company"):
            queryset = queryset.filter(company=self.request.user.company).all()
        else:
            resume = Resume.objects.filter(
                worker=self.request.user.worker).all()
            queryset = queryset.filter(
                resume__in=resume).all()
        return queryset

    def perform_create(self, serializer):
        data = serializer.data
        resume = Resume.objects.filter(pk=data["resume_id"]).first()

        if not resume:
            raise ResumeIDNotFoundException()

        company = self.request.user.company
        data["resume"] = resume
        data["company"] = company
        obj = Question.objects.create(**data)
        obj.clean()
        obj.save()


class AnswerViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated and IsWorker, )

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        resume = Resume.objects.filter(worker=self.request.user.worker).all()
        question = Question.objects.filter(resume__in=resume).all()
        queryset = super().get_queryset()
        queryset = queryset.filter(question__in=question)
        return queryset

    def perform_create(self, serializer):
        data = serializer.data
        question = Question.objects.filter(
            pk=data["question_id"]).first()

        if not question:
            raise QuestionIDNotFoundException()

        data["question"] = question
        obj = Answer.objects.create(**data)
        obj.clean()
        obj.save()

    """
    def list(self, request, *args, **kwargs):
        data = self.get_queryset().first()
        serializer = self.get_serializer(data)
        return Response(serializer.data)
    """
