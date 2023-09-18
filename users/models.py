from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "남")
        FEMALE = ("female", "여")

    class ActivityLevelChoices(models.TextChoices):
        LOWEST = ("lowest", "비활동적")
        LOW = ("low", "저활동적")
        MIDDLE = ("middle", "활동적")
        HIGH = ("high", "매우 활동적")

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    gender = models.CharField(
        max_length=30,
        choices=GenderChoices.choices,
    )

    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    activity = models.CharField(
        max_length=30,
        choices=ActivityLevelChoices.choices,
        default="lowest",
    )
