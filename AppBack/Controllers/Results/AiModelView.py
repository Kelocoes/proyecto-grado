from datetime import date

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from AppBack.models import Patient, Results, Results_Medic_Patient

from ..Cypher.encrypt import CustomAesRenderer
from .ia_model import IAModel
from .serializer import ResultsSerializer


class ModelApi(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ia_model = IAModel()

    serializer_class = ResultsSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomAesRenderer]

    def post(self, request):
        try:
            prediction = self.ia_model.predict(request.data)

            if prediction["prediction"] != "error":
                results = Results.objects.create(
                    date=date.today().strftime("%Y-%m-%d"),
                    age=request.data["age"],
                    sex=request.data["sex"],
                    weight=request.data["weight"],
                    height=request.data["height"],
                    diabetes=request.data["diabetes"],
                    systolic=request.data["systolic"],
                    diastolic=request.data["diastolic"],
                    cholesterol=request.data["cholesterol"],
                    hdl=request.data["hdl"],
                    ldl=request.data["ldl"],
                    triglycerides=request.data["triglycerides"],
                    smoking=request.data["smoking"],
                    background=request.data["background"],
                    estimation=prediction["prediction"],
                )
                results.save()

                if request.data["registered"]:
                    results_medic_patient = Results_Medic_Patient.objects.create(
                        patient_id=request.data["patient_id"],
                        result_id=results.pk,
                        user_id=request.data["user_id"],
                    )
                    results_medic_patient.save()

                    Patient.objects.filter(pk=request.data["patient_id"]).update(
                        actual_estimation=prediction["prediction"]
                    )

            return Response(prediction)
        except Exception:
            return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
