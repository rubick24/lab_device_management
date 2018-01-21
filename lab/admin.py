from django.contrib import admin

# Register your models here.
from .models import DeviceType,Device,Repair,Scrap,ApplyRecord

admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(Repair)
admin.site.register(Scrap)
admin.site.register(ApplyRecord)