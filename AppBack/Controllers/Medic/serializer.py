from django.contrib.auth.models import User as Account
from rest_framework import serializers

from AppBack.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class MedicAccountSerializer(serializers.ModelSerializer):
    user_id = AccountSerializer()

    class Meta:
        model = User
        fields = "__all__"


class AccountMedicSerialier(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "last_login"]


class MedicSerializer(serializers.ModelSerializer):
    user_id = AccountMedicSerialier()

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
