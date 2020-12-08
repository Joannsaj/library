from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_librarian = models.BooleanField('librarian status', default=False)
    is_student = models.BooleanField('student status', default=False)

