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
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetResultsWithoutRegistration(generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [CustomAesRenderer]

    queryset = Results.objects.exclude(
        resultsmedicpatient__result_id__isnull=False
    ).order_by("-date")
