from django.contrib import admin
from users.models import Role, CustomUser

admin.site.register(Role)
admin.site.register(CustomUser)
