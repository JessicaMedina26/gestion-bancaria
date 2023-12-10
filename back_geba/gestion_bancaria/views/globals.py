# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'index.html')


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


@api_view(['GET'])
@permission_classes([AllowAny])
def ApiOverview(_):
    api_urls = {
        'customer': {
            'all_items': '/customer/all/',
            'Search by Name': '/customer/?name=name',
            'Add': '/customer/create',
            'Update': '/customer/update/pk',
            'Delete': '/customer/item/pk/delete'
        }
    }
    return Response(api_urls)
