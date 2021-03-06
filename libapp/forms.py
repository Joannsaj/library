from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from .models import User, Library, Books, Borrow, Return

class LibrarianSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_librarian = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        
        return user

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ('name','location',)                

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ('title','author','description','library')                        

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ('book',)    

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        exclude = ['book', 'date',]                   
