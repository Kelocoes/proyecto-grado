from rest_framework import generics, permissions

from AppBack.models import User

from .serializer import AdminSerializer


class GetAdmin(generics.RetrieveAPIView):
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(user_type="Admin")
