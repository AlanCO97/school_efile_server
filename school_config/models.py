from django.db import models
from django.contrib.auth.models import User

MORNING_SHIFT = 'MATUTINO'
AFTERNOON_SHIFT = 'VESPERTINO'
SHIFT_CHOICES = [
    (MORNING_SHIFT, 'Matutino'),
    (AFTERNOON_SHIFT, 'Vespertino'),
]

class SchoolTurns(models.Model):
    turn = models.CharField(max_length=20, choices=SHIFT_CHOICES, default=AFTERNOON_SHIFT)

    def __str__(self) -> str:
        return self.turn
    
    class Meta:
        verbose_name = 'Turno de la escuela'
        verbose_name_plural = 'Turnos de la escuela'

class SchoolConfig(models.Model):
    school_name = models.CharField(max_length=255)
    school_key = models.CharField(max_length=60)
    zone = models.CharField(max_length=255, null=True, blank=True)
    turn = models.ForeignKey(SchoolTurns, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.school_name}-{self.school_key}"

    class Meta:
        verbose_name = 'Configuracion de la escuela'
        verbose_name_plural = 'Configuraciones de la escuela'

class AcademicYear(models.Model):
    init_day = models.DateField()
    end_day = models.DateField()

    def __str__(self) -> str:
        return f"{self.init_day.year}-{self.end_day.year}"

    class Meta:
        verbose_name = 'Ciclo escolar'
        verbose_name_plural = 'Ciclos escolares'

class Position(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'

class Employee(models.Model):
    name = models.CharField(max_length=255)
    father_lastname = models.CharField(max_length=255)
    mother_lastname = models.CharField(max_length=255)
    curp = models.CharField(max_length=18)
    birthDate = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolConfig, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(null=True, blank=True)

    def complete_name(self) -> str:
        return f"{self.name} {self.father_lastname} {self.father_lastname}"

    def __str__(self) -> str:
        complete_name: str = self.complete_name()

        return complete_name

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

class EfileConfig(models.Model):
    folio = models.CharField(max_length=255)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolConfig, on_delete=models.CASCADE)
    current_config = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.folio}"

    def save(self, *args, **kwargs):
        """ pass all current_config to false """
        EfileConfig.objects.update(current_config=False)
        return super(EfileConfig, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Configuracion del expediente'
        verbose_name_plural = 'Configuracion del expediente'

class Grade(models.Model):
    grade = models.CharField(max_length=255)
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.grade
    
    class Meta:
        verbose_name = 'Grados'
        verbose_name_plural = 'Grados'

class Group(models.Model):
    group = models.CharField(max_length=255)
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.group
    
    class Meta:
        verbose_name = 'Grupos'
        verbose_name_plural = 'Grupos'

class GradeGroupConfig(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.grade.grade}-{self.group.group}"

    class Meta:
        verbose_name = 'Configuracion del grado y grupo'
        verbose_name_plural = 'Configuracion del grado y grupo'