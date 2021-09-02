from django.contrib import admin

# Register your models here.
from library.models import Book, Rental

admin.site.register(Book)
admin.site.register(Rental)

