import random

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail

from ytasks import settings
from .email import Email
from .models import User
from .serializers import UserSerializer


class RegisterUser(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            Email.Builder().setEmail(user.email).setTitle(
                'Вы успешно зарегестрировались!'
            ).addDescriptionLine(
                'Спасибо'
            ).addDescriptionLine(
                'Теперь вы можете посетить наш сайт: http://localhost:3000/'
            ).build().send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Me(APIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ResetRequest(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        reset_token = random.randrange(0, 10000000)
        user = get_object_or_404(User, email=request.data['email'])

        Email.Builder().setEmail(request.data['email']).setTitle(
            "Восстановление пароля"
        ).addDescriptionLine(
            "Для восстановления перейдите по ссылке"
        ).addDescriptionLine(
            "http://localhost:3000/reset/" + str(reset_token)
        ).build().send()

        user.reset_token = reset_token
        user.save()

        return Response()


class Reset(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        user = get_object_or_404(User, reset_token=request.data['token'])

        user.set_password(request.data['password'])
        user.reset_token = None
        user.save()

        return Response()


class UpdateEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        new_email = request.data.get('email')

        if not new_email:
            return Response({'error': 'Еmail обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, не занят ли email другим пользователем
        if User.objects.filter(email=new_email).exclude(id=user.id).exists():
            return Response({'error': 'Такая почта уже занята'}, status=status.HTTP_400_BAD_REQUEST)

        user.email = new_email
        user.save()

        return Response({'email': new_email}, status=status.HTTP_200_OK)
