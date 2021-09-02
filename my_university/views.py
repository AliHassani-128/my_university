from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .forms import StudentForm, SelectLesson
from .models import *


# Create your views here.
def home(request):
    return render(request, 'my_university/home.html')

def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(Student.objects.filter(name=username))
        print(Student.objects.filter(name=username,password=password))
        if Student.objects.filter(name=username, password=password):
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'username or password not found')
                return render(request, 'my_university/login_student.html')
        else:
            messages.error(request, 'Just Students can login with this view')
            return render(request, 'my_university/login_student.html')

    return render(request, 'my_university/login_student.html')


def login_teacher(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Teacher.objects.filter(name=username, password=password):
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'username or password not found')
                return render(request, 'my_university/login_teacher.html')
        else:
            messages.error(request, 'Just Teachers can login with this view')
            return render(request, 'my_university/login_teacher.html')

    return render(request, 'my_university/login_teacher.html')

def login_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Staff.objects.filter(name=username,password=password):
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'username or password not found')
                return render(request, 'my_university/login_staff.html')
        else:
            messages.error(request, 'Just Staffs can login with this view')
            return render(request,'my_university/login_staff.html')



    return render(request, 'my_university/login_staff.html')





def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'username or password not found')
            return render(request, 'my_university/login.html')

    return render(request, 'my_university/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def all_class(request):
    context = {'classes': Class.objects.all()}
    return render(request, 'my_university/index.html', context=context)


def lesson_student(request, class_id):
    find_class = Class_Lesson_Student.objects.filter(classroom_id=class_id).values('lesson_id','lesson__name').distinct()
    context = {'classes': find_class}
    return render(request, 'my_university/lesson_student.html', context=context)

def show_lesson_student(request,lesson_id):
    find_lesson = Class_Lesson_Student.objects.filter(lesson_id=lesson_id)
    context = {'classes':find_lesson}
    return render(request,'my_university/show_lesson_student.html',context=context)





#@permission_required('my_university.add_student',raise_exception=True)
def new_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            major = form.cleaned_data['major']
            new_st = form.save(commit=False)
            if Student.objects.filter(name=name, last_name=last_name, major=major).exists():
                messages.error(request, 'Student with this name has exists')
                return render(request, 'my_university/new_student.html', context={'form': form})

            else:
                new_st.password = password
                new_st.save()
                messages.success(request, 'Student added successfully')
                return HttpResponseRedirect('/')

    else:
        form = StudentForm()
    return render(request, 'my_university/new_student.html', context={'form': form})

@login_required
def select_lesson(request, st_id):
    student = Student.objects.get(id=st_id)
    if request.method == 'POST':
        form = SelectLesson(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            if not Class_Lesson_Student.objects.filter(classroom_id=instance.classroom.id, lesson_id=instance.lesson.id,
                                                       student_id=st_id):
                instance.student = student
                form.save()

                messages.success(request, 'Lesson for this student added successfully')
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'You had selected this lesson with this class later')
                form = SelectLesson()
                return render(request, 'my_university/select_lesson.html', context={'form': form})

    else:
        form = SelectLesson()
    return render(request, 'my_university/select_lesson.html', context={'form': form})


def edit_profile(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully edit')
            return HttpResponseRedirect('/')
    else:
        form = StudentForm(instance=student)
    return render(request, 'my_university/new_student.html', context={'form': form})


def search(request):
    if request.method == 'POST':
        input = request.POST.get('search')
        result = Class_Lesson_Student.objects.filter(
            Q(classroom__name__contains=input) | Q(lesson__name__contains=input)).values('lesson_id','lesson__name').distinct()
        if result:
            return render(request, 'my_university/lesson_student.html', context={'classes': result})
        else:
            messages.error(request, 'Not found')
            return render(request, 'my_university/home.html')

def all_students(request,teacher_id):

    try:
        staff = get_object_or_404(Staff,id=teacher_id)
    except:
        classroom = Class_Lesson_Student.objects.filter(lesson__teacher_id=teacher_id).values('student__last_name','student__name','student_id').distinct()
    else:
        classroom = Class_Lesson_Student.objects.filter(Q(lesson__teacher_id=teacher_id )|Q(student__faculty_id=staff.faculty.id)).values('student__last_name','student__name','student_id').distinct()
    return render(request,'my_university/all_students.html',context={'classes':classroom})

def student_all_lessons(request,student_id):
    classroom = Class_Lesson_Student.objects.filter(student_id=student_id)
    return render(request, 'my_university/edit_student_lessons.html', context={'classes':classroom})


@login_required
@permission_required('my_university.delete_class_lesson_student',raise_exception=True)
def edit_student_lesson(request,lesson_id,student_id):
    Class_Lesson_Student.objects.filter(lesson_id=lesson_id,student_id=student_id).delete()
    classroom = Class_Lesson_Student.objects.filter(student_id=student_id)
    return render(request, 'my_university/edit_student_lessons.html', context={'classes':classroom})