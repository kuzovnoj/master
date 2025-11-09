from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import RegisterAPIView

app_name = "users"


urlpatterns = [
        path('login/', views.LoginUser.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('register/', views.RegisterUser.as_view(), name='register'),
        path('profile/', views.ProfileUser.as_view(), name='profile'),
        path('', RegisterAPIView.as_view(), name='registration'),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]