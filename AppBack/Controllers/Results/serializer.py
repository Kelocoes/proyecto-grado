from rest_framework import serializers
from AppBack.models import Results, Results_Medic_Patient

class ResultsSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Results
        fields = '__all__'


class ResultsMedicPatientSerializer(serializers.ModelSerializer):
    result = ResultsSerializer()

    class Meta:
        model = Results_Medic_Patient
        fields = ['result', 'user', 'patient']

