import datetime

from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from AppBack.models import Results, ResultsMedicPatient

from ..Cypher.encrypt import CustomAesRenderer
from .serializer import ResultsMedicPatientSerializer, ResultsSerializer


class GetResultsByPatient(generics.ListAPIView):
    serializer_class = ResultsMedicPatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def post(self, request):
        try:
            cypher_class = CustomAesRenderer()
            request.data.update(cypher_class.decryptJson(request.data))
            request.data.pop("ciphertext")
            user = request.user
            patient_id = request.data.get("patient_id")
            print(patient_id)
            if user.is_superuser:
                rows = ResultsMedicPatient.objects.filter(patient_id=patient_id)
            else:
                rows = ResultsMedicPatient.objects.filter(
                    patient_id=patient_id, user_id=user.id
                )
            serialized_rows = ResultsMedicPatientSerializer(rows, many=True)
            return Response(
                {"detail": "Información obtenida", "results": serialized_rows.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e), "results": []}, status=status.HTTP_400_BAD_REQUEST
            )


class GetResultsWithoutRegistration(generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [CustomAesRenderer]

    queryset = Results.objects.exclude(
        resultsmedicpatient__result_id__isnull=False
    ).order_by("-date")


class GetResultsByMonth(generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            actual_year = datetime.date.today().year
            query = (
                Results.objects.filter(date__year=actual_year)
                .annotate(month=TruncMonth("date"))
                .values("month")
                .annotate(count=Count("result_id"))
                .order_by("month")
            )
            months = []
            amounts = []
            for rows in query:
                month = rows["month"].strftime("%B")
                amount = rows["count"]
                months.append(month)
                amounts.append(amount)
            return Response(
                {
                    "detail": "Información obtenida",
                    "results": {"months": months, "amounts": amounts},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e), "results": {}}, status=status.HTTP_400_BAD_REQUEST
            )


class GetResultsByCategory(generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user

            labels = [
                "",
                "",
                "Femenino",
                "Masculino",
                "Diabetes positivo",
                "Diabetes negativo",
                "Fumador",
                "No Fumador",
                "Antecedentes positivo",
                "Antecedentes negativo",
            ]
            values = [[0, 0]]
            querys = []
            if user.is_superuser:
                querys.append(
                    Results.objects.values("sex").annotate(count=Count("result_id"))
                )
                querys.append(
                    Results.objects.values("diabetes").annotate(
                        count=Count("result_id")
                    )
                )
                querys.append(
                    Results.objects.values("smoking").annotate(count=Count("result_id"))
                )
                querys.append(
                    Results.objects.values("background").annotate(
                        count=Count("result_id")
                    )
                )
            else:
                querys.append(
                    Results.objects.filter(resultsmedicpatient__user_id=user.id)
                    .values("sex")
                    .annotate(count=Count("result_id"))
                )
                querys.append(
                    Results.objects.filter(resultsmedicpatient__user_id=user.id)
                    .values("diabetes")
                    .annotate(count=Count("result_id"))
                )
                querys.append(
                    Results.objects.filter(resultsmedicpatient__user_id=user.id)
                    .values("smoking")
                    .annotate(count=Count("result_id"))
                )
                querys.append(
                    Results.objects.filter(resultsmedicpatient__user_id=user.id)
                    .values("background")
                    .annotate(count=Count("result_id"))
                )

            for cat in querys:
                amounts = []
                for type in cat:
                    amount = type["count"]
                    amounts.append(amount)
                values.append(amounts)

            return Response(
                {
                    "detail": "Información obtenida",
                    "results": {"datasets": labels, "values": values},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e), "results": {"datasets": [], "values": []}},
                status=status.HTTP_400_BAD_REQUEST,
            )
