from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import DietList, SelectedDiet
from math import floor
from django.db.models import Sum


class CalculationMixin:
    def rating_calculation(self, user):
        daily_total_calorie = DietList.objects.filter(created_date=user.created_date)
        meal_calorie = user.meal_calorie
        recommended_calorie = user.user.recommended_calorie

        total_calorie = daily_total_calorie + meal_calorie

        if total_calorie <= recommended_calorie:
            return 5.0

        calorie_difference = total_calorie - recommended_calorie
        rating = 5.0 - floor(calorie_difference / 100) * 0.5
        return max(0.0, rating)

    def daily_calorie_sum(self, created_date):
        total_rating = self.objects.filter(created_date=created_date).aggregate(
            Sum("meal_calorie")
        )["meal_calorie__sum"]
        if total_rating is None:
            total_rating = 0
        return total_rating


class DietSerializer(ModelSerializer, CalculationMixin):
    daily_rating = SerializerMethodField()

    class Meta:
        model = DietList
        fields = "__all__"


class DietReviewSerializer(ModelSerializer, CalculationMixin):
    class Meta:
        model = DietList
        fields = (
            "daily_review",
            "created_date",
            "created_time",
            "updated_at",
        )


class SelectedDietSerializer(ModelSerializer, CalculationMixin):
    class Meta:
        model = SelectedDiet
        fields = "__all__"
