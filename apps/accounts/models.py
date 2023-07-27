from django.db import models
from apps.common.models import CommonUser


class Users(CommonUser):
    email = models.EmailField()
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
