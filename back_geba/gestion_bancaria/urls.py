from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
	# path('', views.ApiOverview, name='home'),

	# auth
	path('token/', views.ObtainTokenPairWithColorView.as_view(), name='token_create'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('blacklist/', views.LogoutView.as_view(), name='blacklist'),

	# persona
	path('persona/all/', views.ListPersonaView.as_view(), name='persona_view'),
	path('persona/create/', views.CreatePersonaView.as_view(), name="persona_create"),
	path('persona/update/<int:pk>/', views.UpdatePersonaView.as_view(), name='persona_update'),
	path('persona/item/<int:pk>/delete/', views.DeletePersonaView.as_view(), name='persona_delete'),

	# cliente
	path('cliente/all/', views.ListClienteView.as_view(), name='cliente_view'),

	# departamento
	path('departamento/all/', views.ListDepartamentoView.as_view(), name='departamento_view'),
	path('departamento/create/', views.CreateDepartamentoView.as_view(), name='departamento_create'),
	path('departamento/update/<int:pk>/', views.UpdateDepartamentoView.as_view(), name='departamento_update'),
	path('departamento/item/<int:pk>/delete/', views.DeleteDepartamentoView.as_view(), name='departamento_delete'),

	# ciudad
	path('ciudad/all/', views.ListCiudadView.as_view(), name='ciudad_view'),
	path('ciudad/create/', views.CreateCiudadView.as_view(), name='ciudad_create'),
	path('ciudad/update/<int:pk>/', views.UpdateCiudadView.as_view(), name='ciudad_update'),
	path('ciudad/item/<int:pk>/delete/', views.DeleteCiudadView.as_view(), name='ciudad_delete'),

	# cuenta
	path('cuenta/all/', views.ListCuentaView.as_view(), name='cuenta_view'),
	path('cuenta/create/', views.CreateCuentaView.as_view(), name='cuenta_create'),
	path('cuenta/update/<int:pk>/', views.UpdateCuentaView.as_view(), name='cuenta_update'),
	path('cuenta/item/<int:pk>/changeStatus/', views.ChangeStatusCuentaView.as_view(), name='cuenta_status'),

	# movimiento
	path('movimiento/all/', views.ListMovimientoView.as_view(), name='movimiento_view'),
	path('movimiento/deposit/', views.DepositMovimientoView.as_view(), name='movimiento_deposit'),
	path('movimiento/extraction/', views.ExtractionMovimientoView.as_view(), name='movimiento_extraction'),
	path('movimiento/transfer/', views.TransferMovimientoView.as_view(), name='movimiento_transfer'),

]
