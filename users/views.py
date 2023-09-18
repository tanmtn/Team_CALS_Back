from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import User

class Signup(APIView):
    def post(self, request):
        user = UserSerializer(data=request.data)
        print(request.data)

        if user.is_valid():
            user = User.create_user(
                username = request.data["username"],
                password = request.data["password"],
                email = request.data["email"],
                age = request.data["age"],
                gender = request.data["gender"],
                height = request.data["height"],
                weight = request.data["weight"],
                activity = request.data["activity"],
            )