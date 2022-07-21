import logging
from auth.serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from school_config.models import AcademicYear, EfileConfig, Employee, SchoolConfig
from school_config.serializers import AcademicYearSerializer, EfileConfigSerializer, EmployeeSerializer
from school_efile_server.settings import DEBUG
from utils.permissions.permissions import validate_rol

log = logging.getLogger(__name__)

class EfileConfiguration(APIView):

    def get(self, request):
        efile_config = EfileConfig.objects.select_related('academic_year', 'school').all()
        serializer = EfileConfigSerializer(efile_config, many=True)
        if serializer.data:
            return Response(data=serializer.data)
        return Response(data={'msg':'Hubo un error al obtener la configuracion'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        employee: Employee = Employee.objects.get(user=request.user)

        is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion"])

        if is_rol_valid:
            data = request.data.copy()
            with transaction.atomic():
                academic_year: AcademicYear = AcademicYear.objects.filter(id=data.get('academic_year'))

                if academic_year:
                    try:
                        efile_config = EfileConfig.objects.all().order_by('-id')
                        current_folio = efile_config.first().folio
                        new_folio = str(int(current_folio) + 1)
                        new_efile_config: EfileConfig = EfileConfig.objects.create(
                            folio = new_folio,
                            academic_year = academic_year.first(),
                            school = employee.school
                        )

                        new_efile_config.save()

                        return Response(data={'msg': 'La configuracion se creo con exito'})
                    except Exception as e:
                        log.info(str(e))
                        return Response(data={'msg': 'Hubo un error al guardar el registro'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(data={'msg': 'No se encontro la configuracion'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)

class EfileConfigurationDetail(APIView):
    def get_object(self, pk):
        try:
            return EfileConfig.objects.select_related('academic_year', 'school').get(pk=pk)
        except EfileConfig.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        efile_config = self.get_object(pk=pk)
     
        serializer = EfileConfigSerializer(efile_config)
        if serializer.data:
            return Response(data=serializer.data)
        return Response(data={'msg':'Hubo un error al obtener la configuracion'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

    def patch(self, request, pk):
        employee: Employee = Employee.objects.get(user=request.user)

        is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion"])

        if not is_rol_valid:
            return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)

        efile_config = self.get_object(pk=pk)
        serializer = EfileConfigSerializer(efile_config, data={"current_config":True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data={'msg':'Hubo un error al obtener la configuracion'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Employees(APIView):

    def get(self, request):
        employees = Employee.objects.select_related('position', 'user', 'school').all()
        serializer = EmployeeSerializer(employees, many=True)
        if serializer.data:
            return Response(data=serializer.data)
        return Response(data={'msg':'Hubo un error al obtener los usuarios'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        employee: Employee = Employee.objects.get(user=request.user)

        is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion", "Secretaria"])

        if is_rol_valid:
            data = request.data.copy()
            try:
                user = {
                    "username": data.get('username'),
                    "password": make_password(data.get('password')),
                    "first_name": data.get('name', ''),
                    "last_name": data.get('father_lastname', '') + data.get('father_lastname', ''),
                    "email": data.get('email', '')
                }

                employee_serializer = {}
                user_serializer = {}

                user_serializer = RegisterSerializer(data=user)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
                new_user = User.objects.get(username=user_serializer.data.get('username')).pk
                new_employee = {
                    "school": data.get('school'),
                    "position": data.get('position'),
                    "user": int(new_user),
                    "name": data.get('name'),
                    "father_lastname": data.get('father_lastname'),
                    "mother_lastname": data.get('mother_lastname'),
                    "curp": data.get('curp'),
                    "birthDate": data.get('birthDate'), #YYYY-MM-DD
                    "email": data.get('email')
                }
                employee_serializer = EmployeeSerializer(data=new_employee)
                employee_serializer.is_valid(raise_exception=True)
                employee_serializer.save()

                return Response(data={"msg":"El empleado se creo con exito"})
            except Exception as e:
                log.info(str(e))
                errors = None

                if user_serializer.errors and employee_serializer:
                    errors = user_serializer.errors.update(employee_serializer.errors)
                elif user_serializer.errors:
                    errors = user_serializer.errors
                else:
                    errors = employee_serializer.errors
                    new_user.delete()

                return Response(data={
                        "msg": "Hubo un error al guardar el empleado", 
                        "err": errors,
                        "exception": str(e) if DEBUG else ''
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)

class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.select_related('position', 'user', 'school').get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        employee = self.get_object(pk=pk)
        if employee:
            serializer = EmployeeSerializer(employee)
            if serializer.data:
                return Response(data=serializer.data)
            return Response(data={'msg':'Hubo un error al obtener el empleado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response(data={'msg':'No se encontro el empleado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, pk):
        employee: Employee = Employee.objects.get(user=request.user)

        is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion"])

        if not is_rol_valid:
            return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)
        
        employee_retrieve: Employee = self.get_object(pk=pk)

        # if not employee_retrieve.is_active:
        #     return Response(data={'msg': 'Parece que el empleado que intentas modificar no esta activo'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmployeeSerializer(employee_retrieve, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee: Employee = Employee.objects.get(user=request.user)

        is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion"])

        if not is_rol_valid:
            return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)
        
        employee_retrieve: Employee = self.get_object(pk=pk)

        if not employee_retrieve.is_active:
            return Response(data={'msg': 'Parece que el empleado ya esta inactivo'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmployeeSerializer(employee_retrieve, data={"is_active":False}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcademicYears(APIView):
    def get(self, request):
        academic_years: AcademicYear = AcademicYear.objects.all()

        serializer = AcademicYearSerializer(academic_years, many=True)
        if serializer.data:
            return Response(serializer.data)
        
        raise Http404
    
    def post(self, request):
        employee: Employee = Employee.objects.get(user=request.user)

        is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion"])

        if not is_rol_valid:
            return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AcademicYearSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            return Response(serializer.data)

class AcademicYearsDetail(APIView):
    def get_object(self, pk):
        try:
            return AcademicYear.objects.get(pk=pk)
        except AcademicYear.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        academic_years = self.get_object(pk=pk)
        if academic_years:
            serializer = AcademicYearSerializer(academic_years)
            if serializer.data:
                return Response(data=serializer.data)
            return Response(data={'msg':'Hubo un error al obtener el ciclo escolar'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response(data={'msg':'No se encontro el ciclo escolar'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        employee: Employee = Employee.objects.get(user=request.user)

        is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion"])

        if not is_rol_valid:
            return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)
        
        academic_years: AcademicYear = self.get_object(pk=pk)
        
        serializer = AcademicYearSerializer(academic_years, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)