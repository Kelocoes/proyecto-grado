from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import User

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AdminSerializer


class GetAdmin(APIView):
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            id = user.id

            user = User.objects.get(pk=id)
            serializer = AdminSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
