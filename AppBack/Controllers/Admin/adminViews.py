from rest_framework import generics
from .serializer import AdminSerializer

from AppBack.models import Account, User
from rest_framework import permissions
from rest_framework.views import APIView

class GetAdmin(generics.RetrieveAPIView):
    serializer_class = AdminSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(user_type = "Admin")