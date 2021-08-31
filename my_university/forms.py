from django import forms
from .models import Student, Class_Lesson_Student


class StudentForm(forms.ModelForm):
    password = forms.CharField(max_length=100,widget=forms.PasswordInput())
    class Meta:
        model = Student
        fields = '__all__'

class SelectLesson(forms.ModelForm):
    class Meta:
        model = Class_Lesson_Student
        exclude = ('student',)




