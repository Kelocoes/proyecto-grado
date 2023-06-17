from django.contrib.auth.models import User as Account
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import User

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AccountAdminSerialier, AccountSerializer, UserSerializer


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
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]

    def put(self, request):
        try:
            user = request.user

            try:
                admin = User.objects.get(pk=user.id)
                account = Account.objects.get(pk=user.id)
            except User.DoesNotExist or Account.DoesNotExist:
                return Response(
                    {"detail": "No existe el usuario"}, status=status.HTTP_404_NOT_FOUND
                )

            serializerAdmin = UserSerializer(admin, data=request.data)
            serializerAccount = AccountSerializer(
                account,
                data={
                    "first_name": request.data.get("first_name"),
                    "last_name": request.data.get("last_name"),
                },
            )

            # Valida los datos del serializer
            if serializerAdmin.is_valid() and serializerAccount.is_valid():
                # Guarda los datos actualizados en la base de datos
                serializerAdmin.save()
                serializerAccount.save()
                return Response(
                    {"mensaje": "Información actualizada correctamente"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"detail": "Ocurrió un error con los datos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateOther(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]

    def put(self, request):
        try:
            user_id = request.data.get("user_id")

            try:
                user = User.objects.get(pk=user_id, user_id__is_superuser=False)
                account = Account.objects.get(pk=user.id)
            except User.DoesNotExist or Account.DoesNotExist:
                return Response(
                    {"detail": "No existe el usuario"}, status=status.HTTP_404_NOT_FOUND
                )

            serializerUser = UserSerializer(user, data=request.data)
            serializerAccount = AccountSerializer(
                account,
                data={
                    "first_name": request.data.get("first_name"),
                    "last_name": request.data.get("last_name"),
                },
            )

            # Valida los datos del serializer
            if serializerUser.is_valid() and serializerAccount.is_valid():
                # Guarda los datos actualizados en la base de datos
                serializerUser.save()
                serializerAccount.save()
                return Response(
                    {"mensaje": "Información actualizada correctamente"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"detail": "Ocurrió un error con los datos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
