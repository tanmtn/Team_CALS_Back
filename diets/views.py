from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers


class Diet(APIView):
    def post(self, request):
        diet_serializer = serializers.DietSerializer(data=request.data)
        if diet_serializer.is_valid():
            user_data = diet_serializer.validated_data
            daily_calorie_rating = diet_serializer.get_daily_rating(user_data)
            diet = diet_serializer.save()
            return Response(
                {
                    "diet": serializers.DietSerializer(diet).data,
                    "daily_rating": daily_calorie_rating,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
