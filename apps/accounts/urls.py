from django.urls import re_path
from apps.accounts.views import user_views


urlpatterns = [
    re_path(r"^login/$", user_views.Login.as_view(), name="Login"),
    re_path(
        r"^register/$",
        user_views.CreateUniversityAndUser.as_view(),
        name="CreateUniversityAndUser",
    ),
]
