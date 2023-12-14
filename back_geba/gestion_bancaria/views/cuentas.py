# Create your views here.
import random
import string
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from gestion_bancaria.serializers import CuentaSerializer
from gestion_bancaria.models import Cuenta


class ListCuentaView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        if request.query_params:
            items = Cuenta.objects.filter(**request.query_params.dict())
        else:
            items = Cuenta.objects.all()

        if items:
            serializer = CuentaSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No se encontraron datos disponibles"}, status=status.HTTP_400_BAD_REQUEST)


class CreateCuentaView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data['nro_contrato'] = generar_nro_contrato()
        request.data['nro_cuenta'] = generar_nro_cuenta()

        if Cuenta.objects.filter(nro_contrato=request.data['nro_contrato']).exists():
            return Response({"message": "Ya existe el Nro. de contrato"}, status=status.HTTP_400_BAD_REQUEST)

        if Cuenta.objects.filter(nro_cuenta=request.data['nro_cuenta']).exists():
            return Response({"message": "Ya existe el Nro. de cuenta"}, status=status.HTTP_400_BAD_REQUEST)

        if Cuenta.objects.filter(**request.data).exists():
            return Response({"message": "Ya existe la Cuenta"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CuentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Debe completar los campos solicitados"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCuentaView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            item = Cuenta.objects.get(pk=pk)
        except Cuenta.DoesNotExist:
            return Response({"message": "No se pudo identificar la Cuenta"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CuentaSerializer(instance=item, data=request.data)
        if Cuenta.objects.filter(nro_contrato=request.data['nro_contrato']).exclude(pk=pk).exists():
            return Response({"message": "Ya existe el Nro. de contrato"}, status=status.HTTP_400_BAD_REQUEST)

        if Cuenta.objects.filter(nro_cuenta=request.data['nro_cuenta']).exclude(pk=pk).exists():
            return Response({"message": "Ya existe el Nro. de cuenta"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"ID: {pk} no encontrado"}, status=status.HTTP_400_BAD_REQUEST)


class ChangeStatusCuentaView(generics.UpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def put(self, request, pk):
        try:
            item = Cuenta.objects.get(pk=pk)
        except Cuenta.DoesNotExist:
            return Response({"message": "No se pudo identificar la Cuenta"}, status=status.HTTP_400_BAD_REQUEST)

        item.estado = request.data['estado']
        item.save()
        return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)


def generar_nro_cuenta():
    while True:
        number = random.randint(10 ** (8 - 1), 10 ** 8 - 1)
        if not Cuenta.objects.filter(nro_cuenta=number).exists():
            return number


def generar_nro_contrato():
    while True:
        number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        if not Cuenta.objects.filter(nro_contrato=number).exists():
            return number

