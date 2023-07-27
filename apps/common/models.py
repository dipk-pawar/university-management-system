from django.db import models


# Create your models here.
class TimeStampModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommonUser(TimeStampModel):
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    university = models.ForeignKey(
        "master.University",
        to_field="uid",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        "master.Role",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    country = models.ForeignKey(
        "master.Country",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
