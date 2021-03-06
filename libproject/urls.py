"""libproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from libapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/librarian/', views.LibrarianSignUpView.as_view(), name='librarian_signup'),
    path('accounts/logsout/', auth_views.LogoutView.as_view(next_page = '/accounts/login/'), name='logout'),
    path('',views.index, name='index'),
    path('library',views.library, name='library'),
    path('book',views.book, name='book'),
    path('borrow',views.borrow, name='borrow'),
    path('view_books', views.view_books, name='view_books'),
    path('search', views.search_results, name= 'search'),
    path('book/<int:book_id>', views.get_book, name='get_book'),
    path('borrowed', views.borrowed_books, name='borrowed'),
    # path('return/<int:book_id>',views.return_book, name='return'),
    # path('returned', views.returned_books, name='returned',)
]
