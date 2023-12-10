from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
	path('', views.ApiOverview, name='home'),

	path('token/', views.ObtainTokenPairWithColorView.as_view(), name='token-create'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
	path('blacklist/', views.LogoutView.as_view(), name='blacklist'),

	# persona
	path('persona/all/', views.ListPersonaView.as_view(), name='persona-view'),
	path('persona/create/', views.CreatePersonaView.as_view(), name="persona-create"),
	path('persona/update/<int:pk>/', views.UpdatePersonaView.as_view(), name='persona-update'),
	path('persona/item/<int:pk>/delete/', views.DeletePersonaView.as_view(), name='persona-delete'),

	# cliente
	path('cliente/all/', views.ListClienteView.as_view(), name='cliente-view'),

	# departmento
	path('departamento/all/', views.ListDepartamentoView.as_view(), name='departamento-view'),
	path('departamento/create/', views.CreateDepartamentoView.as_view(), name='departamento-create'),
	path('departamento/update/<int:pk>/', views.UpdateDepartamentoView.as_view(), name='departamento-update'),
	path('departamento/item/<int:pk>/delete/', views.DeleteDepartamentoView.as_view(), name='departamento-delete'),

	# ciudad
	path('ciudad/all/', views.ListCiudadView.as_view(), name='ciudad-view'),
	path('ciudad/create/', views.CreateCiudadView.as_view(), name='ciudad-create'),
	path('ciudad/update/<int:pk>/', views.UpdateCiudadView.as_view(), name='ciudad-update'),
	path('ciudad/item/<int:pk>/delete/', views.DeleteCiudadView.as_view(), name='ciudad-delete'),
]