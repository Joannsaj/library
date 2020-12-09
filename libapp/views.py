from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from .models import User
from .forms import StudentSignUpForm, LibrarianSignUpForm, LibraryForm, BooksForm, BorrowForm
from django.contrib.auth import login

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class LibrarianSignUpView(CreateView):
    model = User
    form_class = LibrarianSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'librarian'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('library')

def index(request):
    return render(request,'index.html')

def library(request):    
    if request.method == 'POST':
        form = LibraryForm(request.POST,request.FILES)
        if form.is_valid() :
            library = form.save(commit=False)
            library.librarian = request.user
            library.save()
            return redirect('book')
    else:
        form = LibraryForm()
    return render(request,'library.html',{"form":form})

def book(request):    
    if request.method == 'POST':
        form = BooksForm(request.POST,request.FILES)
        if form.is_valid() :
            book = form.save(commit=False)
            book.librarian = library
            book.save()
            return redirect('index')
    else:
        form = BooksForm()
    return render(request,'book.html',{"form":form})

def borrow(request):    
    if request.method == 'POST':
        form = BorrowForm(request.POST,request.FILES)
        if form.is_valid() :
            borrow = form.save(commit=False)
            borrow.borrower = request.user
            borrow.save()
            return redirect('index')
    else:
        form = BorrowForm()
    return render(request,'borrow.html',{"form":form})
