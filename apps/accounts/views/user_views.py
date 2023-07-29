from rest_framework import generics, status
from apps.accounts.serializers.user_serializer import (
    UserSerializer,
    BasicAuthenticationSerializer,
)
from apps.master.models import User as public_users
from django.db import transaction
from apps.common.generate_schema_name import Schema
from apps.common.tasks import create_university_schema
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from ums.jwt_custom_token import get_tokens_for_user


# Create your views here.
class Login(ObtainAuthToken):
    serializer_class = BasicAuthenticationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_message = self.get_error_message(serializer.errors)
            return Response(
                {"error": True, "message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        tokens = get_tokens_for_user(user=user)
        user_data = self.get_user_data(user)

        return Response(
            {
                "error": False,
                "tokens": tokens,
                "user": user_data,
                "message": "Login successfully",
            },
            status=status.HTTP_200_OK,
        )

    def get_error_message(self, errors):
        if "email" in errors:
            return errors["email"][0]
        elif "password" in errors:
            return errors["password"][0]
        else:
            return errors["error"][0]


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
                "username",
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
                        "user_name": user_obj.get("username"),
                        "first_name": user_obj.get("first_name"),
                        "middle_name": user_obj.get("middle_name"),
                        "last_name": user_obj.get("last_name"),
                        "email": user_obj.get("email"),
                        "university_name": user_obj.get("university_id__name"),
                    }
                ],
                "message": message,
            },
        )
