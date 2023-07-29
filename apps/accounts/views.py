from django.shortcuts import render


# Create your views here.
class CreateCompanyAndUser(generics.CreateAPIView):
    """
    This is a view for creating a Company account. It handles the process of creating
    a company and a user associated with the company, and setting default data in the
    database. It also generates a unique schema name for the company and auth token for the user. # noqa: E501
    """

    serializer_class = user_serializers.UserSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check it company id is available
        if "company_id" in request.data:
            company_id = request.data.get("company_id")
            user = serializer.save(company_id=company_id, is_staff=False)
            # Assing Group to user
            group, _ = Group.objects.get_or_create(name=RoleType.EMPLOYEE)
            user.groups.add(group)
            message = "User Created successfully"
        elif (
            request.data.get("company_name") is not None
            and request.data.get("company_name").strip() != ""
        ):
            schema_name = Schema.generate_schema_name(
                company_name=request.data.get("company_name")
            )
            uid = Schema.generate_uuid()

            company_id = create_company_schema(
                uid=uid,
                schema_name=schema_name,
                company_data=request.data,
            )
            user = serializer.save(
                company_id=company_id, is_staff=True, is_companyadmin=True
            )
            # Assing Group to company admin
            group, _ = Group.objects.get_or_create(name=RoleType.ADMIN)
            user.groups.add(group)
            message = "Company Created successfully"
        else:
            raise ValueError("company name is required")

        user_obj = (
            public_users.objects.filter(id=user.id)
            .values(
                "id",
                "email",
                "first_name",
                "last_name",
                "middle_name",
                "phone_number",
                "company_id__company_name",
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
                        "company_name": user_obj.get("company_id__company_name"),
                    }
                ],
                "message": message,
            },
        )
