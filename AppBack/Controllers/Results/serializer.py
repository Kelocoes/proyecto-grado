from rest_framework import serializers

from AppBack.models import Patient, Results, ResultsMedicPatient, User


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patient_id", "first_name", "last_name", "outcome"]


class MedicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "id_type", "first_name", "last_name"]


class ResultsMedicPatientSerializer(serializers.ModelSerializer):
    result = ResultsSerializer()
    patient = PatientSerializer()
    user = MedicSerializer()

    class Meta:
        model = ResultsMedicPatient
        fields = ["result", "user", "patient"]
