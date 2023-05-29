"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppBack.Controllers.Admin.adminViews import (
    GetAdmin
)

from AppBack.Controllers.Account.accountViews import (
    isActive,
    ChangeStatus
)

from AppBack.Controllers.Medic.medicViews import (
    GetAllMedics,
    GetMedic
)

from AppBack.Controllers.Patient.patientViews import (
    GetAllPatients,
    GetPatient
)

from AppBack.Controllers.Results.AiModelView import (
    ModelApi
)

from AppBack.Controllers.Results.resultsView import (
    GetResultsByDoctor,
    GetResultsWithoutRegistration
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #Account
    path('api/account/isActive', isActive.as_view()),
    path('api/account/update/status/<str:pk>', ChangeStatus.as_view()),
    #Admin
    path('api/admin/get/<str:pk>', GetAdmin.as_view()),
    #Medic
    path('api/medic/get/all', GetAllMedics.as_view()),
    path('api/medic/get/<str:pk>', GetMedic.as_view()),
    # Patient
    path('api/patient/get/all', GetAllPatients.as_view()),
    path('api/patient/get/<int:pk>', GetPatient.as_view()),
    # Results
    path('api/results/model/generate', ModelApi.as_view()),
    path('api/results/get/byDoctor', GetResultsByDoctor.as_view()),
    path('api/results/get/noregister', GetResultsWithoutRegistration.as_view())

]
