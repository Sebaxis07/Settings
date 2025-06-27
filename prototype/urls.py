from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libro/<int:id>/', views.libro_detalle, name='libro_detalle'),
    path('nota/eliminar/<int:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('anadir-libro/', views.LibroUsuarioCreateView.as_view(), name='libro_anadir'),
    path('libro/<int:pk>/eliminar/', views.LibroDeleteView.as_view(), name='libro_eliminar_usuario'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]