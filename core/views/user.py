from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from core.models import User
from core.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"message": "Usuário já existente!"}, status=status.HTTP_400_BAD_REQUEST)
    elif User.objects.filter(email=email).exists():
        return Response({"message": "Email já está sendo utilizado!"}, status=status.HTTP_400_BAD_REQUEST)

    if username and email and password:
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        response_data = {
            "message": "Usuário criado com sucesso!",
            "username": user.username,
            "email": user.email,
            "id": user.id,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Dados de usuário inválidos!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login(request):
    value = request.data.get("value")
    password = request.data.get("password")
    print("Value:", value)
    print("Password:", password)

    if value is not None and password is not None:
        try:
            user = User.objects.get(Q(username=value) | Q(email=value))
            user.save()
            print("Stored Password:", user.password)
            print("Password Check:", check_password(password, user.password))
            print("Is user active:", user.is_active)
            username = user.username
            print("User found in database:", username)

            user_auth = authenticate(username=username, password=password)
            print("Authentication result:", user_auth)

            if user_auth is not None:
                refresh = RefreshToken.for_user(user)
                access = AccessToken.for_user(user_auth)

                response_data = {
                    "refresh": str(refresh),
                    "access": str(access),
                    "username": user_auth.username,
                    "email": user_auth.email,
                    "id": user_auth.id,
                    "message": "Login realizado com sucesso!",
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                print("Authentication failed for the user")

        except User.DoesNotExist:
            user = None
            print("User not found in the database")

    else:
        return Response({"message": "Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST)

    print("Final user object:", user)

    return Response({"message": "Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST)
