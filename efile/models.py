from django.db import models

from school_config.models import AcademicYear, EfileConfig, Employee, GradeGroupConfig, SchoolConfig

def upload_to_birth_certificate(instance, filename) -> str:
    return f"user-{instance.curp.upper()}/birth_certificate_student/{filename}"

def upload_to_curp(instance, filename) -> str:
    return f"user-{instance.curp.upper()}/curp_student/{filename}"

def upload_to_tutor_address_proof(instance, filename) -> str:
    return f"user-{instance.curp.upper()}/curp_father/{filename}"

def upload_to_tutor_ine(instance, filename) -> str:
    return f"user-{instance.curp.upper()}/curp_ine/{filename}"

class InsuranceHealth(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Seguro medico'
        verbose_name_plural = 'Seguros medicos'

class BloodType(models.Model):
    blood_type = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.blood_type

    class Meta:
        verbose_name = 'Tipo de sangre'
        verbose_name_plural = 'Tipo de sangre'

class RelationshipType(models.Model):
    relation_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.relation_name

    class Meta:
        verbose_name = 'Tipo de relacion'
        verbose_name_plural = 'Tipo de relacion'

class ZipCode(models.Model):
    zip_code = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Catalogo de codigos postales'
        verbose_name_plural = 'Catalogo de codigos postales'

    def __str__(self) -> str:
        return self.zip_code

class Suburb(models.Model):
    name = models.CharField(max_length=255) # colonia

    class Meta:
        verbose_name = 'Catalogo de colonias'
        verbose_name_plural = 'Catalogo de colonias'

    def __str__(self) -> str:
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255) # ciudad

    class Meta:
        verbose_name = 'Catalogo de ciudades'
        verbose_name_plural = 'Catalogo de ciudades'

    def __str__(self) -> str:
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=255) # municipio

    class Meta:
        verbose_name = 'Catalogo de municipios'
        verbose_name_plural = 'Catalogo de municipios'

    def __str__(self) -> str:
        return self.name

class State(models.Model):
    name = models.CharField(max_length=255) # ciudad

    class Meta:
        verbose_name = 'Catalogo de estados'
        verbose_name_plural = 'Catalogo de estados'

    def __str__(self) -> str:
        return self.name

class SepomexCatalog(models.Model):
    zip_code = models.ForeignKey(ZipCode, on_delete=models.CASCADE)
    suburb = models.ForeignKey(Suburb, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Catalogo de sepomex'
        verbose_name_plural = 'Catalogo de sepomex'

    def __str__(self) -> str:
        return f"{self.zip_code.zip_code}-{self.state.name}-{self.city.name}-{self.town.name}-{self.suburb.name}"

class Address(models.Model):
    street = models.CharField(max_length=255)
    no_int = models.CharField(max_length=255, null=True, blank=True, default=None)
    no_ext = models.CharField(max_length=255)    
    phone_number = models.CharField(max_length=255)
    sepomex_catalog = models.ForeignKey(SepomexCatalog, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.street}-No.{self.no_ext}-{self.suburb}-{self.state}-{self.town}"

    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'

class Student(models.Model):
    name = models.CharField(max_length=255)
    father_lastname = models.CharField(max_length=255)
    mother_lastname = models.CharField(max_length=255)
    curp = models.CharField(max_length=18)
    birthDate = models.DateField()
    insurance_health = models.ForeignKey(InsuranceHealth, on_delete=models.SET_NULL, null=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True)
    who_enroll = models.ForeignKey(RelationshipType, on_delete=models.SET_NULL, null=True)
    birth_certificate = models.FileField(upload_to=upload_to_birth_certificate)
    curp_file = models.FileField(upload_to=upload_to_curp)
    school = models.ForeignKey(SchoolConfig, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    grade_group = models.ForeignKey(GradeGroupConfig, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def complete_name(self) -> str:
        return f"{self.name} {self.father_lastname} {self.father_lastname}"

    def __str__(self) -> str:
        complete_name: str = self.complete_name()

        return complete_name

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        constraints = [
            models.UniqueConstraint(fields=['curp'], name='unique curp student')
        ]

class Tutor(models.Model):
    name = models.CharField(max_length=255)
    father_lastname = models.CharField(max_length=255)
    mother_lastname = models.CharField(max_length=255)
    cellphone = models.CharField(max_length=16)
    email = models.EmailField()
    no_ine = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_emergency_contact = models.BooleanField(default=False)
    relationship_kind = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    curp = models.CharField(max_length=18)
    address_proof = models.FileField(upload_to=upload_to_tutor_address_proof)
    ine = models.FileField(upload_to=upload_to_tutor_ine)

    def complete_name(self) -> str:
        return f"{self.name} {self.father_lastname} {self.father_lastname}"

    def __str__(self) -> str:
        complete_name: str = self.complete_name()

        return complete_name

    class Meta:
        verbose_name = 'Tutores'
        verbose_name_plural = 'Tutores'
        constraints = [
            models.UniqueConstraint(fields=['curp'], name='unique curp tutors')
        ]


class Efile(models.Model):
    efile_config = models.ForeignKey(EfileConfig, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor_one =  models.ForeignKey(Tutor, on_delete=models.CASCADE, blank=True, null=True, related_name="tutor_one")
    tutor_two =  models.ForeignKey(Tutor, on_delete=models.CASCADE, blank=True, null=True, related_name="tutor_two")
    emergency_one =  models.ForeignKey(Tutor, on_delete=models.CASCADE, blank=True, null=True,related_name="emergency_one")
    emergency_two =  models.ForeignKey(Tutor, on_delete=models.CASCADE, blank=True, null=True, related_name="emergency_two")
    emergency_three =  models.ForeignKey(Tutor, on_delete=models.CASCADE, blank=True, null=True, related_name="emergency_three")
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def get_folio(self) -> str:
        return str(self.pk).zfill(7)

    def __str__(self) -> str:
        folio: str = self.get_folio()
        return f"folio: {folio}-{self.efile_config.school.school_name}"
    
    class Meta:
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'

