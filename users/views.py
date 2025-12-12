from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserSerializer, ShopSerializer
from .models import Shop


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Генерируем токены
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Регистрация прошла успешно!'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Вход пользователя"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Укажите имя пользователя и пароль'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({
                'error': 'Неверные учетные данные'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class LogoutView(APIView):
    """Выход пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Выход выполнен успешно'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Ошибка при выходе'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class MyShopView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование своего магазина (только для продавцов)"""
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.role != 'seller':
            return Response({'error': 'У вас нет магазина'}, status=status.HTTP_403_FORBIDDEN)
        return Shop.objects.get(owner=self.request.user)