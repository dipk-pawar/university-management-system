from django.urls import re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import user_views


urlpatterns = [
    re_path(
        r"^register/$",
        user_views.CreateUniversityAndUser.as_view(),
        name="CreateUniversityAndUser",
    ),
]
