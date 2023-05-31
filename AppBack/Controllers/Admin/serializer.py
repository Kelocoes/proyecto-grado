from rest_framework import serializers

from AppBack.models import Account, User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user_id", "email", "user_status"]


class AdminSerializer(serializers.ModelSerializer):
    user_id = AccountSerializer()

    class Meta:
        model = User
        fields = ["user_id", "user_type", "name", "last_name", "city"]
