from django.contrib.auth.models import User as Account
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import User

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import MedicAccountSerializer, MedicSerializer


class CreateMedic(APIView):
    serializer_class = MedicAccountSerializer
    permission_classes = [permissions.AllowAny]
    # renderer_classes = [CustomAesRenderer]

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            email = request.data.get("email")
            city = request.data.get("city")
            cellphone = request.data.get("cellphone")
            id = request.data.get("id")
            id_type = request.data.get("id_type")

            if (
                Account.objects.filter(username=username).exists()
                or Account.objects.filter(email=email).exists()
            ):
                raise Exception(
                    "Ya existe un usuario con ese nombre de usuario o correo"
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
                id=id,
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
    serializer_class = MedicSerializer
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            id = user.id

            user = User.objects.get(pk=id)
            serializer = MedicSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAllMedics(generics.ListAPIView):
    serializer_class = MedicSerializer
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]
    queryset = User.objects.exclude(user_id__is_superuser=True)
