from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.PanelLibroListView.as_view(), name='libro_list'),
    path('libros/nuevo/', views.PanelLibroCreateView.as_view(), name='libro_create'),
    path('libros/<int:pk>/editar/', views.PanelLibroUpdateView.as_view(), name='libro_update'),
    path('libros/<int:pk>/eliminar/', views.PanelLibroDeleteView.as_view(), name='libro_delete'),
    path('usuarios/', views.UserListView.as_view(), name='usuario_list'),
    path('usuarios/nuevo/', views.UserCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.UserUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', views.UserDeleteView.as_view(), name='usuario_delete'),
]
