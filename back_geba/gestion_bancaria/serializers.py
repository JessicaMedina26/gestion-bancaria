from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Departamento, Ciudad, Persona, Cliente, Cuenta, Movimiento


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'id': self.user.id})
        data.update({'username': self.user.username})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'email': self.user.email})
        data.update({'is_superuser': self.user.is_superuser})

        if Cliente.objects.filter(persona=self.user.id).exists():
            try:
                item_cliente = Cliente.objects.get(persona=self.user.id)
            except Cliente.DoesNotExist:
                item_cliente = None
            data.update({'id_cliente': item_cliente.id_cliente})
        else:
            data.update({'id_cliente': None})
        return data

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


class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = '__all__'


class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'
