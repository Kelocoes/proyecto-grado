from rest_framework import generics, permissions

from AppBack.models import User

from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AdminSerializer


class GetAdmin(generics.RetrieveAPIView):
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]
    queryset = User.objects.filter(user_type="Admin")
