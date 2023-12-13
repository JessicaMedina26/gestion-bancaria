# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout


# frontend
def index(request):
    return render(request, 'index.html')


def login_page(request):
    return render(request, 'login.html')


def mis_cuentas_page(request):
    return render(request, 'mis-cuentas.html')


def mis_movimientos_page(request):
    return render(request, 'mis-movimientos.html')


def deposito_page(request):
    return render(request, 'deposito.html')


def extraccion_page(request):
    return render(request, 'extraccion.html')


def transferencia_page(request):
    return render(request, 'transferencia.html')


def logout_page(request):
    logout(request)  # Cierra la sesión del usuario actual
    return redirect('inicio')  # Redirige al usuario a la página de inicio u otra página de tu elección


# methods globals
@api_view(['GET'])
@permission_classes([AllowAny])
def log_out(request):
    logout(request)
    return redirect_login()


@api_view(['GET'])
@permission_classes([AllowAny])
def home(_):
    return redirect_login()


def redirect_login():
    return HttpResponseRedirect('/admin/')
