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
# from django.contrib import admin
from django.urls import path, include
from gestion_bancaria import views

urlpatterns = [
    # frontend
    path('', views.index, name='home'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout'),
    path('cuentas/', views.cuentas_page, name='cuentas_page'),
    path('mis-cuentas/', views.mis_cuentas_page, name='mis_cuentas_page'),
    path('mis-movimientos/', views.mis_movimientos_page, name='mis_movimientos_page'),
    path('mis-movimientos/deposito/', views.deposito_page, name='deposito_page'),
    path('mis-movimientos/extraccion/', views.extraccion_page, name='extraccion_page'),
    path('mis-movimientos/transferencia/', views.transferencia_page, name='transferencia_page'),

    # apis
    path('admin/logout/', views.log_out),
    path('api/', include('gestion_bancaria.urls')),

    # admin django
    # path('admin/', admin.site.urls),
    # path("i18n/", include("django.conf.urls.i18n")),
]