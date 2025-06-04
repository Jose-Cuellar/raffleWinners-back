from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import MinLengthValidator
from .models import User

# Serializer para el registro de usuarios
class UserCreateSerializer(serializers.ModelSerializer):
    document_number = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="El número de cédula ingresado ya está registrado."),
            MinLengthValidator(8, message="El campo 'Número de cédula' debe tener al menos 8 caracteres.")
        ]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="El correo electrónico ya está registrado.")]
    )
    name = serializers.CharField(
        validators=[MinLengthValidator(4, message="El campo 'Nombres' debe tener al menos 4 caracteres.")]
    )
    password = serializers.CharField(
        validators=[MinLengthValidator(8, message="La contraseña debe tener al menos 8 caracteres.")]
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'document_number', 'email', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'is_staff': {
                'read_only': True
            },
            'is_superuser': {
                'read_only': True
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
# Serializer para obtener el listado de usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']

# Serializer para editar la información de los usuarios
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'email', 'is_active']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance