from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . import serializers
from .models import DietList


class DietView(APIView):
    def get(self, request):
        diets = DietList.objects.filter(user=request.user, created_date=request.created_date)
        serializer = serializers.DietSerializer(diets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 당일 식단 저장 및 평점
    def post(self, request):
        serializer = serializers.DietSerializer(data=request.data)
        if serializer.is_valid():
            diet = serializer.save()
            return Response(
                {"diet": serializers.DietSerializer(diet).data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PutDiet(APIView):
    def get(self, request, pk):
        try:
            diet = DietList.objects.get(pk=pk)
            serializer = serializers.DietSerializer(diet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except diet.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 한줄 평가 입력
    def put(self, request, pk):
        diet = DietList.objects.get(pk=pk)
        serializer = serializers.DietReviewSerializer(
            diet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_diet = serializer.save()
            return Response(
                serializers.DietReviewSerializer(updated_diet).data,
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, pk):
        diets = DietList.objects.get(pk=pk)
        diet.delete()
