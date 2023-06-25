from django.contrib.auth.models import User as Account
from rest_framework import serializers

from AppBack.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class AccountMedicSerializer(serializers.ModelSerializer):
    user_id = AccountSerializer()

    class Meta:
        model = User
        fields = "__all__"


class AccountsSomeFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "username", "email", "last_login"]


class AccountsSomeFieldsSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name"]


class AccountMedicGetSerializer(serializers.ModelSerializer):
    user_id = AccountsSomeFieldsSerializer()

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "id_type",
            "first_name",
            "last_name",
            "city",
            "cellphone",
        ]
