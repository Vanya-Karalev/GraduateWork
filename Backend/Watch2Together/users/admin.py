from django.contrib import admin
from users.models import Role, CustomUser, Notifications

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Notifications)
