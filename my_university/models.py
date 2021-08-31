from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class Staff(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    user = None
    def save(self,*args,**kwargs):
        self.user = User.objects.create_user(username=self.name, password=self.password)
        self.user.is_staff = True
        permission = Permission.objects.get(name='Can delete class_ lesson_ student')
        self.user.user_permissions.add(permission)
        self.id = self.user.id
        self.user.save()
        super(Staff, self).save(*args, **kwargs)




class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='teacher_img',null=True,blank=True)
    user = None

    def save(self, *args, **kwargs):
        self.user = User.objects.create_user(username=self.name, password=self.password)
        self.user.is_staff = True
        permission = Permission.objects.get(name='Can delete class_ lesson_ student')
        self.user.user_permissions.add(permission)
        self.id = self.user.id
        self.user.save()
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'





class Student(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='student_img',null=True,blank=True)
    user = None
    def save(self,*args,**kwargs):
        self.user = User.objects.create_user(username=self.name,password=self.password)
        self.user.is_staff = True
        permission = Permission.objects.get(name='Can add student')
        self.user.user_permissions.add(permission)
        self.id = self.user.id
        self.user.save()

        super(Student,self).save(*args,**kwargs)

    def __str__(self):
        return f'{self.name} --{self.last_name} -- {self.major} -- {self.faculty.name}'



class Lesson(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'




class Class(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    ACTIVE = True
    DEACTIVE = False
    class_status = (
        (ACTIVE,'Active'),
        (DEACTIVE,'Deactive'),
    )
    status = models.BooleanField(choices=class_status,default=ACTIVE)

    def __str__(self):
        return f'{self.name}'


class Class_Lesson_Student(models.Model):
    classroom = models.ForeignKey(Class,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)


