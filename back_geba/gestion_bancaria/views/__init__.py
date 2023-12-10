from gestion_bancaria.views.globals import *
from gestion_bancaria.views.auth import *
from gestion_bancaria.views.personas import *
from gestion_bancaria.views.departamentos import *
from gestion_bancaria.views.ciudades import *

# alternative in __init__.py:
from .globals import *
from .auth import ObtainTokenPairWithColorView, LogoutView
from .personas import ListPersonaView, CreatePersonaView, UpdatePersonaView, DeletePersonaView
from .clientes import ListClienteView
from .departamentos import ListDepartamentoView, CreateDepartamentoView, UpdateDepartamentoView, DeleteDepartamentoView
from .ciudades import ListCiudadView, CreateCiudadView, UpdateCiudadView, DeleteCiudadView

