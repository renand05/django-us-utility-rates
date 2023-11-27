from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest

from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from pydantic import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from security.models import CustomUser

class RefreshTokenModel(BaseModel):
    token_type: str
    exp: int
    iat: int
    jti: str
    user_id: int

class SignUpForm(UserCreationForm):
   class Meta:
      model = CustomUser   
      fields = ('username', 'email', 'password1', 'password2',)


@authentication_classes([])
@permission_classes([])
class RegistrationView(APIView):
    def post(self, request: HttpRequest) -> Response:
        form = SignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_201_CREATED)

        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: HttpRequest) -> Response:
        response = super().post(request)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = RefreshToken(response.data.get('refresh'))
            refresh_token_model = RefreshTokenModel.model_validate(refresh_token.payload)
            access = response.data.get('access')
            user_id = refresh_token_model.user_id
            response.data.update({
                'user_id': user_id,
                'refresh': response.data.get('refresh'),
                'access': access,
            })

        return response

@authentication_classes([])
@permission_classes([])
class CustomTokenRefreshView(APIView):
    def post(self, request: HttpRequest) -> Response:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            user_id = refresh.payload.get('user_id')
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user_id': user_id,
            'access': access_token,
        })


@authentication_classes([])
@permission_classes([])
class LoginView(APIView):
    def post(self, request: HttpRequest) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
