from rest_framework import generics
from .serializer import MedicSerializer

from AppBack.models import Account, User
from rest_framework import permissions
from rest_framework.views import APIView

class GetMedic(generics.RetrieveAPIView):
    serializer_class = MedicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(user_type = "Medico")

class GetAllMedics(generics.ListAPIView):
    serializer_class = MedicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(user_type = "Medico").all()