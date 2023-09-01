from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


# Department
class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department


class DepartmentAdmin(ImportExportModelAdmin):
    resource_classes = [DepartmentResource]
    list_display = ['department_name']


class SemesterResource(resources.ModelResource):
    class Meta:
        model = Semester


class SemesterAdmin(ImportExportModelAdmin):
    resource_classes = [SemesterResource]
    list_display = ['id', 'year', 'name']


# Major
class MajorResource(resources.ModelResource):
    class Meta:
        model = Major


class MajorAdmin(ImportExportModelAdmin):
    resource_classes = [MajorResource]
    list_display = ['major_name', 'department']


# Student
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        import_id_fields = ('student_key',)
        exclude = ('id',)


class StudentAdmin(ImportExportModelAdmin):
    resource_classes = [StudentResource]
    list_display = ['student_key', 'gender_str', 'major', 'status']

    @admin.display(description="Gender String")
    def gender_str(self, obj):
        if obj.gender:
            return "Male"
        else:
            return "Female"


# Point
class PointResource(resources.ModelResource):
    class Meta:
        model = Point


class PointAdmin(ImportExportModelAdmin):
    resource_classes = [PointResource]
    list_display = ('student', 'point_type', 'value')


# Fact
class FactResource(resources.ModelResource):
    class Meta:
        model = Fact


class FactAdmin(ImportExportModelAdmin):
    resource_classes = [FactResource]
    list_display = ('id', 'student', 'semester', 'event')


# Register
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(Fact, FactAdmin)
