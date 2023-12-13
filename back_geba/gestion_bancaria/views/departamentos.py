# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from gestion_bancaria.serializers import DepartamentoSerializer
from gestion_bancaria.models import Departamento


class ListDepartamentoView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.query_params:
            items = Departamento.objects.filter(**request.query_params.dict())
        else:
            items = Departamento.objects.filter(estado=True)

        if items:
            serializer = DepartamentoSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No se encontraron datos disponibles"},
                            status=status.HTTP_400_BAD_REQUEST)


class CreateDepartamentoView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = DepartamentoSerializer(data=request.data)
        if Departamento.objects.filter(**request.data).exists():
            return Response({"message": "Ya existe el Departamento"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"Debe completar los campos solicitados"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateDepartamentoView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            item = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response({"message": "No se pudo identificar el Departamento"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DepartamentoSerializer(instance=item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"ID: {pk} no encontrado"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteDepartamentoView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            item = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response({"message": "No se pudo identificar el Departamento"}, status=status.HTTP_400_BAD_REQUEST)

        item.estado = False
        item.save()
        return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
