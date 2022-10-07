import os

from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=80, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        password = attrs.get("password", "")

        attrs['image'] = None

        if not password:
            raise serializers.ValidationError({
                "password":"password is required!"
            })

        if len(password) < 8:
            raise serializers.ValidationError("password must be at least 8 characters")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=5, write_only=True)
    password = serializers.CharField(max_length=80, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["email", "password", "tokens"]

    def get_tokens(self, data):
        tokens = data.get('tokens')
        tokens = tokens()
        return {
            "refresh" : tokens["refresh"],
            "access" : tokens["access"]
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        
        get_user = User.objects.filter(email=email)

        user = authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed("invalid credientials!")

        if not user.is_active:
            raise AuthenticationFailed("user is not active!")
        
        if not user.is_verify:
            raise AuthenticationFailed("verify your email!")

        return {
            "tokens" : user.tokens
        }

class GetUserFromTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True)
    email = serializers.CharField(max_length=255, min_length=5, read_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    profile_pic = serializers.ImageField(read_only=True)
    
    def validate(self, attrs):
        user_id = attrs.get('user_id')
        
        user = User.objects.filter(id=user_id).first()

        if user:
            return {
                "email" : user.email,
                "username" : user.username,
                "profile_pic" : user.image,
            }
        raise AuthenticationFailed("not found any user!")

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email','')
        
        user = User.objects.filter(email=email)

        if not email:
            raise serializers.ValidationError("email is required!")

        if not user:
            raise AuthenticationFailed(f'{email} is not register!')

        if user and user[0].auth_provider != "email":
            raise AuthenticationFailed(f'your email is register as {user[0].auth_provider}')

        return attrs

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            password_reset_token = PasswordResetTokenGenerator()
            if not password_reset_token.check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
