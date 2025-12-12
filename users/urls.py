from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users_api'

urlpatterns = [
    # Аутентификация
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Профиль
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('my-shop/', views.MyShopView.as_view(), name='my_shop'),
]