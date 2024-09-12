from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

#
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True}}
        
class UserLoginSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'is_staff']
 
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    # Validar la contraseña anterior
    def validate_old_password(self, value):
        user = self.context['request'].user  # Acceder al usuario autenticado
        if not user.check_password(value):  # Verificar la contraseña
            raise serializers.ValidationError("La contraseña anterior no es correcta")
        return value
