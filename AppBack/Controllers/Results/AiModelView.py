from datetime import date

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import Doctor_Patient, Patient, Results, Results_Medic_Patient

from ..Cypher.encrypt import CustomAesRenderer
from .ia_model import IAModel
from .serializer import ResultsSerializer


class ModelApi(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ia_model = IAModel()

    serializer_class = ResultsSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [CustomAesRenderer]

    def post(self, request):
        try:
            prediction = self.ia_model.predict(request.data)

            if prediction["prediction"] != "error":
                results = Results.objects.create(
                    date=date.today().strftime("%Y-%m-%d"),
                    age=request.data.get("age"),
                    sex=request.data.get("sex"),
                    weight=request.data.get("weight"),
                    height=request.data.get("height"),
                    diabetes=request.data.get("diabetes"),
                    systolic=request.data.get("systolic"),
                    diastolic=request.data.get("diastolic"),
                    cholesterol=request.data.get("cholesterol"),
                    hdl=request.data.get("hdl"),
                    ldl=request.data.get("ldl"),
                    triglycerides=request.data.get("triglycerides"),
                    smoking=request.data.get("smoking"),
                    background=request.data.get("background"),
                    estimation=prediction.get("prediction"),
                )
                results.save()

                if request.data.get("registered"):
                    user = request.user

                    if (
                        user.is_superuser
                        or Doctor_Patient.objects.filter(
                            patient_id=request.data.get("patient_id"), user_id=user.id
                        ).exists()
                    ):
                        results_medic_patient = Results_Medic_Patient.objects.create(
                            patient_id=request.data.get("patient_id"),
                            result_id=results.pk,
                            user_id=user.id,
                        )
                        results_medic_patient.save()

                        Patient.objects.filter(
                            pk=request.data.get("patient_id")
                        ).update(actual_estimation=prediction["prediction"])
                    else:
                        return Response(
                            {
                                "detail": "Estas tratando de hacerle una estimación a un "
                                "paciente que no es tuyo"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            return Response(prediction)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
