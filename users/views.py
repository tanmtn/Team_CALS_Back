from rest_framework.views import APIView
from rest_framework.response import Response

# from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import serializers
from .models import User


class Signup(APIView):
    # 회원 정보 조회
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        return Response(
            serializers.UserSerializer(user).data, status=status.HTTP_200_OK
        )

    def post(self, request):
        user = serializers.UserSerializer(data=request.data)

        # id 중복 검사
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 회원가입
        if user.is_valid():
            user_data = user.validated_data
            recommended_calorie = user.get_recommended_calorie(user_data)
            user = User.objects.create_user(
                username=request.data["username"],
                password=request.data["password"],
                email=request.data["email"],
                gender=request.data["gender"],
                age=request.data["age"],
                height=request.data["height"],
                weight=request.data["weight"],
                activity=request.data["activity"],
            )
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
        return Response(
            {
                "user": serializers.UserSerializer(user).data,
                "recommended_calorie": recommended_calorie,
                "access": access_token,
                "refresh": refresh_token,
            },
            status=status.HTTP_201_CREATED,
        )

    # 회원 정보 수정(비밀번호, 키, 몸무게, 활동량)
    def put(self, request):
        serializer = serializers.UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 회원 탈퇴
class Withdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.is_active = False
            user.save()
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
