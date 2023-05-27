from rest_framework import generics
from .serializer import PatientSerializer

from AppBack.models import Patient
from rest_framework import permissions

class GetPatient(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Patient.objects.all()

class GetAllPatients(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Patient.objects.all()