# coding: utf-8
from django.contrib.auth import authenticate
from rest_framework import serializers
import re
from datetime import datetime
from django.utils.timezone import utc

from .models import User, SignUpToken

from rest_framework.exceptions import NotAcceptable, PermissionDenied


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'], password=attrs['password'])

        if not user:
            raise NotAcceptable(detail="Incorrect email or password.")

        if not user.is_active:
            raise NotAcceptable(detail="Incorrect email or password.")

        return {'user': user}


class LogoutSerializer(serializers.Serializer):
    pass


class SingUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        """validation tokenからチェックするため個別チェックはしない
        """

        email = attrs['email']
        password = attrs['password']
        token = attrs['token']

        self._validate_token(token)
        self._validate_email(email)
        self._validate_password(password)

        return attrs

    def _validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if user is not None:
            raise NotAcceptable(
                detail="this email address is already registration")
        return email

    def _validate_password(self, password):
        pattern = r"\w{8,20}"
        if re.match(pattern, password) is None:
            raise NotAcceptable(
                detail="our password must be 8 to 20 characters long")
        return password

    def _validate_token(self, token):
        signup_token = SignUpToken.objects.filter(token=token).first()

        if signup_token is None:
            raise PermissionDenied(detail="token is not accepted")

        now = datetime.utcnow().replace(tzinfo=utc)
        if signup_token.expiration_date <= now:
            raise PermissionDenied(detail="token is timeout")

        return token
