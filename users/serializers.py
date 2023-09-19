from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User


class UserSerializer(ModelSerializer):
    recommended_calorie = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "is_active",
            "email",
            "age",
            "gender",
            "height",
            "weight",
            "activity",
            "recommended_calorie",
        )

    def get_recommended_calorie(self, user_data):
        age = user_data.get("age")
        height = user_data.get("height")
        weight = user_data.get("weight")
        gender = user_data.get("gender")
        activity = user_data.get("activity")

        activity_coefficients = {
            "lowest": 1.0,
            "low": 1.11,
            "middle": 1.25,
            "high": 1.48,
            "female_lowest": 1.0,
            "female_low": 1.12,
            "female_middle": 1.27,
            "female_high": 1.45,
        }

        if gender == "male":
            recommended_calorie = activity_coefficients.get(activity, 1.0) * (
                (6.25 * height) + (10 * weight) - (5 * age) + 5
            )
        else:
            recommended_calorie = activity_coefficients.get(
                f"female_{activity}", 1.0
            ) * ((6.25 * height) + (10 * weight) - (5 * age) - 161)
        return recommended_calorie
