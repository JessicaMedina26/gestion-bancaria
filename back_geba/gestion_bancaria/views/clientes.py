# Create your views here.
from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from gestion_bancaria.models import Cliente
from gestion_bancaria.serializers import ClienteListSerializer


class ListClienteView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.query_params:
            items = Cliente.objects.filter(**request.query_params.dict())
        else:
            # items = Cliente.objects.raw('SELECT p.*,c.* '
            #                             'FROM gestion_bancaria_Cliente p, gestion_bancaria_cliente c '
            #                             'WHERE p.id=c.Cliente_id and p.is_active is true')
            items = Cliente.objects.all()
        if items:
            serializer = ClienteListSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"message": "No se encontraron datos disponibles"}, status=status.HTTP_400_BAD_REQUEST)

