from django.contrib.auth.models import User as Account
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import User

from .serializer import (
    AccountMedicGetSerializer,
    AccountMedicSerializer,
    AccountsSomeFieldsSerializer2,
    UserSerializer,
)


class CreateMedic(APIView):
    serializer_class = AccountMedicSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            email = request.data.get("email")
            city = request.data.get("city")
            cellphone = request.data.get("cellphone")
            medic_id = request.data.get("id")
            id_type = request.data.get("id_type")

            if (
                Account.objects.filter(username=username).exists()
                or Account.objects.filter(email=email).exists()
            ):
                return Response(
                    {
                        "detail": "Ya existe un usuario con ese nombre de usuario o correo"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            account = Account.objects.create_user(
                username=username,
                password=password,
                is_staff=False,
                is_active=True,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            User.objects.create(
                user_id=account,
                id=medic_id,
                id_type=id_type,
                first_name=first_name,
                last_name=last_name,
                city=city,
                cellphone=cellphone,
            )

            token = Token.objects.create(user=account)

            return Response(
                {"detail": "Usuario creado correctamente", "token": token.key},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetMedic(APIView):
    serializer_class = AccountMedicGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            user = User.objects.get(pk=user.id)
            serializer = AccountMedicGetSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAllMedics(generics.ListAPIView):
    serializer_class = AccountMedicGetSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        try:
            queryset = User.objects.exclude(user_id__is_superuser=True).order_by(
                "user_id"
            )
            serializer = self.serializer_class(queryset, many=True)

            return Response(
                {
                    "detail": "Médicos obtenidos exitosamente",
                    "results": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateMedic(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        try:
            user = request.user

            try:
                medic = User.objects.get(pk=user.id)
                account = Account.objects.get(pk=user.id)
            except (User.DoesNotExist, Account.DoesNotExist):
                return Response(
                    {"detail": "No existe el usuario"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer_medic = UserSerializer(medic, data=request.data)
            serializer_account = AccountsSomeFieldsSerializer2(
                account,
                data={
                    "first_name": request.data.get("first_name"),
                    "last_name": request.data.get("last_name"),
                },
            )
            # Valida los datos del serializer
            if serializer_medic.is_valid() and serializer_account.is_valid():
                # Guarda los datos actualizados en la base de datos
                serializer_medic.save()
                serializer_account.save()
                return Response(
                    {"detail": "Información actualizada correctamente"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"detail": "Ocurrió un error con los datos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
