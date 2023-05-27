from rest_framework import serializers
from AppBack.models import Results

class ResultsSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Results
        fields = '__all__'