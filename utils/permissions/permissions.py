from school_config.models import Employee

def validate_rol(employee: Employee, need_rol: list)-> bool:
    if employee.position.name in need_rol:
        return True
    return False