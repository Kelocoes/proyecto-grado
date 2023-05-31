from rest_framework import serializers

from AppBack.models import Patient, Results, Results_Medic_Patient


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patient_id", "name", "last_name"]


class ResultsMedicPatientSerializer(serializers.ModelSerializer):
    result = ResultsSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Results_Medic_Patient
        fields = ["result", "user", "patient"]
