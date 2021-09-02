from django.shortcuts import render

# Create your views here.
from library.forms import RentalForm
from library.models import Rental, Book
from my_university.models import Student


def rent_book(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.student = Student.objects.get(id=request.user.id)
            book = form.cleaned_data['book']
            book.status = False
            book.save()
            form.save()
            return render(request,'library/student_rental_book.html',context={'rentals':Rental.objects.filter(student_id=request.user.id)})
    form = RentalForm()
    return render(request,'library/rent_book.html',context={'form':form})

def show_books(request):
    rentals = Rental.objects.filter(student_id=request.user.id)
    if rentals:
        return render(request,'library/student_rental_book.html',context={'rentals':rentals})

