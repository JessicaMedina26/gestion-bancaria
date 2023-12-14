# Geba Bank

#### actualizar version python (opcional)
    python3.10 -m pip install --upgrade pip 

#### virtualenv
    sudo pip3 install virtualenv
    mkdir venv && cd venv
    virtualenv env
    source env/bin/activate

#### install django
      pip3 install django    
      pip3 install djangorestframework
      pip3 install djangorestframework-simplejwt
      pip3 install psycopg2
      pip3 install psycopg2-binary
      pip3 install django-cors-headers
      pip3 install django-jazzmin

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

Usaremos el manage.py archivo para aplicar las migraciones.

    python manage.py makemigrations
    python manage.py migrate

#### si ya cuentas con el proyecto descargado, para instalar las librerias del archivo requirements.txt 
    pip3 install -r requirements.txt
