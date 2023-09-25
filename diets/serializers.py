from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import DietList, SelectedDiet
from math import floor
from django.db.models import Sum


class DietSerializer(ModelSerializer):
    daily_rating = SerializerMethodField()

    class Meta:
        model = DietList
        fields = "__all__"

    def get_daily_rating(self, user):
        created_date = user.created_date
        daily_total_calorie = DietList.daily_total_calorie(created_date)
        meal_calorie = user.meal_calorie
        recommended_calorie = user.user.recommended_calorie

        total_calorie = daily_total_calorie + meal_calorie

        if total_calorie <= recommended_calorie:
            return 5.0

        calorie_difference = total_calorie - recommended_calorie
        rating = 5.0 - floor(calorie_difference / 100) * 0.5
        return max(0.0, rating)


class DietReviewSerializer(ModelSerializer):
    class Meta:
        model = DietList
        fields = (
            "daily_review",
            "created_date",
            "created_time",
            "updated_at",
        )


class SelectedDietSerializer(ModelSerializer):
    class Meta:
        model = SelectedDiet
        fields = "__all__"

        def daily_total_calorie(self, created_date):
            total_rating = self.objects.filter(created_date=created_date).aggregate(
                Sum("meal_calorie")
            )["meal_calorie__sum"]
            if total_rating is None:
                total_rating = 0
            return total_rating
