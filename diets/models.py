from django.db import models
from common.models import CommonModel
from django.db.models import Sum


class Diet(CommonModel):
    """식단 모델"""

    class MealCategoryChoices(models.TextChoices):
        BREAKFAST = ("breackfast", "아침")
        LUNCH = ("lunch", "점심")
        DINNER = ("dinner", "저녁")
        SNACK = ("snack", "간식")
        NIGHT_SNACK = ("night_snack", "야식")
        DRINK = ("drink", "음료")

    meal_category = models.CharField(
        max_length=30,
        choices=MealCategoryChoices.choices,
    )  # 식사 종류(아/점/저/간/야/음)
    food_name = models.CharField(max_length=200)  # 음식명
    food_calorie = models.PositiveIntegerField()  # 음식당 칼로리
    meal_calorie = models.PositiveIntegerField()  # 식사당 총 칼로리
    daily_review = models.TextField(null=True,blank=True,)


    def daily_total_calorie(cls,created_date):
        total_rating = cls.objects.filter(created_date=created_date).aggregate(Sum('meal_calorie'))['meal_calorie__sum']
        if total_rating is None:
            total_rating = 0
        return total_rating