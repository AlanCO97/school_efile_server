from django.db import transaction

def get_fields_and_properties(model, instance):
    """
        Method that get the field and property of a model

        ARGS:
            - Model: name of the model
            - Instance: Intance of the model
    """
    field_names = [f.name for f in model._meta.fields]
    property_names = [name for name in dir(model) if isinstance(getattr(model, name), property)]
    return dict((name, getattr(instance, name)) for name in field_names + property_names)

def add_field_to_efile(model, field_name, value, instance) -> tuple:
    with transaction.atomic():
        try:
            fields: dict = get_fields_and_properties(model=model, instance=instance)

            is_updated: bool = False

            for field in fields:
                if field_name in field:
                    if not fields[field]:
                        instance[field] = value
                        instance.save()
                        is_updated = True
                        break
            
            if is_updated:
                return True, 'Se actualizo'
            
            raise Exception('El campo solicitado ya esta lleno')

        except Exception as e:
            return False, str(e)