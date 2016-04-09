from django.contrib import admin

from .models import HighVolume, LowVolume, Asset

admin.site.register(HighVolume)
admin.site.register(LowVolume)
admin.site.register(Asset)
