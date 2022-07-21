from rest_framework import serializers
from django.contrib.auth.models import User
from school_config.models import AcademicYear, EfileConfig, Employee, Position, SchoolConfig

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class EfileConfigSerializer(serializers.ModelSerializer):
    academic_year = serializers.SerializerMethodField()
    school =  serializers.SerializerMethodField()
    
    class Meta:
        model = EfileConfig
        fields = '__all__'
    
    def get_academic_year(self, obj):
        if obj.academic_year:
            academic_year = AcademicYear.objects.filter(id=obj.academic_year.id)
            if academic_year:
                response = {}
                for year in academic_year:
                    response['id'] = year.id
                    response['init'] = year.init_day
                    response['end'] = year.end_day
                
                return response

        return {}
    
    def get_school(self, obj):
        if obj.school:
            schools = SchoolConfig.objects.filter(id=obj.school.id)
            if schools:
                response = {}
                for school in schools:
                    response['id'] = school.id
                    response['name'] = school.school_name
                
                return response
        return {}

class EmployeeSerializer(serializers.ModelSerializer):
    # school =  serializers.SerializerMethodField()
    # position =  serializers.SerializerMethodField()
    # user =  serializers.SerializerMethodField()
    school =  serializers.PrimaryKeyRelatedField(queryset=SchoolConfig.objects.all(), many=False)
    position =  serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), many=False)
    user =  serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)

    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance: Employee):
        
        return {
            "id": instance.id,
            "name": instance.name,
            "father_lastname": instance.father_lastname,
            "mother_lastname": instance.mother_lastname,
            "curp": instance.curp,
            "birthDate": instance.birthDate,
            "is_active": instance.is_active,
            "email": instance.email,
            "position": {
                "position": instance.position.id,
                "name": instance.position.name
            },
            "user": {
                "id": instance.user.id,
                "name": instance.user.username
            },
            "school": {
                "id": instance.school.id,
                "name": instance.school.school_name
            }
        }
    
    # def get_school(self, obj):
    #     if obj.school:
    #         schools = SchoolConfig.objects.filter(id=obj.school.id)
    #         if schools:
    #             response = {}
    #             for school in schools:
    #                 response['id'] = school.id
    #                 response['name'] = school.school_name
                
    #             return response
    #     return {}

    # def get_position(self, obj):
    #     if obj.position:
    #         positions = Position.objects.filter(id=obj.position.id)
    #         if positions:
    #             response = {}
    #             for position in positions:
    #                 response['id'] = position.id
    #                 response['name'] = position.name
                
    #             return response
    #     return {}

    # def get_user(self, obj):
    #     if obj.user:
    #         users = User.objects.filter(id=obj.user.id)
    #         if users:
    #             response = {}
    #             for user in users:
    #                 response['id'] = user.id
    #                 response['name'] = user.first_name
                
    #             return response
    #     return {}

    # def create(self, validated_data):
    #     position_id = self.context.get('position')
    #     user_id = self.context.get('user'),
    #     school_id = self.context.get('school')
    #     return Employee.objects.create(
    #         position_id=position_id,
    #         user_id=user_id[0],
    #         school_id=school_id,
    #         **validated_data
    #     )