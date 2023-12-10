from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Departamento, Ciudad, Persona, Cliente


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['nro_documento'] = user.nro_documento
        return token


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'


class PersonaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'tipo_documento', 'nro_documento', 'email', 'first_name', 'last_name', 'username', 'password',
                  'celular', 'direccion', 'ciudad', 'is_staff', 'is_active', 'is_superuser', 'cliente')


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data['password'] is not None:
            instance.set_password(validated_data['password'])

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.celular = validated_data['celular']
        instance.direccion = validated_data['direccion']
        instance.tipo_documento = validated_data['tipo_documento']
        instance.nro_documento = validated_data['nro_documento']
        instance.ciudad = validated_data['ciudad']
        instance.save()
        return instance


class ClienteListSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = ('id_cliente', 'calificacion', 'fecha_ingreso', 'persona')


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
