from django.contrib import admin
from movies.models import *

admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Favorites)
