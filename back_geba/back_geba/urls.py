"""
URL configuration for back_geba project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gestion_bancaria import views

urlpatterns = [
    # path('', views.home),
    path('', views.index, name='home'),
    path('login/', views.index, name='iniciar_sesion'),
    path('logout/', views.index, name='cerrar_sesion'),
    path('registro/', views.index, name='registro'),

    path('cuentas/', views.index, name='cuentas_desc'),
    path('about/', views.index, name='about_desc'),
    path('contacto/', views.index, name='contact_desc'),
    path('politicas/', views.index, name='politicas_desc'),
    path('terminos/', views.index, name='terminos_desc'),

    # apis
    path('admin/logout/', views.log_out),
    path('admin/', admin.site.urls),
    path('api/', include('gestion_bancaria.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
]