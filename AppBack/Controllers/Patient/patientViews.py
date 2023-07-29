from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import MedicPatient, Patient

from ..Cypher.encrypt import CustomAesRenderer
from .serializer import MedicPatientSerializer, PatientSerializer


class CreatePatient(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    queryset = Patient.objects.all()

    def post(self, request):
        try:
            cypher_class = CustomAesRenderer()
            request.data.update(cypher_class.decryptJson(request.data))
            request.data.pop("ciphertext")
            user = request.user

            patient = Patient.objects.create(
                patient_id=request.data.get("patient_id"),
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                birth_date=request.data.get("birth_date"),
                city=request.data.get("city"),
                address=request.data.get("address"),
                blood_type=request.data.get("blood_type"),
                cellphone=request.data.get("cellphone"),
            )

            patient.save()

            medicpatient = MedicPatient.objects.create(
                patient_id=patient.pk, user_id=user.id
            )

            medicpatient.save()

            return Response(
                {"detail": "Se creo correctamente"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetPatient(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            cypher_class = CustomAesRenderer()
            request.data.update(cypher_class.decryptJson(request.data))
            request.data.pop("ciphertext")
            user = request.user
            if not (user.is_superuser) and (
                not (
                    MedicPatient.objects.filter(
                        patient_id=request.data.get("patient_id"), user_id=user.id
                    ).exists()
                )
            ):
                return Response(
                    {"detail": "Usuario no encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            patient = Patient.objects.get(pk=request.data.get("patient_id"))
            serializer = PatientSerializer(patient)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAllPatients(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def get(self, request):
        try:
            user = request.user
            if user.is_superuser:
                patients = MedicPatient.objects.all().order_by("patient_id")
                serializer = MedicPatientSerializer(patients, many=True)
            else:
                patients = Patient.objects.filter(
                    medicpatient__user_id=user.id
                ).order_by("patient_id")
                serializer = PatientSerializer(patients, many=True)
            return Response(
                {
                    "detail": "Pacientes obtenidos exitosamente",
                    "results": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePatient(APIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def put(self, request):
        try:
            user = request.user
            try:
                cypher_class = CustomAesRenderer()
                request.data.update(cypher_class.decryptJson(request.data))
                request.data.pop("ciphertext")
                if user.is_superuser:
                    patient = Patient.objects.get(pk=request.data.get("patient_id"))
                else:
                    patient = Patient.objects.get(
                        pk=request.data.get("patient_id"),
                        medicpatient__user_id=user.id,
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
    renderer_classes = [CustomAesRenderer]

    def delete(self, request):
        try:
            cypher_class = CustomAesRenderer()
            request.data.update(cypher_class.decryptJson(request.data))
            request.data.pop("ciphertext")
            user = request.user
            try:
                if user.is_superuser:
                    patient = Patient.objects.get(pk=request.data.get("patient_id"))
                else:
                    patient = Patient.objects.get(
                        pk=request.data.get("patient_id"),
                        medicpatient__user_id=user.id,
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
