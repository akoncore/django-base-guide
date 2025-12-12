from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Shop

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Повторите пароль')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role', 'first_name', 'last_name', 'phone')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email уже используется."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # Если пользователь продавец, создаем магазин
        if user.role == 'seller':
            from django.utils.text import slugify
            Shop.objects.create(
                owner=user,
                name=f"Магазин {user.username}",
                slug=slugify(f"shop-{user.username}")
            )
        
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'avatar', 'created_at')
        read_only_fields = ('id', 'created_at')


class ShopSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    total_products = serializers.IntegerField(read_only=True)
    total_sold = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at')


class ShopListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка магазинов"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    total_products = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Shop
        fields = ('id', 'name', 'slug', 'logo', 'description', 'owner_username', 'total_products', 'is_active')