from rest_framework.serializers import ModelSerializer, SerializerMethodField
from math import floor
from django.db.models import Sum
from .models import DietList, SelectedDiet
from users.models import User
from users.serializers import UserSerializer
from . import serializers


class SelectedDietSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedDiet
        fields = (
            "food_name",
            "food_calorie",
        )


# class CalculationMixin:
    # def rating_calculation(self, user):
    #     daily_total_calorie = DietList.objects.filter(created_date=user.created_date)
    #     meal_calorie = user.meal_calorie
    #     recommended_calorie = user.user.recommended_calorie

    #     total_calorie = daily_total_calorie + meal_calorie

    #     if total_calorie <= recommended_calorie:
    #         return 5.0

    #     calorie_difference = total_calorie - recommended_calorie
    #     rating = 5.0 - floor(calorie_difference / 100) * 0.5
    #     return max(0.0, rating)

    # def daily_calorie_sum(self, created_date):
    #     total_rating = self.objects.filter(created_date=created_date).aggregate(
    #         Sum("meal_calorie")
    #     )["meal_calorie__sum"]
    #     if total_rating is None:
    #         total_rating = 0
    #     return total_rating


class DietSerializer(serializers.ModelSerializer):
    daily_star_rating = serializers.SerializerMethodField()
    daily_calorie_sum = serializers.SerializerMethodField()
    user = serializers.UserSerializer()

    class Meta:
        model = DietList
        fields = (
            "meal_category",
            "meal_calorie",
            "daily_review",
            "selected_diet",
            "created_date",
            "created_time",
            "updated_at",
            "daily_star_rating",
            "daily_calorie_sum",
            "user",
        )

    def get_daily_star_rating(self, diets):
        daily_total_calorie = DietList.objects.filter(created_date=diets.created_date)
        meal_calorie = diets.meal_calorie
        recommended_calorie = diets.recommended_calorie

        total_calorie = daily_total_calorie + meal_calorie

        if total_calorie <= recommended_calorie:
            return 5.0

        calorie_difference = total_calorie - recommended_calorie
        rating = 5.0 - floor(calorie_difference / 100) * 0.5
        return max(0.0, rating)

    def get_daily_calorie_sum(self, created_date):
        total_rating = self.objects.filter(created_date=created_date).aggregate(
            Sum("meal_calorie")
        )["meal_calorie__sum"]
        if total_rating is None:
            total_rating = 0
        return total_rating


# class DietReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DietList
#         fields = (
#             "daily_review",
#             "created_date",
#             "created_time",
#             "updated_at",
#         )


# class SelectedDietSerializer(serializers.ModelSerializer, CalculationMixin):
#     class Meta:
#         model = SelectedDiet
#         fields = "__all__"
