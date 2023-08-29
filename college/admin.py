from django.contrib import admin
from .models import *


class MajorAdmin(admin.ModelAdmin):
    list_display = ['major_name', 'department', 'current_students']


class EventAdmin(admin.ModelAdmin):
    list_display = ['major', 'event_type', 'event_date', 'students']
    list_filter = ["major", "event_type"]


admin.site.register(Department)
admin.site.register(Major, MajorAdmin)
admin.site.register(Event, EventAdmin)

