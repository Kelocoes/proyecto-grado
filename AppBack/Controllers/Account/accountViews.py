from django.contrib.auth.models import User as Account
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AccountSerializer, AccountStatusSerializer


class isActive(APIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [CustomAesRenderer]

    def get(self, request):
        user = request.user
        is_active = user.is_active
        return Response({"detail": is_active}, status=status.HTTP_200_OK)


class ChangeStatus(APIView):
    serializer_class = AccountStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]

    def put(self, request):
        try:
            token = request.data.get("token")
            token_obj = Token.objects.get(pk=token)
            user_id = token_obj.user_id
            is_active = request.data.get("is_active")
            account = Account.objects.get(pk=user_id)
            account.is_active = is_active
            account.save()
            return Response(
                {"detail": "Estado de activo actualizado"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckPassword(APIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
    # renderer_classes = [CustomAesRenderer]

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            try:
                account = Account.objects.get(username=username)
            except Exception:
                raise Exception("Usuario no encontrado")

            if not (account.is_active):
                raise Exception("Usuario desactivado")

            if account is not None and account.check_password(password):
                token = Token.objects.get(user=account)
                account.last_login = timezone.now()
                account.save()
                return Response(
                    {"detail": "Usuario ingresado correctamente", "token": token.key},
                    status=status.HTTP_200_OK,
                )

            raise Exception("Contraseña incorrecta")

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
