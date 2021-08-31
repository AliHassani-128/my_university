from django.contrib import admin

# Register your models here.
from .models import *

class StudentInline(admin.StackedInline):
    model = Student



class ClassInline(admin.StackedInline):
    model = Class_Lesson_Student

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass

@admin.register(Class_Lesson_Student)
class ClassLessonAdimn(admin.ModelAdmin):
    pass


def set_lesson_off(modeladmin, request, queryset):
    queryset.update(status=False)

set_lesson_off.short_description = 'غیر فعال کردن کلاس'
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    actions = [set_lesson_off, ]


