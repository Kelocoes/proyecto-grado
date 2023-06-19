from django.contrib import admin
from django.urls import path

from AppBack.Controllers.Account.accountViews import (
    ChangePassword,
    ChangeStatus,
    CheckPassword,
    IsActive,
    SendEmailPassword,
)
from AppBack.Controllers.Admin.adminViews import GetAdmin, UpdateAdmin, UpdateOther
from AppBack.Controllers.Captcha.CaptchaViews import GetCaptchaResponse
from AppBack.Controllers.Medic.medicViews import (
    CreateMedic,
    GetAllMedics,
    GetMedic,
    UpdateMedic,
)
from AppBack.Controllers.Patient.patientViews import (
    CreatePatient,
    DeletePatient,
    GetAllPatients,
    GetPatient,
    UpdatePatient,
)
from AppBack.Controllers.Results.AiModelView import ModelApi
from AppBack.Controllers.Results.resultsView import (
    GetResultsByDoctor,
    GetResultsWithoutRegistration,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Captcha
    path("api/captcha/getResponse", GetCaptchaResponse.as_view()),
    # Account
    path("api/account/isActive", IsActive.as_view()),
    path("api/account/update/status", ChangeStatus.as_view()),
    path("api/account/checkpassword", CheckPassword.as_view()),
    path("api/account/changepassword", ChangePassword.as_view()),
    path("api/account/sendemailpassword", SendEmailPassword.as_view()),
    # Admin
    path("api/admin/get", GetAdmin.as_view()),
    path("api/admin/update/self", UpdateAdmin.as_view()),
    path("api/admin/update/other", UpdateOther.as_view()),
    # Medic
    path("api/medic/create", CreateMedic.as_view()),
    path("api/medic/get", GetMedic.as_view()),
    path("api/medic/get/all", GetAllMedics.as_view()),
    path("api/medic/update/self", UpdateMedic.as_view()),
    # Patient
    path("api/patient/create", CreatePatient.as_view()),
    path("api/patient/get", GetPatient.as_view()),
    path("api/patient/get/all", GetAllPatients.as_view()),
    path("api/patient/update", UpdatePatient.as_view()),
    path("api/patient/delete", DeletePatient.as_view()),
    # Results
    path("api/results/model/generate", ModelApi.as_view()),
    path("api/results/get/byDoctor", GetResultsByDoctor.as_view()),
    path("api/results/get/noregister", GetResultsWithoutRegistration.as_view()),
]
