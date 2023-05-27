from rest_framework import generics
from .serializer import AccountSerializer

from AppBack.models import Account
from rest_framework import permissions

class RetreiveAllAccounts(generics.ListAPIView):
    serializer_class = AccountSerializer
    model = Account
    permission_classes = [permissions.AllowAny]
    queryset = Account.objects.all()