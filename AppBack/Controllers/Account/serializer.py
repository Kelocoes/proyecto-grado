from django.contrib.auth.models import User as Account
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class AccountStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["is_active"]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["username, email"]
