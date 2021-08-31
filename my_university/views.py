from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .forms import StudentForm, SelectLesson
from .models import *


# Create your views here.
def home(request):
    return render(request, 'my_university/home.html')




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
    find_class = Class_Lesson_Student.objects.filter(classroom_id=class_id).order_by('lesson_id')
    context = {'classes': find_class}
    return render(request, 'my_university/lesson_student.html', context=context)





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
                return HttpResponseRedirect('login/')

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
            Q(classroom__name__contains=input) | Q(lesson__name__contains=input))
        if result:
            return render(request, 'my_university/lesson_student.html', context={'classes': result})
        else:
            messages.error(request, 'Not found')
            return render(request, 'my_university/home.html')

def all_students(request):
    students = Student.objects.all()
    return render(request,'my_university/all_students.html',context={'students':students})

def student_all_lessons(request,student_id):
    classroom = Class_Lesson_Student.objects.filter(student_id=student_id)
    return render(request, 'my_university/edit_student_lessons.html', context={'classes':classroom})


@login_required
@permission_required('my_university.delete_class_lesson_student',raise_exception=True)
def edit_student_lesson(request,lesson_id,student_id):
    Class_Lesson_Student.objects.filter(lesson_id=lesson_id,student_id=student_id).delete()
    classroom = Class_Lesson_Student.objects.filter(student_id=student_id)
    return render(request, 'my_university/edit_student_lessons.html', context={'classes':classroom})