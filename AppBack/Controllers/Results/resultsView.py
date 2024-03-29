import datetime

from django.db.models import Avg, Count, Max, Min, OuterRef, Q, Subquery
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

    def get(self, request):
        try:
            queryset = Results.objects.exclude(
                resultsmedicpatient__result_id__isnull=False
            ).order_by("-date")
            serialized_rows = ResultsSerializer(queryset, many=True)
            return Response(
                {
                    "detail": "Información de no registros obtenida",
                    "results": serialized_rows.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e), "results": {}}, status=status.HTTP_400_BAD_REQUEST
            )


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
                    "detail": "Información por mes obtenida",
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
                keyfilter = Q()
            else:
                keyfilter = Q(resultsmedicpatient__user_id=user.id)

            field_list = ["sex", "diabetes", "smoking", "background"]

            for field in field_list:
                querys.append(
                    Results.objects.filter(keyfilter)
                    .values(field)
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
                    "detail": "Información por categoría obtenida",
                    "results": {"labels": labels, "values": values},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e), "results": {"labels": [], "values": []}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetScatterPatients(generics.ListAPIView):
    serializer_class = ResultsMedicPatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            labels = []
            values = []
            subquery = (
                ResultsMedicPatient.objects.filter(patient_id=OuterRef("patient_id"))
                .order_by("-result__date")
                .values("result__estimation")[:1]
            )
            query = (
                ResultsMedicPatient.objects.filter(user_id=user.id)
                .values("patient_id")
                .annotate(max_date=Max("result__date"), estimation=Subquery(subquery))
                .order_by("patient_id")
            )
            for rows in query:
                labels.append(rows["patient_id"])
                values.append(rows["estimation"])

            return Response(
                {
                    "detail": "Información por paciente obtenida",
                    "results": {"labels": labels[:100], "values": values[:100]},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e), "results": {"labels": [], "values": []}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AvgNumericResults(generics.ListAPIView):
    serializer_class = ResultsMedicPatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            results = []
            if user.is_superuser:
                keyfilter = Q()
            else:
                keyfilter = Q(resultsmedicpatient__user_id=user.id)

            field_names = [
                "age",
                "weight",
                "height",
                "systolic",
                "diastolic",
                "cholesterol",
                "hdl",
                "ldl",
                "triglycerides",
            ]
            query_avgs = {}
            for field_name in field_names:
                queryset = (
                    Results.objects.filter(keyfilter)
                    .values("quartil")
                    .annotate(Avg(field_name))
                    .order_by("quartil")
                )
                query_avgs[field_name] = queryset

            quartil_list = list(
                Results.objects.filter(keyfilter)
                .values_list("quartil", flat=True)
                .distinct()
                .order_by("quartil")
            )
            for i in range(len(quartil_list)):
                row = []
                row.append(quartil_list[i])
                for field_name in field_names:
                    row.append(
                        round(query_avgs[field_name][i][field_name + "__avg"], 2)
                    )
                results.append(row)

            return Response(
                {"detail": "Promedios generados correctamente", "results": results},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e), "results": []},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DataForTraining(generics.ListAPIView):
    serializer_class = ResultsMedicPatientSerializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            subquery = ResultsMedicPatient.objects.filter(
                patient_id=OuterRef("patient_id")
            )
            last_result_id_subquery = (
                subquery.values("patient_id")
                .annotate(max_id=Min("result_id"))
                .values("max_id")[:1]
            )

            query = ResultsMedicPatient.objects.filter(
                result_id__in=Subquery(last_result_id_subquery)
            )

            serialized_rows = ResultsMedicPatientSerializer(query, many=True)

            return Response(
                {
                    "detail": "Información por paciente obtenida",
                    "results": serialized_rows.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e), "results": []},
                status=status.HTTP_400_BAD_REQUEST,
            )
