# coding: utf-8
from django.contrib.auth import authenticate
from rest_framework import serializers
import re
from datetime import datetime
from django.utils.timezone import utc

from .models import User, SignUpToken


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


class LogoutSerializer(serializers.Serializer):
    pass


class SingUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    token = serializers.CharField()

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if user is not None:
            raise serializers.ValidationError(
                "this email address is already registration")
        return email

    def validate_password(self, password):
        pattern = r"\w{8,20}"

        if re.match(pattern, password) is None:
            raise serializers.ValidationError(
                "our password must be 8 to 20 characters long"
            )
        return password

    def validate_token(self, token):
        signup_token = SignUpToken.objects.filter(token=token).first()

        if signup_token is None:
            raise serializers.ValidationError(
                "this page is timeout"
            )

        now = datetime.utcnow().replace(tzinfo=utc)
        if signup_token.expiration_date <= now:
            raise serializers.ValidationError(
                "this page is timeout"
            )
        return token
