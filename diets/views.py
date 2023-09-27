from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . import serializers
from .models import DietList, SelectedDiet


class SelectedDietView(APIView):
    def get(self, request):
        all_selected_diet = SelectedDiet.objects.all()
        serializer = serializers.SelectedDietSerializer(all_selected_diet, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.SelectedDietSerializer(data=request.data)
        if serializer.is_valid():
            selected_diet = serializer.save()
            return Response(serializers.SelectedDietSerializer(selected_diet).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectedDietDetail(APIView):
    def get_object(self, pk):
        try:
            return SelectedDiet.objects.get(pk=pk)
        except SelectedDiet.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        selected_diet = self.get_object(pk)
        serializer = serializers.SelectedDietSerializer(selected_diet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        selected_diet = self.get_object(pk)
        serializer = serializers.SelectedDietSerializer(
            selected_diet,
            data=request.data,
            partial=True,
        )  # 부분 수정 가능하도록 partial true
        if serializer.is_valid():
            updated_selected_diet = serializer.save()
            return Response(serializers.SelectedDietSerializer(updated_selected_diet).data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        selected_diet = self.get_object(pk)
        selected_diet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DietView(APIView):
    def get(self, request):
        created_date = request.query_params.get("created_date", "")
        diets = DietList.objects.filter(user=request.user, created_date=created_date)
        serializer = serializers.DietSerializer(diets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 당일 식단 저장 및 평점
    def post(self, request):
        serializer = serializers.DietSerializer(data=request.data)
        if serializer.is_valid():
            diet = serializer.save(user=request.user)
            selected_diets = request.data.get("selected_diet")
            for selected_diet_pk in selected_diets:
                try:
                    selected_diet = SelectedDiet.objects.get(pk=selected_diet_pk)
                except SelectedDiet.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                diet.selected_diet.add(selected_diet)
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
