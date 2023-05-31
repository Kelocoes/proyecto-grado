from rest_framework import generics, permissions
from rest_framework.response import Response

from AppBack.models import Results, Results_Medic_Patient

from .serializer import ResultsMedicPatientSerializer, ResultsSerializer


class GetResultsByDoctor(generics.ListAPIView):
    serializer_class = ResultsMedicPatientSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, id_medic):
        return Results_Medic_Patient.objects.filter(user=id_medic)

    def get(self, request):
        rows = self.get_queryset(request.data["user_id"])

        serialized_rows = self.serializer_class(rows, many=True)
        return Response(serialized_rows.data)


class GetResultsWithoutRegistration(generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Results.objects.exclude(
        results_medic_patient__result_id__isnull=False
    ).order_by("-date")
