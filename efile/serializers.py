from efile.models import Address, BloodType, InsuranceHealth, RelationshipType, SepomexCatalog, Student, Tutor
from rest_framework import serializers
from school_config.models import GradeGroupConfig, SchoolConfig
from school_efile_server.settings import HOST, MEDIA_URL
import os

class StudentSerializer(serializers.ModelSerializer):
    insurance_health = serializers.PrimaryKeyRelatedField(queryset=InsuranceHealth.objects.all(), many=False)
    blood_type = serializers.PrimaryKeyRelatedField(queryset=BloodType.objects.all(), many=False)
    who_enroll = serializers.PrimaryKeyRelatedField(queryset=RelationshipType.objects.all(), many=False)
    school = serializers.PrimaryKeyRelatedField(queryset=SchoolConfig.objects.all(), many=False)
    grade_group = serializers.PrimaryKeyRelatedField(queryset=GradeGroupConfig.objects.all(), many=False)
    blood_type = serializers.PrimaryKeyRelatedField(queryset=BloodType.objects.all(), many=False)

    class Meta:
        model = Student
        fields = '__all__'
    
    def to_representation(self, instance: Student):
        return {
            "id": instance.id,
            "insurance_health": {
                "id": instance.insurance_health.id,
                "name": instance.insurance_health.name
            },
            "who_enroll":{
                "id": instance.who_enroll.id,
                "name": instance.who_enroll.relation_name
            },
            "school": {
                "id": instance.school.id,
                "name": instance.school.school_name
            },
            "grade_group": {
                "grade": {
                    "id": instance.grade_group.grade.id,
                    "grade": instance.grade_group.grade.grade
                },
                "group": {
                    "id": instance.grade_group.group.id,
                    "grade": instance.grade_group.group.group
                }
            },
            "blood_type": {
                "id": instance.blood_type.id,
                "blood_type": instance.blood_type.blood_type
            },
            "name": instance.name,
            "father_lastname": instance.father_lastname,
            "mother_lastname": instance.mother_lastname,
            "curp": instance.curp,
            "birthDate": instance.birthDate,
            "birth_certificate": f"{HOST}{MEDIA_URL}{instance.birth_certificate}" if os.path.exists(instance.birth_certificate.path) else None,
            "curp_file": f"{HOST}{MEDIA_URL}{instance.curp_file}" if os.path.exists(instance.curp_file.path) else None,
            "email": instance.email,
            "is_active": instance.is_active
        }

class AddressSerializer(serializers.ModelSerializer):
    sepomex_catalog = serializers.PrimaryKeyRelatedField(queryset=SepomexCatalog.objects.select_related(
        'zip_code', 
        'suburb', 
        'city', 
        'town', 
        'state'
        ).all(), many=False)
    
    class Meta:
        model = Address
        fields = '__all__'

class TutorSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.select_related('sepomex_catalog').all(), many=False)
    relationship_kind = serializers.PrimaryKeyRelatedField(queryset=RelationshipType.objects.all(), many=False)

    class Meta:
        model = Tutor
        fields = '__all__'

    def to_representation(self, instance: Tutor):
        suburb = {}
        zip_code = {}
        city = {}
        town = {}
        state = {}

        if instance.address.sepomex_catalog.suburb:
            suburb = {
                "id": instance.address.sepomex_catalog.suburb.id,
                "zip_code": instance.address.sepomex_catalog.suburb.name
            }
        
        if instance.address.sepomex_catalog.zip_code:
            zip_code = {
                "id": instance.address.sepomex_catalog.zip_code.id,
                "zip_code": instance.address.sepomex_catalog.zip_code.zip_code
            }

        if instance.address.sepomex_catalog.city:
            city = {
                "id": instance.address.sepomex_catalog.city.id,
                "city": instance.address.sepomex_catalog.city.name
            }

        if instance.address.sepomex_catalog.town:
            town = {
                "id": instance.address.sepomex_catalog.town.id,
                "town": instance.address.sepomex_catalog.town.name
            }

        if instance.address.sepomex_catalog.state:
            state = {
                "id": instance.address.sepomex_catalog.state.id,
                "state": instance.address.sepomex_catalog.state.name
            }


        return {
            "id": instance.id,
            "name": instance.name,
            "father_lastname": instance.father_lastname,
            "mother_lastname": instance.mother_lastname,
            "cellphone": instance.cellphone,
            "email": instance.email,
            "no_ine": instance.no_ine,
            "address": {
                "street": instance.address.street,
                "no_int": instance.address.no_int,
                "no_ext": instance.address.no_ext,
                "phone_number": instance.address.phone_number,
                "sepomex_catalog": {
                    "id": instance.address.sepomex_catalog.id,
                    "zip_code": zip_code if zip_code else None,
                    "suburb": suburb if suburb else None,
                    "city": city if city else None,
                    "town": town if town else None,
                    "state": state if state else None
                }
            },
            "is_emergency_contact": instance.is_emergency_contact,
            "relationship_kind": {
                "id": instance.relationship_kind.id,
                "relation_name": instance.relationship_kind.relation_name
            },
            "curp": instance.curp,
            "address_proof": f"{HOST}{MEDIA_URL}{instance.address_proof}" if os.path.exists(instance.address_proof.path) else None,
            "ine": f"{HOST}{MEDIA_URL}{instance.ine}" if os.path.exists(instance.ine.path) else None,
        }