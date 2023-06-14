from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import User

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AccountAdminSerialier, AdminSerializer


class GetAdmin(APIView):
    serializer_class = AccountAdminSerialier
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            id = user.id

            user = User.objects.get(pk=id)
            serializer = AccountAdminSerialier(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateAdmin(APIView):
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]

    def put(self, request):
        try:
            user = request.user

            try:
                admin = User.objects.get(pk=user.id)
            except User.DoesNotExist:
                return Response(
                    {"detail": "No existe el usuario"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = AdminSerializer(admin, data=request.data)

            # Valida los datos del serializer
            if serializer.is_valid():
                # Guarda los datos actualizados en la base de datos
                serializer.save()
                return Response(
                    {"mensaje": "Información actualizada correctamente"},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
