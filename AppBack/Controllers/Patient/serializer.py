from rest_framework import serializers

from AppBack.models import MedicPatient, Patient, User


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class MedicPatientSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    user = UserSerializer()

    class Meta:
        model = MedicPatient
        fields = ["patient", "user"]
