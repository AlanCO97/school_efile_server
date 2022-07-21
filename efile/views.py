import logging
from efile.models import Address, Efile, Student, Tutor
from efile.serializers import AddressSerializer, StudentSerializer, TutorSerializer
from efile.utils.efile_handler import EfileHandler
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db import transaction
from school_config.models import EfileConfig, Employee
from utils.permissions.permissions import validate_rol
from utils.utils import add_field_to_efile


log = logging.getLogger(__name__)

class Students(APIView):

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404
    
    def get(self, request):
        students = Student.objects.all()

        student_serializer = StudentSerializer(students, many=True)
        if student_serializer.data:
            return Response(student_serializer.data)
        raise Http404

    def post(self, request):
        try:
            with transaction.atomic():
                employee: Employee = Employee.objects.get(user=request.user)

                student_serializer = None

                is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion", "Secretaria"])

                if not is_rol_valid:
                    return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)
                
                efile_handler = EfileHandler()
                efile_config: EfileConfig = efile_handler.get_current_efile_config()
                info = request.data.copy()
                info['is_active'] = True
                student_serializer = StudentSerializer(data=info)
                if student_serializer.is_valid():
                    student_serializer.save()
                    new_student = self.get_object(pk=student_serializer.data.get('id'))
                    is_saved, e = efile_handler.create_efile(efile_config=efile_config, student=new_student, employee=employee)
                    if not is_saved:
                        raise Exception(e)
                    return Response(data=student_serializer.data)
                return Response(data=student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response(data={"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk=pk)

        try:
            student_serializer = StudentSerializer(student)
            if student_serializer.data:
                return Response(student_serializer.data)
            raise Exception("No se pudo obtener la informacion del estudiante")
        except Exception as e:
            return Response(data={"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, pk):
        student = self.get_object(pk=pk)

        try:
            with transaction.atomic():
                employee: Employee = Employee.objects.get(user=request.user)

                student_serializer = None

                is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion", "Secretaria"])

                if not is_rol_valid:
                    return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)
                
                info = request.data.copy()
                info['is_active'] = True
                student_serializer = StudentSerializer(student, data=info)
                if student_serializer.is_valid():
                    student_serializer.save()
                    return Response(data=student_serializer.data)
                return Response(data=student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        student: Student = self.get_object(pk=pk)
        if student.is_active:
            student.is_active = False
            student.save()
            return Response(data={"msg": f"El estudiante se ha dado de baja el estudiante {student.complete_name()}"})
        return Response(data={"msg": f"El alumno {student.complete_name()} ya habia sido desactivado"}, status=status.HTTP_400_BAD_REQUEST)

class Tutors(APIView):
    
    def get_object(self, pk):
        try:
            return Tutor.objects.get(pk=pk)
        except Tutor.DoesNotExist:
            raise Http404
    
    def get(self, request):
        tutors = Tutor.objects.select_related('address').all()

        tutor_serializer = TutorSerializer(tutors, many=True)

        if tutor_serializer.data:
            return Response(data=tutor_serializer.data)

        if not tutor_serializer.data:
            return Response(data={"msg":"No hay tutores registrados"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={"msg":"Hubo un problema al encontrar los tutores"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data: dict = request.data.copy()
        efile_id = data.pop('efile_id', 0)[0]
        efile: Efile = Efile.objects.filter(pk=efile_id).first()

        if not efile:
            raise Http404

        try:
            with transaction.atomic():
                employee: Employee = Employee.objects.get(user=request.user)

                is_rol_valid: bool = validate_rol(employee=employee, need_rol=["Direccion", "Secretaria"])

                if not is_rol_valid:
                    return Response(data={'msg': 'Parece que no tienes permisos para realizar la operacion'}, status=status.HTTP_403_FORBIDDEN)
                
                #1. Primero guardar el address
                address_info = {
                    "street": data.pop('street', None)[0],
                    "no_int": data.pop('no_int', None)[0],
                    "no_ext": data.pop('no_ext', None)[0],
                    "phone_number": data.pop('phone_number', None)[0],
                    "sepomex_catalog": data.pop('sepomex_catalog', None)[0]
                }
                address_serializer = AddressSerializer(data=address_info)
                if address_serializer.is_valid():
                    address_serializer.save()
                    new_address = Address.objects.select_related('sepomex_catalog').get(pk=address_serializer.data.get('id')).pk
                    data['address'] = new_address
                    type_of_contact: str = data.pop('type', '')[0]
                    tutor_serializer = TutorSerializer(data=data)
                    if tutor_serializer.is_valid():
                        tutor_serializer.save()
                        #agregar el tutor al expediente
                        new_tutor = Tutor.objects.get(id=tutor_serializer.data.get('id'))
                        success, error = add_field_to_efile(model=Efile, field_name=type_of_contact, value=new_tutor, instance=efile)
                        breakpoint()
                        raise Exception('error')
                        if success:
                             return Response(data=tutor_serializer.data)
                        raise Exception(error)
                       
                    return Response(data=tutor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)                    
                return Response(data=address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(data={"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)