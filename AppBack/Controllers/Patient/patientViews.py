from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import Doctor_Patient, Patient

# from ..Cypher.encrypt import CustomAesRenderer
from .serializer import PatientSerializer


class CreatePatient(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [CustomAesRenderer]
    queryset = Patient.objects.all()

    def post(self, request):
        try:
            user = request.user

            patient = Patient.objects.create(
                patient_id=request.data.get("patient_id"),
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                birth_date=request.data.get("birth_date"),
                city=request.data.get("city"),
                address=request.data.get("address"),
                blood_type=request.data.get("blood_type"),
            )

            patient.save()

            doctor_patient = Doctor_Patient.objects.create(
                patient_id=patient.pk, user_id=user.id
            )

            doctor_patient.save()

            return Response(
                {"detail": "Se creo correctamente"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetPatient(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            if not (user.is_superuser) and (
                not (
                    Doctor_Patient.objects.filter(
                        patient_id=request.data.get("patient_id"), user_id=user.id
                    ).exists()
                )
            ):
                raise Exception("Elemento no encontrado")

            patient = Patient.objects.get(pk=request.data.get("patient_id"))
            serializer = PatientSerializer(patient)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAllPatients(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            if user.is_superuser:
                patients = Patient.objects.all()
            else:
                patients = Patient.objects.filter(doctor_patient__user_id=user.id)

            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePatient(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [CustomAesRenderer]

    def put(self, request):
        try:
            user = request.user
            try:
                if user.is_superuser:
                    patient = Patient.objects.get(pk=request.data.get("patient_id"))
                else:
                    patient = Patient.objects.get(
                        pk=request.data.get("patient_id"),
                        doctor_patient__user_id=user.id,
                    )
            except Patient.DoesNotExist:
                return Response(
                    {"detail": "No existe el paciente"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = PatientSerializer(patient, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"detail": "Se ha actualizado correctamente"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"detail": "Ocurrió un error con los datos"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeletePatient(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [CustomAesRenderer]

    def delete(self, request):
        try:
            user = request.user
            try:
                if user.is_superuser:
                    patient = Patient.objects.get(pk=request.data.get("patient_id"))
                else:
                    patient = Patient.objects.get(
                        pk=request.data.get("patient_id"),
                        doctor_patient__user_id=user.id,
                    )
            except Patient.DoesNotExist:
                return Response(
                    {"detail": "No existe el paciente"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            patient.delete()
            return Response(
                {"detail": "Se ha eliminado correctamente"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
