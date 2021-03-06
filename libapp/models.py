from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_librarian = models.BooleanField('librarian status', default=False)
    is_student = models.BooleanField('student status', default=False)

class Library(models.Model):
    librarian = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    location = models.CharField(max_length=60)

    def __str__(self):
        return self.librarian

class Books(models.Model):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=60)
    description = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)    

    @classmethod
    def search_book(cls,search_term ):
        return cls.objects.filter(title__icontains=search_term).all()

class Borrow(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book        

class Return(models.Model):
    returned_book = models.ForeignKey(Borrow, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date            