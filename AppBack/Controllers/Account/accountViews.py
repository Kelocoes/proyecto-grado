import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import User as Account
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AccountSerializer, AccountStatusSerializer, EmailSerializer

load_dotenv()

SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
SENDER_PASS = os.getenv("SENDER_PASS")
FRONT_URL = os.getenv("FRONT_URL")
NOT_FOUND_MESSAGE = "Usuario no encontrado"


class IsActive(APIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        is_active = user.is_active
        is_admin = user.is_superuser
        return Response(
            {"detail": str(is_active), "is_admin": is_admin}, status=status.HTTP_200_OK
        )


class ChangeStatus(APIView):
    serializer_class = AccountStatusSerializer
    permission_classes = [permissions.IsAdminUser]

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

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            account = (
                Account.objects.filter(username=username).first()
                or Account.objects.filter(email=username).first()
            )

            if not (account):
                return Response(
                    {"detail": NOT_FOUND_MESSAGE},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not (account.is_active):
                return Response(
                    {"detail": "Usuario desactivado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if account is not None and account.check_password(password):
                token = Token.objects.get(user=account)
                account.last_login = timezone.now()
                account.save()
                return Response(
                    {"detail": "Usuario ingresado correctamente", "token": token.key},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"detail": "Contraseña incorrecta"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePassword(APIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        try:
            user = request.user
            new_password = request.data.get("password")
            secret = request.data.get("secret")

            try:
                account = Account.objects.get(pk=user.id)
            except Account.DoesNotExist:
                return Response(
                    {"detail": NOT_FOUND_MESSAGE},
                    status=status.HTTP_404_NOT_FOUND,
                )

            cypher_class = CustomAesRenderer()
            decrypted_secret = cypher_class.decryptString(secret)

            if decrypted_secret == str(datetime.now().date()):
                account.set_password(new_password)
                account.save()
                return Response(
                    {"detail": "Contraseña actualizada exitosamente"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "detail": "Link vencido, realiza los pasos "
                    "nuevamente para actualizar tu contraseña"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendEmailPassword(APIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            username = request.data.get("username")

            account = (
                Account.objects.filter(username=username).first()
                or Account.objects.filter(email=username).first()
            )
            if not (account):
                return Response(
                    {"detail": NOT_FOUND_MESSAGE},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not (account.is_active):
                return Response(
                    {"detail": "Usuario desactivado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = Token.objects.get(user=account)
            cypher_class = CustomAesRenderer()
            secret = cypher_class.encryptString(data=str(datetime.now().date()))
            mail_content = """
            Hola,
            Parece que deseas cambiar tu contraseña, ingresa al siguiente link y sigue los pasos:
            %s/#/changepassword/%s/%s
            Tienes el plazo de el día de hoy para realizar esta acción.

            Atentamente: RiesgoUV """ % (
                FRONT_URL,
                token,
                secret,
            )

            sender_address = SENDER_ADDRESS
            sender_pass = SENDER_PASS
            receiver_address = account.email
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = receiver_address
            message["Subject"] = "Actualiza tu contraseña. RiesgoUV"
            message.attach(MIMEText(mail_content, "plain"))
            session = smtplib.SMTP("smtp.gmail.com", 587)
            session.starttls()
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            return Response(
                {"detail": "Te hemos enviado un correo electrónico"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
