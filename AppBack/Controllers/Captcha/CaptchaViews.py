import json
import os

import requests
from dotenv import load_dotenv
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv()

CAPTCHA_SECRET_KEY = os.getenv("CAPTCHA_SECRET_KEY")


class GetCaptchaResponse(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            token = request.data.get("token")
            url = (
                "https://www.google.com/recaptcha/api/siteverify?secret=%s&response=%s"
                % (CAPTCHA_SECRET_KEY, token)
            )
            res = requests.post(url)
            return Response({"detail": json.loads(res.text)}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
