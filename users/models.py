from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    ID = models.CharField(max_length=30, unique=True)
    password = 
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    email = models.EmailField(max_length=100)
