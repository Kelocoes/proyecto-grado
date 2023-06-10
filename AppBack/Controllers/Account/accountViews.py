from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import Account

from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AccountSerializer, AccountStatusSerializer


class isActive(APIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        user_id = request.data["user_id"]

        account = Account.objects.filter(user_id=user_id).first()

        if account is not None:
            account_dict = account.__dict__
            user_type = account_dict["user_type"]
            user_satus = account_dict["user_status"]
        else:
            user_type = "not found"
            user_satus = True

        return Response({"user_type": user_type, "user_status": user_satus})


class ChangeStatus(generics.UpdateAPIView):
    serializer_class = AccountStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]
    queryset = Account.objects.all()
