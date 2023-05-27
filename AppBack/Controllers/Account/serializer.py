from rest_framework import serializers
from AppBack.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'user_type', 'password', 'email', 'user_status']