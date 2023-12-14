# Create your views here.
from decimal import InvalidOperation, Decimal
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from gestion_bancaria.serializers import MovimientoSerializer
from gestion_bancaria.models import Movimiento, Cuenta


class ListMovimientoView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        if request.query_params:
            items = Movimiento.objects.filter(**request.query_params.dict())
        else:
            return Response({"message": "Cuenta no identificada"}, status=status.HTTP_400_BAD_REQUEST)

        if items:
            serializer = MovimientoSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No se encontraron datos disponibles"}, status=status.HTTP_400_BAD_REQUEST)


class DepositMovimientoView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        # se valida canal
        canal = request.data.get('canal')
        if canal is None:
            return Response({'message': 'El campo canal es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida moneda
        moneda = request.data.get('moneda')
        if canal is None:
            return Response({'message': 'El campo moneda es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida monto
        try:
            monto_movimiento = Decimal(request.data.get('monto'))
            print(monto_movimiento)
            if monto_movimiento <= 0:
                return Response({'message': 'Monto debe ser mayor a cero'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidOperation:
            return Response({'message': 'Monto no válido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida nro. de cuenta destino
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        if nro_cuenta_destino is None:
            return Response({'message': 'Nro. de cuenta destino es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida cuenta destino
        try:
            cuenta_destino = Cuenta.objects.get(nro_cuenta=nro_cuenta_destino)
        except Cuenta.DoesNotExist:
            return Response({'message': 'La cuenta destino no existe'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida si la cuenta se encuentra bloqueada
        if cuenta_destino.estado == 'BLOQUEADO':
            return Response({'message': 'La cuenta destino está bloqueada'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida que la cuenta sea de la misma moneda
        if cuenta_destino.moneda != moneda:
            return Response({'message': 'La transacciones deben pertenecer a la misma moneda de la cuenta'},
                            status=status.HTTP_400_BAD_REQUEST)

        # actualizacion de cuenta
        nro_cuenta_origen = 0
        tipo_movimiento = "CREDITO"
        saldo_anterior = cuenta_destino.saldo
        saldo_actual = saldo_anterior + monto_movimiento

        cuenta_destino.saldo = saldo_actual
        cuenta_destino.save()

        Movimiento.objects.create(cuenta=cuenta_destino,
                                  tipo_movimiento=tipo_movimiento,
                                  saldo_anterior=saldo_anterior,
                                  saldo_actual=saldo_actual,
                                  monto_movimiento=monto_movimiento,
                                  cuenta_origen=nro_cuenta_origen,
                                  cuenta_destino=nro_cuenta_destino,
                                  canal=canal)

        return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)


class ExtractionMovimientoView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        # se valida canal
        canal = request.data.get('canal')
        if canal is None:
            return Response({'message': 'El campo canal es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida moneda
        moneda = request.data.get('moneda')
        if canal is None:
            return Response({'message': 'El campo moneda es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida monto
        try:
            monto_movimiento = Decimal(request.data.get('monto'))
            if monto_movimiento <= 0:
                return Response({'message': 'Monto debe ser mayor a cero'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidOperation:
            return Response({'message': 'Monto no válido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida nro. de cuenta origen
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        if nro_cuenta_origen is None:
            return Response({'message': 'Nro. de cuenta origen es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida cuenta origen
        try:
            cuenta_origen = Cuenta.objects.get(nro_cuenta=nro_cuenta_origen)
        except Cuenta.DoesNotExist:
            return Response({'message': 'La cuenta origen no existe'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida si la cuenta se encuentra bloqueada
        if cuenta_origen.estado == 'BLOQUEADO':
            return Response({'message': 'La cuenta origen está bloqueada'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida que el monto del movimiento no supere el saldo
        if cuenta_origen.saldo < monto_movimiento:
            return Response({'message': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida que la cuenta sea de la misma moneda
        if cuenta_origen.moneda != moneda:
            return Response({'message': 'La transacciones deben pertenecer a la misma moneda de la cuenta'},
                            status=status.HTTP_400_BAD_REQUEST)

        # actualizacion de cuenta
        nro_cuenta_destino = 0
        tipo_movimiento = "DEBITO"
        saldo_anterior = cuenta_origen.saldo
        saldo_actual = saldo_anterior - monto_movimiento

        cuenta_origen.saldo = saldo_actual
        cuenta_origen.save()

        Movimiento.objects.create(cuenta=cuenta_origen,
                                  tipo_movimiento=tipo_movimiento,
                                  saldo_anterior=saldo_anterior,
                                  saldo_actual=saldo_actual,
                                  monto_movimiento=monto_movimiento,
                                  cuenta_origen=nro_cuenta_origen,
                                  cuenta_destino=nro_cuenta_destino,
                                  canal=canal)

        return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)


class TransferMovimientoView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        # se valida canal
        canal = request.data.get('canal')
        if canal is None:
            return Response({'message': 'El campo canal es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida moneda
        moneda = request.data.get('moneda')
        if canal is None:
            return Response({'message': 'El campo moneda es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida monto
        try:
            monto_movimiento = Decimal(request.data.get('monto'))
            if monto_movimiento <= 0:
                return Response({'message': 'Monto debe ser mayor a cero'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidOperation:
            return Response({'message': 'Monto no válido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida nro. de cuenta origen
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        if nro_cuenta_origen is None:
            return Response({'message': 'Nro. de cuenta origen es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida nro. de cuenta destino
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        if nro_cuenta_destino is None:
            return Response({'message': 'Nro. de cuenta destino es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida cuenta origen
        try:
            cuenta_origen = Cuenta.objects.get(nro_cuenta=nro_cuenta_origen)
        except Cuenta.DoesNotExist:
            return Response({'message': 'La cuenta origen no existe'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida cuenta destino
        try:
            cuenta_destino = Cuenta.objects.get(nro_cuenta=nro_cuenta_destino)
        except Cuenta.DoesNotExist:
            return Response({'message': 'La cuenta destino no existe'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida en caso que la cuenta origen sea igual a la cuenta destino
        if cuenta_origen == cuenta_destino:
            return Response({'message': 'La cuenta destino debe ser diferente a la cuenta origen'},
                            status=status.HTTP_400_BAD_REQUEST)

        # se valida si se encuentra bloqueada la cuenta
        if cuenta_origen.estado == 'BLOQUEADO':
            return Response({'message': 'La cuenta origen está bloqueada'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida si se encuentra bloqueada la cuenta
        if cuenta_destino.estado == 'BLOQUEADO':
            return Response({'message': 'La cuenta destino está bloqueada'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida que el monto del movimiento no supere el saldo
        if cuenta_origen.saldo < monto_movimiento:
            return Response({'message': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        # se valida que la cuenta sea del mismo tipo
        if cuenta_origen.tipo_cuenta != cuenta_destino.tipo_cuenta:
            return Response({'message': 'Las cuentas deben ser del mismo tipo para efectuar la transferencia'},
                            status=status.HTTP_400_BAD_REQUEST)

        # se valida que la cuenta sea de la misma moneda
        if cuenta_origen.moneda != moneda:
            return Response({'message': 'La transacciones deben pertenecer a la misma moneda de la cuenta'},
                            status=status.HTTP_400_BAD_REQUEST)

        # se procesa cuenta origen
        tipo_movimiento_origen = "DEBITO"
        saldo_anterior_origen = cuenta_origen.saldo
        saldo_actual_origen = saldo_anterior_origen - monto_movimiento
        cuenta_origen.saldo = saldo_actual_origen
        cuenta_origen.save()

        # se procesa movimiento origen
        Movimiento.objects.create(cuenta=cuenta_origen,
                                  tipo_movimiento=tipo_movimiento_origen,
                                  saldo_anterior=saldo_anterior_origen,
                                  saldo_actual=saldo_actual_origen,
                                  monto_movimiento=monto_movimiento,
                                  cuenta_origen=nro_cuenta_origen,
                                  cuenta_destino=nro_cuenta_destino,
                                  canal=canal)

        # se procesa cuenta destino
        tipo_movimiento_destino = "CREDITO"
        saldo_anterior_destino = cuenta_destino.saldo
        saldo_actual_destino = saldo_anterior_destino + monto_movimiento
        cuenta_destino.saldo = saldo_actual_destino
        cuenta_destino.save()

        # se procesa movimiento destino
        Movimiento.objects.create(cuenta=cuenta_destino,
                                  tipo_movimiento=tipo_movimiento_destino,
                                  saldo_anterior=saldo_anterior_destino,
                                  saldo_actual=saldo_actual_destino,
                                  monto_movimiento=monto_movimiento,
                                  cuenta_origen=nro_cuenta_origen,
                                  cuenta_destino=nro_cuenta_destino,
                                  canal=canal)

        return Response({"message": "Procesado con éxito"}, status=status.HTTP_200_OK)
