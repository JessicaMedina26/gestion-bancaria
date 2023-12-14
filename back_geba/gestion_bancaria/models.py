from django.contrib.auth.models import AbstractUser
from django.db import models


class Departamento(models.Model):
    objects = models.Manager()
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre", max_length=50)
    estado = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id_departamento']

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    objects = models.Manager()
    id_ciudad = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre", max_length=50)
    codigo_postal = models.IntegerField("Código Postal")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Persona(AbstractUser):
    tipo_documento = models.CharField(max_length=10)
    nro_documento = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)


class Cliente(models.Model):
    objects = models.Manager()
    id_cliente = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='cliente')
    fecha_ingreso = models.DateTimeField("Fecha Ingreso", auto_now_add=True)
    calificacion = models.IntegerField("Calificación")


class Cuenta(models.Model):
    objects = models.Manager()
    id_cuenta = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cliente')
    nro_cuenta = models.PositiveIntegerField(unique=True)
    nro_contrato = models.CharField(max_length=255, unique=True)
    fecha_alta = models.DateTimeField("Fecha Alta", auto_now_add=True)
    tipo_cuenta = models.CharField(choices=(
        ('CUENTA CORRIENTE', 'CUENTA CORRIENTE'),
        ('CAJA DE AHORRO', 'CAJA DE AHORRO'),
    ))
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    costo_mantenimiento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promedio_acreditacion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    moneda = models.CharField(choices=(('GS', 'GS'), ('USD', 'USD')), default='GS')
    estado = models.CharField(choices=(
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO'),
        ('BLOQUEADO', 'BLOQUEADO'),
    ), default='ACTIVO')


class Movimiento(models.Model):
    objects = models.Manager()
    id_movimiento = models.AutoField(primary_key=True)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='cuenta')
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(choices=(('CREDITO', 'CREDITO'), ('DEBITO', 'DEBITO')))
    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2)
    monto_movimiento = models.DecimalField(max_digits=10, decimal_places=2)
    cuenta_origen = models.DecimalField(max_digits=10, decimal_places=2)
    cuenta_destino = models.DecimalField(max_digits=10, decimal_places=2)
    canal = models.CharField(choices=(('APP', 'APP'), ('WEB', 'WEB')), default='WEB')
