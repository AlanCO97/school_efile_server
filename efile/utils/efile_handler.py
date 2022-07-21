from dataclasses import dataclass
from django.db import transaction
from efile.models import Efile, Student
from school_config.models import EfileConfig, Employee


@dataclass
class EfileHandler:
    
    def create_efile(self, efile_config: EfileConfig, student: Student, employee: Employee) -> bool|str:
        try:
            with transaction.atomic():
                efile: Efile = Efile.objects.create(efile_config=efile_config, student=student, created_by=employee)

                if efile:
                    return True, ''
                raise Exception("no se pudo crear el expediente")
        except Exception as e:
            return False, str(e)
    
    def get_current_efile_config(self) -> EfileConfig:
        efile_config: EfileConfig = EfileConfig.objects.filter(current_config=True)

        if efile_config:
            return efile_config.first()
        raise Exception('No hay una configuracion activa')