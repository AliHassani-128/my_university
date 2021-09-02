from django import forms
from .models import Book, Rental


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        exclude = ('student',)

    def __init__(self, *args, **kwargs):
        super(RentalForm, self).__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(status=True)



