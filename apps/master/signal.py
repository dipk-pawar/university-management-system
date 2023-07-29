# from django.db import connection
# from django.db.models.signals import post_save, pre_delete
# from django.dispatch import receiver

# from apps.accounts.models import Users as tenant_users
# from apps.common.helper.common_helper import save_data_in_schema_table
# from apps.common.helper.users_helper import remove_extra_keys

# from .models import User


# @receiver(post_save, sender=User)
# def user_post_save(sender, instance, created, **kwargs):
#     user_instance = instance.__dict__.copy()
#     user_data = remove_extra_keys(user_data=user_instance)
#     # Create / Update the Users data in Schema model
#     save_user_data(instance, user_data)

#     if created and instance.company and instance.company.schema_name:
#         # Save User setting in schema model
#         save_data_in_schema_table(
#             data={"user_id": instance.id},
#             schema_name=instance.company.schema_name,
#             app_lable="accounts",
#             model_name="UserSettings",
#         )


# def save_user_data(instance, user_data):
#     if instance.company and instance.company.schema_name:
#         save_data_in_schema_table(
#             data=user_data,
#             schema_name=instance.company.schema_name,
#             app_lable="accounts",
#             model_name="Users",
#         )


# @receiver(pre_delete, sender=User)
# def delete_related_accounts_users(sender, instance, **kwargs):
#     __tenant_schema_name = instance.company.schema_name
#     with connection.cursor() as cursor:
#         cursor.execute(f"SET search_path TO {__tenant_schema_name}")
#         tenant_users.objects.filter(user=instance).delete()
