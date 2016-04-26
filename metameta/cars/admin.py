from django.contrib import admin
from cars.models import HondaCar


class HondaCarAdmin(admin.ModelAdmin):
    pass

admin.site.register(HondaCar, HondaCarAdmin)
