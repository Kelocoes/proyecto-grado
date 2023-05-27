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
    isActive
)

from AppBack.Controllers.Medic.medicViews import (
    GetAllMedics,
    GetMedic
)

from AppBack.Controllers.Patient.patientViews import (
    GetAllPatients,
    GetPatient
)

from AppBack.Controllers.Results.AiModelview import (
    ModelApi
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/isActive', isActive.as_view()),
    path('api/admin/get/<str:pk>', GetAdmin.as_view()),
    path('api/medic/get/all', GetAllMedics.as_view()),
    path('api/medic/get/<str:pk>', GetMedic.as_view()),
    path('api/patient/get/all', GetAllPatients.as_view()),
    path('api/patient/get/<int:pk>', GetPatient.as_view()),
    path('api/results/model/generate', ModelApi.as_view())

]
