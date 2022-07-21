from django.urls import path
from .views import AcademicYears, AcademicYearsDetail, EfileConfiguration, EfileConfigurationDetail, EmployeeDetail, Employees

urlpatterns = [
    path('', EfileConfiguration.as_view(), name='all_config_file'),
     path('<int:pk>', EfileConfigurationDetail.as_view(), name='all_config_detail'),
    path('employee/', Employees.as_view(), name='employee_config'),
    path('employee/<int:pk>', EmployeeDetail.as_view(), name='employee_detail'),
    path('academicYears/', AcademicYears.as_view(), name='academic_years'),
    path('academicYears/<int:pk>', AcademicYearsDetail.as_view(), name='academic_years'),
]