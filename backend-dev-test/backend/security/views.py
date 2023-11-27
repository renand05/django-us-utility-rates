from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from security.models import CustomUser

class SignUpForm(UserCreationForm):
   class Meta:
      model = CustomUser   
      fields = ('username', 'email', 'password1', 'password2',)


@authentication_classes([])
@permission_classes([])
class RegistrationView(APIView):
    def post(self, request) -> Response:
        form = SignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_201_CREATED)

        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request) -> Response:
        response = super().post(request)
        if response.status_code == status.HTTP_200_OK:
            refresh = response.data.get('refresh')
            access = response.data.get('access')
            user_id = self.request.user.id if self.request.user else None
            response.data.update({
                'user_id': user_id,
                'refresh': refresh,
                'access': access,
            })

        return response

@authentication_classes([])
@permission_classes([])
class CustomTokenRefreshView(APIView):
    def post(self, request) -> Response:
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
    def post(self, request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
