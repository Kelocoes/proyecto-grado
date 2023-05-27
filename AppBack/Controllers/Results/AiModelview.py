from rest_framework.views import APIView
from .serializer import ResultsSerializer
from rest_framework.response import Response
from datetime import date

from AppBack.models import Results, Results_Medic_Patient
from rest_framework import permissions
from .ia_model import IAModel

class ModelApi(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ia_model = IAModel()

    serializer_class = ResultsSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        prediction = self.ia_model.predict(request.data)

        if prediction["prediction"] != "error" and request.data["registered"] :
            results = Results(
                date= date.today().strftime("%Y-%m-%d"),
                age = request.data["age"],
                sex = request.data["sex"],
                weight = request.data["weight"],
                height = request.data["height"],
                diabetes = request.data["diabetes"],
                systolic = request.data["systolic"],
                diastolic = request.data["diastolic"],
                cholesterol = request.data["cholesterol"],
                hdl = request.data["hdl"],
                ldl = request.data["ldl"],
                triglycerides = request.data["triglycerides"],
                smoking = request.data["smoking"],
                background = request.data["background"],
                estimation= prediction["prediction"]
            )
            results.save()

            results_medic_patient = Results_Medic_Patient(
                patient_id = request.data["patient_id"],
                result_id = results.pk,
                user_id = request.data["user_id"],
            )
            results_medic_patient.save()




        return Response(prediction)
