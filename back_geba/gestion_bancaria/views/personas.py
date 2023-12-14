# Create your views here.
from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt import serializers
from gestion_bancaria.models import Persona, Cliente
from gestion_bancaria.serializers import PersonaSerializer, ClienteSerializer, PersonaListSerializer


class ListPersonaView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.query_params:
            items = Persona.objects.filter(**request.query_params.dict())
        else:
            items = Persona.objects.filter(is_active=True)
        if items:
            serializer = PersonaListSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No se encontraron datos disponibles"}, status=status.HTTP_400_BAD_REQUEST)


class CreatePersonaView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        if Persona.objects.filter(username=request.data['username']).exists():
            return Response({"message": "Ya existe el nombre de usuario"}, status=status.HTTP_400_BAD_REQUEST)

        if Persona.objects.filter(nro_documento=request.data['nro_documento']).exists():
            return Response({"message": "Ya existe el nro. de documento"}, status=status.HTTP_400_BAD_REQUEST)

        if Persona.objects.filter(email=request.data['email']).exists():
            return Response({"message": "Ya existe el correo electrónico"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # verificamos para registrar o actualizar cliente
            if request.data['cliente'] is not None:
                request.data['cliente']['persona'] = serializer.data['id']
                try:
                    item_cliente = Cliente.objects.get(persona=serializer.data['id'])
                    serializer_cliente = ClienteSerializer(instance=item_cliente, data=request.data['cliente'])
                except Cliente.DoesNotExist:
                    serializer_cliente = ClienteSerializer(data=request.data['cliente'])

                # procesamos registro o actualizacion de cliente
                if serializer_cliente is not None and serializer_cliente.is_valid():
                    serializer_cliente.save()

            return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonaView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        if Persona.objects.filter(nro_documento=request.data['nro_documento']).exclude(pk=pk).exists():
            return Response({"message": "Ya existe el nro. de documento"}, status=status.HTTP_400_BAD_REQUEST)

        if Persona.objects.filter(email=request.data['email']).exclude(pk=pk).exists():
            return Response({"message": "Ya existe el correo electrónico"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            return Response({"message": "No se pudo identificar la Persona"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonaSerializer(instance=item, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # verificamos para registrar o actualizar cliente
            if request.data['cliente'] is not None:
                request.data['cliente']['persona'] = serializer.data['id']
                try:
                    item_cliente = Cliente.objects.get(persona=pk)
                    serializer_cliente = ClienteSerializer(instance=item_cliente, data=request.data['cliente'])
                except Cliente.DoesNotExist:
                    serializer_cliente = ClienteSerializer(data=request.data['cliente'])

                # procesamos registro o actualizacion de cliente
                if serializer_cliente is not None and serializer_cliente.is_valid():
                    serializer_cliente.save()

            return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePersonaView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            item = Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            return Response({"message": "No se pudo identificar la Persona"}, status=status.HTTP_400_BAD_REQUEST)

        item.is_active = False
        item.save()
        return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
