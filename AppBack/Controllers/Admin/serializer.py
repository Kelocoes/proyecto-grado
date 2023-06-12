from django.contrib.auth.models import User as Account
from rest_framework import serializers

from AppBack.models import User


class AccountAdminSerialier(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "last_login"]


class AdminSerializer(serializers.ModelSerializer):
    user_id = AccountAdminSerialier()

    class Meta:
        model = User
        fields = [
            "user_id",
            "id",
            "id_type",
            "first_name",
            "last_name",
            "city",
            "cellphone",
        ]
