from django.urls import path
from .views import rent_book , show_books

app_name = 'library'
urlpatterns = [

    path('rent-book/',rent_book,name='rent_book'),
    path('show-books/',show_books,name='show_books'),

]