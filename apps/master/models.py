from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
from apps.common.models import CommonUser, TimeStampModel


class CustomUserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        if not extra_fields.get("email"):
            raise ValueError("The Email field must be set")
        extra_fields["email"] = self.normalize_email(extra_fields.get("email"))
        user = self.model(**extra_fields)
        user.set_password(extra_fields.get("password"))
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superadmin", True)
        return self.create_user(**extra_fields)


class Domain(DomainMixin):
    pass


class Country(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class University(TenantMixin, models.Model):
    uid = models.UUIDField(primary_key=True, editable=True)
    university_name = models.CharField(max_length=100)
    university_email = models.EmailField(default=None, blank=True, null=True)
    university_address = models.CharField(max_length=250)
    university_country = models.ForeignKey(
        Country,
        to_field="id",
        related_name="university_country_id",
        on_delete=models.CASCADE,
    )
    university_postal_code = models.CharField(max_length=50)
    university_contact_no = models.CharField(
        max_length=50, default=None, blank=True, null=True
    )
    university_website = models.URLField(default=None, blank=True, null=True)
    university_descriptions = models.CharField(
        max_length=250, default=None, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Universities"

    def __str__(self) -> str:
        return self.university_name


class Role(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=250, default=None, blank=True, null=True)
    university = models.ForeignKey(
        "master.University",
        to_field="uid",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.title


class User(AbstractBaseUser, CommonUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    # required fields for
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self) -> str:
        return self.email
