from rest_framework import serializers

from AppBack.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user_id", "user_type", "email", "user_status"]


class AccountStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user_status"]
