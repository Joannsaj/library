from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from .models import User, Books, Borrow, Return
from .forms import StudentSignUpForm, LibrarianSignUpForm, LibraryForm, BooksForm, BorrowForm, ReturnForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .decorators import student_required, librarian_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

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
        return redirect('view_books')

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

# def index(request):
#     return render(request,'index.html')

@login_required(login_url='/accounts/login/')
@librarian_required
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

@login_required(login_url='/accounts/login/')
@librarian_required
def book(request):    
    if request.method == 'POST':
        form = BooksForm(request.POST,request.FILES)
        if form.is_valid() :
            book = form.save(commit=False)
            book.librarian = library
            book.save()
            return redirect('view_books')
    else:
        form = BooksForm()
    return render(request,'book.html',{"form":form})

@login_required(login_url='/accounts/login/')
@student_required
def borrow(request):    
    if request.method == 'POST':
        form = BorrowForm(request.POST,request.FILES)
        if form.is_valid() :
            borrow = form.save(commit=False)
            borrow.borrower = request.user
            borrow.save()
            return redirect('view_books')
    else:
        form = BorrowForm()
    return render(request,'borrow.html',{"form":form})

@login_required(login_url='/accounts/login/')
def view_books(request):
    books = Books.objects.all()
    return render(request,'view_books.html',{"books":books})

@login_required(login_url='/accounts/login/')
@librarian_required
def borrowed_books(request):
    books = Borrow.objects.all()
    return render(request,'borrowed_books.html',{"books":books})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if "book" in request.GET and request.GET["book"]:
        search_term = request.GET.get("book")
        books = Books.search_book(search_term)
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"books": books})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

@login_required(login_url='/accounts/login/')
@student_required
def get_book(request, book_id):
    try:
        book = Books.objects.get(id = book_id)
        if request.method == 'POST':
            form = BorrowForm(request.POST,request.FILES)
            if form.is_valid() :
                borrow = form.save(commit=False)
                borrow.borrower = request.user
                borrow.title = book.title
                borrow.save()
                return redirect('view_books')
        else:
            form = BorrowForm()
        
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"details.html", {"book":book,  "form":form, })

@login_required(login_url='/accounts/login/')
@librarian_required
def return_book(request, book_id):
    try:
        borrowed = Borrow.objects.get(id = book_id)
        if request.method == 'POST':
            form = ReturnForm(request.POST,request.FILES)
            if form.is_valid() :
                returned = form.save(commit=False)
                returned.book = borrowed.book
                returned.save()
                return redirect('borrowed')
        else:
            form = ReturnForm()
        
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"return.html", {"borrowed":borrowed,  "form":form, })

@login_required(login_url='/accounts/login/')
@librarian_required    
def returned_books(request):
    books = Return.objects.all()
    return render(request,'returned_books.html',{"books":books})