from rest_framework import generics, status
from apps.accounts.serializers.user_serializer import UserSerializer
from apps.master.models import User as public_users
from django.db import transaction
from apps.common.generate_schema_name import Schema
from apps.common.tasks import create_university_schema
from rest_framework.response import Response


# Create your views here.
class CreateUniversityAndUser(generics.CreateAPIView):
    """
    This is a view for creating a university account. It handles the process of creating
    a university and a user associated with the university, and setting default data in the
    database. It also generates a unique schema name for the university and auth token for the user. # noqa: E501
    """

    serializer_class = UserSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check it university id is available
        if "university_id" in request.data:
            university_id = request.data.get("university_id")
            user = serializer.save(university_id=university_id, is_staff=False)
            message = "User Created successfully"
        elif (
            request.data.get("university_name") is not None
            and request.data.get("university_name").strip() != ""
        ):
            schema_name = Schema.generate_schema_name(
                university_name=request.data.get("university_name")
            )
            uid = Schema.generate_uuid()

            university_id = create_university_schema(
                uid=uid,
                schema_name=schema_name,
                university_data=request.data,
            )
            user = serializer.save(
                university_id=university_id, is_staff=True, is_universityadmin=True
            )
            message = "university Created successfully"
        else:
            raise ValueError("university name is required")

        user_obj = (
            public_users.objects.filter(id=user.id)
            .values(
                "id",
                "email",
                "first_name",
                "last_name",
                "middle_name",
                "university_id__name",
            )
            .first()
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "error": False,
                "data": [
                    {
                        "user_id": user_obj.get("id"),
                        "email": user_obj.get("email"),
                        "first_name": user_obj.get("first_name"),
                        "last_name": user_obj.get("last_name"),
                        "middle_name": user_obj.get("middle_name"),
                        "university_name": user_obj.get("university_id__name"),
                    }
                ],
                "message": message,
            },
        )
