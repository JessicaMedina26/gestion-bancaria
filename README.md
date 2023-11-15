# gestion-bancaria

#### actualizar version python (opcional)
    python3.11 -m pip install --upgrade pip 

#### virtualenv
    sudo pip3 install virtualenv
    mkdir venv && cd venv
    virtualenv env
    source env/bin/activate

#### install django
    pip3 install django

#### install lib
    pip3 install djangorestframework
    pip3 install psycopg2
    pip3 install psycopg2-binary

#### create project django
    django-admin startproject back_geba

#### configurar proyecto - djangorest - abrir archivo de configuracion principal
    Ubicación: back_geba/back_geba/settings.py

    -- Agregar lib rest framework
    INSTALLED_APPS = [
       ...
        'rest_framework',
    ]

#### Configurar la conexion
    DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'myproject',
            'USER': 'myuser',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

#### creando una app django
    python manage.py startapp gestion_bancaria

#### agregamos la nueva app en INSTALLED_APPS
    INSTALLED_APPS = [
       ...
        'gestion_bancaria',
    ]


#### crearemos columnas de base de datos con los campos de nuestros modelos mediante el proceso de migración. 
- Usaremos el manage.py archivo para aplicar las migraciones. 
    python manage.py makemigrations
    python manage.py migrate


#### Creando una API REST con Django Rest Framework
- Construiremos nuestra API en Django Rest Framework. Nos ocuparemos de vistas, serializadores y puntos finales de URL. Los puntos finales están adjuntos a las vistas que obtienen las respuestas a las solicitudes web. 
- Los serializadores ayudan a traducir entre objetos JSON, XML y Python nativos. 
- Crea un nuevo archivo en el directorio: gestion_bancaria con nombre serializers.py. Ingrese el siguiente código en él. 

    from rest_framework import serializers
    from .models import Customer

    class CustomerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Customer 
            fields = ['pk', 'name', 'email', 'created']


#### Agregar el siguiente código dentro del views.py de la app gestion_bancaria. 
- CustomerCreateView para crear un nuevo objeto de cliente
- CustomerUpdate para actualizar un nuevo objeto de cliente
- CustomerDelete para eliminar un nuevo objeto de cliente
- CustomerList para listar los clientes

    from django.shortcuts import render
    from .models import Customer
    from rest_framework import generics
    from .serializers import CustomerSerializer


    class CustomerCreate(generics.CreateAPIView):
        # API endpoint that allows creation of a new customer
        queryset = Customer.objects.all(),
        serializer_class = CustomerSerializer

    class CustomerUpdate(generics.RetrieveUpdateAPIView):
        # API endpoint that allows a customer record to be updated.
        queryset = Customer.objects.all()
        serializer_class = CustomerSerializer

    class CustomerDelete(generics.RetrieveDestroyAPIView):
        # API endpoint that allows a customer record to be deleted.
        queryset = Customer.objects.all()
        serializer_class = CustomerSerializer

    class CustomerList(generics.ListAPIView):
        # API endpoint that allows customer to be viewed.
        queryset = Customer.objects.all()
        serializer_class = CustomerSerializer

    class CustomerDetail(generics.RetrieveAPIView):
        # API endpoint that returns a single customer by pk.
        queryset = Customer.objects.all()
        serializer_class = CustomerSerializer

#### Configurar URL de la app gestion_bancaria

    from django.urls import include, path
    from .views import CustomerCreate, CustomerList, CustomerDetail, CustomerUpdate, CustomerDelete

    urlpatterns = [
        path('create/', CustomerCreate.as_view(), name='create-customer'),
        path('', CustomerList.as_view()),
        path('<int:pk>/', CustomerDetail.as_view(), name='retrieve-customer'),
        path('update/<int:pk>/', CustomerUpdate.as_view(), name='update-customer'),
        # path('delete/<int:pk>/', CustomerDelete.as_view(), name='delete-customer')
    ]

#### Configurar URL principal - back_geba
    from django.urls import path, include #new

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('customer/', include('customer.urls')), #new
    ]

#### si ya cuentas con el proyecto descargado, para instalar las librerias del archivo requirements.txt 
    pip3 install -r requirements.txt
