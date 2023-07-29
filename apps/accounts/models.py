from django.db import models
from apps.common.models import CommonUser


class Users(CommonUser):
    email = models.EmailField()
    college = models.ForeignKey(
        "common.College",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    department = models.ForeignKey(
        "common.Department",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        "common.Role",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    master_user = models.ForeignKey(
        "master.User",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="master_users",
    )

    class Meta:
        db_table = "accounts_users"
