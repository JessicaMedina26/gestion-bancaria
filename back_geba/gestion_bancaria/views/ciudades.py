# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from gestion_bancaria.serializers import CiudadSerializer
from gestion_bancaria.models import Ciudad


class ListCiudadView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.query_params:
            items = Ciudad.objects.filter(**request.query_params.dict())
        else:
            items = Ciudad.objects.filter(estado=True)

        if items:
            serializer = CiudadSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No se encontraron datos disponibles"}, status=status.HTTP_400_BAD_REQUEST)


class CreateCiudadView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CiudadSerializer(data=request.data)
        if Ciudad.objects.filter(**request.data).exists():
            raise serializers.ValidationError('Ya existe la ciudad')

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"Debe completar los campos solicitados"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCiudadView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        item = Ciudad.objects.get(pk=pk)
        serializer = CiudadSerializer(instance=item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"ID: {pk} no encontrado"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteCiudadView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        item = Ciudad.objects.get(pk=pk)
        if item is None:
            return Response({"message": f"ID: {pk} no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        item.estado = False
        item.save()
        return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
