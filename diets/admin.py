from django.contrib import admin
from .models import DietList


@admin.register(DietList)
class DietAdmin(admin.ModelAdmin):
    list_display = (
        "created_date",
        "created_time",
        "user",
        "meal_category",
        "food_name",
        "food_calorie",
        "meal_calorie",
        "daily_total_calorie",
        "daily_review",
    )

    list_filter = (
        "created_date",
        "meal_category",
    )
