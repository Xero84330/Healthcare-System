from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from Apps.Authentication.models.Users import User


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["name", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)