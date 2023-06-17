import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import User as Account
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import AccountSerializer, AccountStatusSerializer, EmailSerializer

load_dotenv()

SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
SENDER_PASS = os.getenv("SENDER_PASS")


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
                return Response(
                    {"detail": "Usuario no encontrado"},
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
    # renderer_classes = [CustomAesRenderer]

    def put(self, request):
        try:
            user = request.user
            new_password = request.data.get("password")
            try:
                account = Account.objects.get(pk=user.id)
            except Account.DoesNotExist:
                return Response(
                    {"detail": "Usuario no encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            account.set_password(new_password)
            account.save()
            return Response(
                {"detail": "Contraseña actualizada exitosamente"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendEmailPassword(APIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]
    # renderer_classes = [CustomAesRenderer]

    def post(self, request):
        try:
            username = request.data.get("username")
            email = request.data.get("email")

            try:
                account = Account.objects.get(username=username, email=email)
            except Account.DoesNotExist:
                return Response(
                    {"detail": "Usuario no encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            token = Token.objects.get(user=account)
            mail_content = (
                """
            Hola,
            Parece que deseas cambiar tu contraseña, ingresa al siguiente link y sigue los pasos
            https://riesgo-cardiovascular-uv.me/changepassword/%s
            Atentamente: RiesgoUV """
                % token
            )
            # The mail addresses and password
            sender_address = SENDER_ADDRESS
            sender_pass = SENDER_PASS
            receiver_address = account.email
            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = receiver_address
            message["Subject"] = "Actualiza tu contraseña. RiesgoUV"  # The subject line
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "plain"))
            # Create SMTP session for sending the mail
            session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(
                sender_address, sender_pass
            )  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            return Response(
                {"detail": "Email enviado correctamente"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
