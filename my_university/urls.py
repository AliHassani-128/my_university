from django.urls import path, include
from .views import all_class, lesson_student, new_student, select_lesson, edit_profile, search, home, \
    login_user, logout_user, student_all_lessons, all_students, edit_student_lesson, show_lesson_student, login_student, \
    login_teacher, login_staff

app_name = 'my_university'

urlpatterns = [
    path('', home, name='home'),
    path('all-classes/', all_class, name='all_class'),
    path('lesson-student/<int:class_id>', lesson_student, name='lesson_student'),
    path('register-student/', new_student, name='new_student'),
    path('select-lesson/<int:st_id>', select_lesson, name='select_lesson'),
    path('edit-profile/<int:student_id>', edit_profile, name='edit_profile'),
    path('search/', search, name='search'),
    path('login-student/', login_student, name='login_student'),
    path('login-teacher/', login_teacher, name='login_teacher'),
    path('login-staff/', login_staff, name='login_staff'),
    path('login/',login_user,name='login'),
    path('logout/', logout_user, name='logout'),
    path('accounts/login/', login_user),
    path('show-student-lessons/<int:student_id>',student_all_lessons,name='show_all_lessons'),
    path('all-students/<int:teacher_id>',all_students,name='all_students'),
    path('show-student/<int:lesson_id>',show_lesson_student,name='show_lesson_student'),
    path('edit-lesson/<int:lesson_id><int:student_id>',edit_student_lesson,name='edit-lesson')

]
