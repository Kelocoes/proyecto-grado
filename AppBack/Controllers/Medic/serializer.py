from rest_framework import serializers

from AppBack.models import Account, User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user_id", "email", "user_status"]


class MedicAccountSerializer(serializers.ModelSerializer):
    user_id = AccountSerializer()

    class Meta:
        model = User
        fields = ["user_id", "user_type", "name", "last_name", "city"]


class MedicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
