from django.db import models


# Create your models here.
class TimeStampModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class College(TimeStampModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    university = models.ForeignKey(
        "master.University", on_delete=models.CASCADE, related_name="colleges"
    )

    def __str__(self):
        return self.name


class Department(TimeStampModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    college = models.ForeignKey(
        "common.College", on_delete=models.CASCADE, related_name="departments"
    )

    def __str__(self):
        return self.name


class Role(TimeStampModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=250, default=None, blank=True, null=True)
    university = models.ForeignKey(
        "master.University",
        to_field="uid",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
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

    def __str__(self) -> str:
        return self.title


class CommonUser(TimeStampModel):
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    university = models.ForeignKey(
        "master.University",
        to_field="uid",
        null=True,
        blank=True,
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
