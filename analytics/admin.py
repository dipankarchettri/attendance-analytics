from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student, Course, Attendance

# Register your models here.
@admin.register(Student)
class userdata(ImportExportModelAdmin):
    fields = ('usn','full_name', 'gender')  # Specify the field(s) you want to import/export

@admin.register(Course)
class userdata(ImportExportModelAdmin):
    pass

@admin.register(Attendance)
class userdata(ImportExportModelAdmin):
    pass