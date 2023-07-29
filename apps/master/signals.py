from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import Users as tenant_users
from apps.common.helper.common_helper import save_data_in_schema_table
from apps.common.helper.users_helper import remove_extra_keys
from .models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    user_instance = instance.__dict__.copy()
    user_data = remove_extra_keys(user_data=user_instance)
    # Create / Update the Users data in Schema model
    save_user_data(instance, user_data)


def save_user_data(instance, user_data):
    if instance.university and instance.university.schema_name:
        save_data_in_schema_table(
            data=user_data,
            schema_name=instance.university.schema_name,
            app_lable="accounts",
            model_name="Users",
        )
