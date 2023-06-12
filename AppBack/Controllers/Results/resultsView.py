from rest_framework import generics, permissions, status
from rest_framework.response import Response

from AppBack.models import Results, Results_Medic_Patient

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import ResultsMedicPatientSerializer, ResultsSerializer


class GetResultsByDoctor(generics.ListAPIView):
    serializer_class = ResultsMedicPatientSerializer
    permission_classes = [permissions.AllowAny]
    # renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            if user.is_superuser:
                rows = Results_Medic_Patient.objects.all()
            else:
                rows = Results_Medic_Patient.objects.filter(user_id=user.id)
            serialized_rows = ResultsMedicPatientSerializer(rows, many=True)
            return Response(serialized_rows.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "Hubo un error", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetResultsWithoutRegistration(generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [permissions.IsAdminUser]
    # renderer_classes = [CustomAesRenderer]
    queryset = Results.objects.exclude(
        results_medic_patient__result_id__isnull=False
    ).order_by("-date")
