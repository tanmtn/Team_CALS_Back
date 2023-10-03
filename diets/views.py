from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . import serializers
from .models import DietList, SelectedDiet


# class SelectedDietView(APIView):
# def get(self, request):
#     all_selected_diet = SelectedDiet.objects.all()
#     serializer = serializers.SelectedDietSerializer(all_selected_diet, many=True)
#     return Response(serializer.data)

# def post(self, request):
#     serializer = serializers.SelectedDietSerializer(data=request.data["selected_diets"])
#     if serializer.is_valid():
#         diets = request.data["selected_diets"]
#         selected_diet_ids = []
#         for diet in diets :
#             selectedDiet, created = SelectedDiet.objects.get_or_create(
#                 food_name = diets['food_name'],
#                 defaults={'food_calorie' : diets['food_calorie'], 'food_gram': diets['food_gram']}
#             )
#             print(selectedDiet, created)
#             selected_diet_ids.append(selectedDiet.id)
#         if not created:
#             selectedDiet.save()
#             return Response(status=status.HTTP_200_OK)
#         selected_diet = serializer.save()
#         return Response(serializers.SelectedDietSerializer(selected_diet).data, status=status.HTTP_200_OK)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DietView(APIView):
    # def get(self, request):
    #     specific_date = request.query_params.get("created_date", "")
    #     diets = DietList.objects.filter(user=request.user, created_date=specific_date)
    #     serializer = serializers.DietSerializer(diets, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        all_diet_list = DietList.objects.all()
        serializer = serializers.DietSerializer(all_diet_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 당일 식단 저장 및 평점
    def post(self, request):
        diet_serializer = serializers.DietSerializer(data=request.data["diets"])
        selected_serializer = serializers.SelectedDietSerializer(
            data=request.data["selected_diet"]
        )

        if diet_serializer.is_valid():
            selected_diets = request.data["selected_diet"]
            selected_diet_ids = []
            for diet in selected_diets:
                selectedDiet, created = SelectedDiet.objects.get_or_create(
                    food_name=diet["food_name"],
                    defaults={
                        "food_calorie": diet["food_calorie"],
                        "food_gram": diet["food_gram"],
                    },
                )
                selected_diet_ids.append(selectedDiet.id)
                diet.selected_diet.add(selected_diet_ids)

                selected_serializer.save(user=request.user)
                diet = diet_serializer.save(user=request.user)
        if created:
            return Response(diet_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(diet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = serializers.DietSerializer(
            diet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_diet = serializer.save()
            return Response(
                serializers.DietSerializer(updated_diet).data,
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        diets = DietList.objects.get(pk=pk)
        diets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
