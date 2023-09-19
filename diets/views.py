from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from . import serializers
from .models import Diet

class Diet(APIView):
    def get_object(self, pk):
        try:
            return Diet.objects.get(pk=pk)
        except Diet.DoesNotExist:
            return NotFound
    
    # 날짜별 식단 가져오기
    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.DietSerializer(perk)
        return Response(serializer.data)
    
    # 당일 식단 저장 및 평점
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
    
    # 한줄 평가 입력
    def put(self, request, pk):
        diet = self.get_object(pk)
        serializer = serializers.DietReviewSerializer(
            diet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_diet = serializer.save()
            return Response(serializers.DietReviewSerializer(updated_diet).data)
        else:
            return Response(serializer.errors)
