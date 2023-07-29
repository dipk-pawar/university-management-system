import random
import string
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


def generate_random_password(length=12):
    """
    Generate a random password with the specified length.
    The password will consist of uppercase letters, lowercase letters, digits, and punctuation.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def generate_random_username(first_name, last_name):
    first_name_part = first_name[:5]
    last_name_part = last_name[:5]
    random_int_str = str(random.randint(10000, 99999))
    username = f"{first_name_part}{last_name_part}{random_int_str}"
    return username.upper()
