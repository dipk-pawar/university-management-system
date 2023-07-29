import contextlib

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from apps.accounts.models import UserSettings
from apps.accounts.serializers import skills_serializers
from apps.common.helper.common_helper import get_schema_table
from apps.master.models import Company
from apps.master.models import User as public_users
from hrms.utils import Util


class UserSerializer(serializers.ModelSerializer):
    """
    This class represents a serializer for company user accounts..
    """

    user_settings = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()

    class Meta:
        model = public_users
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "password",
            "email",
            "phone_number",
            "about",
            "is_staff",
            "address",
            "joining_date",
            "dob",
            "education",
            "designation",
            "role",
            "experience",
            "facebook_link",
            "instagram_link",
            "linkedin_link",
            "twitter_link",
            "is_companyadmin",
            "user_settings",
            "skills",
        )

        extra_kwargs = {
            "created": {"read_only": True},
            "id": {"read_only": True},
            "email": {"write_only": True},
            "username": {"read_only": True},
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    def get_user_settings(self, obj):
        if obj.company and obj.company.schema_name:
            schema_name = obj.company.schema_name
            schema_model_name = get_schema_table(
                schema_name=schema_name, app_lable="accounts", model_name="UserSettings"
            )
            try:
                user_id = getattr(obj, "user_id", obj.id)
                user_settings_instance = schema_model_name.objects.get(user_id=user_id)
                user_settings_serializer = UserSettingsSerializer(
                    user_settings_instance
                )
                return user_settings_serializer.data
            except schema_model_name.DoesNotExist:
                return {}

    def get_skills(self, obj):
        skills = obj.accounts_skills_users.all()
        return [
            skills_serializers.SkillsSerializer(skill.skill).data for skill in skills
        ]

    def update_user_skills(self, instance, request):
        schema_name = instance.company.schema_name
        schema_model_name = get_schema_table(
            schema_name=schema_name, app_lable="accounts", model_name="SkillsUser"
        )
        user_skills = request.data.get("user_skills")
        existing_skills = schema_model_name.objects.filter(user_id=instance.id)
        for skill in existing_skills:
            if skill.skill_id not in user_skills:
                skill.delete()
        for skill in user_skills:
            schema_model_name.objects.get_or_create(
                user_id=instance.id, skill_id=skill, company_id=instance.company_id
            )

    def is_valid(self, raise_exception=False):
        email = self.initial_data.get("email")
        if email and public_users.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"error": True, "message": "Account already exists."}
            )
        return super(UserSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        return public_users.objects.create_user(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context["request"]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if "email" in request.data and instance.email != request.data.get("email"):
            instance.username = request.data.get("email")
            instance.email = request.data.get("email")

        # Update User Settings i.e about enable / disable the privacy settings
        if "user_settings" in request.data:
            schema_name = instance.company.schema_name
            schema_model_name = get_schema_table(
                schema_name=schema_name, app_lable="accounts", model_name="UserSettings"
            )
            with contextlib.suppress(schema_model_name.DoesNotExist):
                usersetting_instance = schema_model_name.objects.get(
                    user_id=instance.id
                )
                for attr, value in request.data.get("user_settings").items():
                    setattr(usersetting_instance, attr, value)
                usersetting_instance.save()

        # Update User Skills
        if "user_skills" in request.data:
            self.update_user_skills(instance, request)

        instance.save()
        return instance
