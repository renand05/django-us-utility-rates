from django.contrib import admin
from django.urls import path
from utilities import views as utilitiesViews
from security import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', utilitiesViews.RatesDemoView.as_view(), name='rates_demo'),
    path('register', authViews.RegistrationView.as_view(), name='register'),
    path('token', authViews.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', authViews.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('login', authViews.LoginView.as_view(), name='login')
]
