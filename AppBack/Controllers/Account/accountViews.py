from rest_framework import generics
from .serializer import AccountSerializer

from AppBack.models import Account
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

class isActive(APIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):

        user_id = request.data['user_id']

        account = Account.objects.filter(user_id = user_id).first()

        if (not(account is None)):
            account_dict = account.__dict__
            user_type = account_dict['user_type']
            user_satus = account_dict['user_status']
        else: 
            user_type = 'not found'
            user_satus = True

        return Response({
            'user_type': user_type, 
            'user_status' :user_satus
            }
        )
