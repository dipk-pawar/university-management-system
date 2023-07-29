import json

from django.apps import apps
from django_tenants.utils import schema_context


def save_data_in_schema_table(data, schema_name, app_lable, model_name):
    with schema_context(schema_name):
        model_obj = apps.get_model(app_label=app_lable, model_name=model_name)
        try:
            instance = model_obj.objects.get(master_user_id=data.get("master_user_id"))
            # Update operation
            for key, value in data.items():
                setattr(instance, key, value)
            instance.save()
        except model_obj.DoesNotExist:
            # Create operation
            schema_model = model_obj(**data)
            schema_model.save()
