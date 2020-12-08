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
        return self.name
