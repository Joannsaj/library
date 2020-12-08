from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from .models import User
from .forms import StudentSignUpForm, LibrarianSignUpForm
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
        return redirect('index')

def index(request):
    return render(request,'index.html')
