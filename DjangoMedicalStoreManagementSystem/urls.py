"""DjangoMedicalStoreManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.urls.conf import include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from DjangoMedicalApp import views
from DjangoMedicalApp.views import CompanyNameViewSet, CompanyOnlyViewSet, EmployeeBankByEIDViewSet, EmployeeSalaryByEIDViewSet, MedicineNameViewSet, MedicineViewSet

router=routers.DefaultRouter()
router.register("company",views.CompanyViewSet,basename="company")
router.register("companybank",views.CompanyBankViewSet,basename="companybank")
router.register("medicine",views.MedicineViewSet,basename="medicine")
router.register("companyaccount",views.CompanyAccountViewset,basename="companyaccount")
router.register("employee",views.EmployeeViewSet,basename="employee")
router.register("employee_all_bank",views.EmployeeBankViewSet,basename="employee_all_bank")
router.register("employee_all_salary",views.EmployeeSalaryViewSet,basename="employee_all_salary")
router.register("generate_bill",views.GenerateBillViewSet,basename="generate_bill")
router.register("customer_request",views.CustomerRequestViewSet,basename="customer_request")
router.register("home_api",views.HomeApiViewSet,basename="home_api")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/gettoken/',TokenObtainPairView.as_view(),name="gettoken"),
    path('api/refresh_token/',TokenRefreshView.as_view(),name="refresh_token"),
    path('api/companybyname/<str:name>',CompanyNameViewSet.as_view(),name="companybyname"),
    path('api/medicinebyname/<str:name>',MedicineNameViewSet.as_view(),name="medicinebyname"),
    path('api/companyonly/',CompanyOnlyViewSet.as_view(),name="companyonly"),
    path('api/employee_bank_byid/<str:employee_id>',EmployeeBankByEIDViewSet.as_view(),name="employee_bank_byid"),
    path('api/employee_salary_byid/<str:employee_id>',EmployeeSalaryByEIDViewSet.as_view(),name="employee_salary_byid"),
]
