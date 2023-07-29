from apps.master.models import University


def create_university_schema(uid, schema_name, university_data):
    """
    This task creates a new tenant schema for a university and sets it as the user's university.
    """
    university_details = {
        "uid": uid,
        "schema_name": schema_name,
        "name": university_data.get("university_name"),
        "email": university_data.get("university_email"),
        "address": university_data.get("university_address"),
        "country_id": university_data.get("university_country"),
        "postal_code": university_data.get("university_postal_code"),
    }
    university = University.objects.create(**university_details)

    return university.uid
