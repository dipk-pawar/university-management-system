def remove_extra_keys(user_data):
    user_data["master_user_id"] = user_data.get("id")
    user_data.pop("_state", None)
    user_data.pop("id", None)
    user_data.pop("password", None)
    user_data.pop("last_login", None)
    user_data.pop("is_superuser", None)
    user_data.pop("is_active", None)
    user_data.pop("_password", None)
    user_data.pop("date_joined", None)
    user_data.pop("is_admin", None)
    user_data.pop("is_superadmin", None)
    return user_data
