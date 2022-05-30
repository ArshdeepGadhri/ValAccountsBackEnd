from django.contrib import admin

# Register your models here.
from accounts.models import CustomUser, ValorantAccount

admin.site.register(CustomUser)
admin.site.register(ValorantAccount)