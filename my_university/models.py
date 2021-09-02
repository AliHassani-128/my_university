from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models

from University import settings



# Create your models here.



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    email = None
    phone = models.IntegerField('Phone number', unique=True)
    image = models.FileField(upload_to='user_image')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.username



class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class Staff(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    user = None
    # user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # user = CustomUser.objects.create_user(username=name, password=str(password),phone=int(phone))
    def save(self,*args,**kwargs):
        self.user = CustomUser.objects.create_user(username=self.name, password=self.password, phone=self.phone)
        # self.user = User.objects.create_user(username=self.name, password=self.password,phone=self.phone)
        self.user.is_staff = True
        permission = Permission.objects.get(name='Can delete class_ lesson_ student')
        permission2 = Permission.objects.get(name='Can add student')
        self.user.user_permissions.set([permission,permission2])
        self.id = self.user.id
        self.user.save()
        super(Staff, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.name}'





class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='teacher_img',null=True,blank=True)
    phone = models.CharField(max_length=20)
    user=None
    # user = CustomUser.objects.create_user(username=name, password=str(password),phone=int(phone))
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        self.user = CustomUser.objects.create_user(username=self.name, password=self.password,phone=self.phone)
        self.user.is_staff = True
        permission = Permission.objects.get(name='Can delete class_ lesson_ student')
        self.user.user_permissions.add(permission)
        self.id = self.user.id
        self.user.save()
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Major(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return f'{self.name}'




class Student(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    major = models.ForeignKey(Major,on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='student_img',null=True,blank=True)
    phone = models.CharField(max_length=20)
    user = None
    # user = CustomUser.objects.create_user(username=name, password=str(password),phone=int(phone))
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def save(self,*args,**kwargs):
        self.user = CustomUser.objects.create_user(username=self.name, password=self.password, phone=self.phone)
        # self.user = User.objects.create_user(username=self.name,password=self.password,phone=self.phone)
        self.user.is_staff = True
        # permission = Permission.objects.get(name='Can add student')
        permission = Permission.objects.get(name='Can add rental')
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


