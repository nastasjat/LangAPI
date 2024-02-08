from django.contrib import admin

from .models import (
    Course,
    Student,
    Enrolment,
    Teacher,
    Course_Teacher,
    Language,
    Language_Course,
)

# Register your models here.


admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Enrolment)
admin.site.register(Teacher)
admin.site.register(Course_Teacher)
admin.site.register(Language)
admin.site.register(Language_Course)
