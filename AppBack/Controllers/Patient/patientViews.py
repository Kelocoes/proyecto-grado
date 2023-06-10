from rest_framework import generics, permissions, status
from rest_framework.response import Response

from AppBack.models import Doctor_Patient, Patient

from ..Cypher.encrypt import CustomAesRenderer
from .serializer import PatientSerializer


class GetPatient(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]
    queryset = Patient.objects.all()


class GetAllPatients(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]
    queryset = Patient.objects.all()


class CreatePatient(generics.CreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]
    model = Patient

    def post(self, request):
        try:
            patient = Patient.objects.create(
                patient_id=request.data["patient_id"],
                name=request.data["name"],
                last_name=request.data["last_name"],
                birth_date=request.data["birth_date"],
                city=request.data["city"],
                address=request.data["address"],
                blood_type=request.data["blood_type"],
            )

            patient.save()

            doctor_patient = Doctor_Patient.objects.create(
                patient_id=patient.pk, user_id=request.data["user_id"]
            )

            doctor_patient.save()

            return Response(
                {"message": "Se creo correctamente"}, status=status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                {"message": "Error al crear usuario"},
                status=status.HTTP_400_BAD_REQUEST,
            )
