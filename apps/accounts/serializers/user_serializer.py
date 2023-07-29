from rest_framework import serializers
from apps.master.models import User as public_users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = public_users
        fields = (
            "id",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "university",
            "country",
            "is_verified",
            "is_active",
        )

        extra_kwargs = {
            "created_date": {"read_only": True},
            "id": {"read_only": True},
            "email": {"write_only": True},
            "username": {"read_only": True},
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    def create(self, validated_data):
        return public_users.objects.create_user(**validated_data)
