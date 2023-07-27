from django.contrib import admin
from .models import User, Role, College, Country, Department

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(College)
admin.site.register(Country)
admin.site.register(Department)
