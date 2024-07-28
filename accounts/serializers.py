# serializers.py
from rest_framework import serializers
from .models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'password']

    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Account with this email already exists.")
        return value

    def create(self, validated_data):
        user = Account.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'].split("@")[0],
            password=validated_data['password']
        )
        user.is_active = False  # Set as inactive initially
        user.save()
        return user
