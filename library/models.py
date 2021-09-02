from django.db import models

# Create your models here.
from my_university.models import Major, Student


class Book(models.Model):
    name = models.CharField(max_length=100)
    major = models.ForeignKey(Major,on_delete=models.CASCADE)
    ACTIVE = True
    DEACTIVE = False
    book_status = (
        (ACTIVE, 'Active'),
        (DEACTIVE, 'Deactive'),
    )
    status = models.BooleanField(choices=book_status, default=ACTIVE)

    def __str__(self):
        return f'{self.name}'

class Rental(models.Model):
    student = models.ForeignKey(Student,on_delete=models.RESTRICT)
    book = models.ForeignKey(Book,on_delete=models.RESTRICT)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self,*args,**kwargs):
        self.book.status = False
        super(Rental,self).save(*args,**kwargs)

    def __str__(self):
        return f'{self.book.name} -- {self.student.name}'


