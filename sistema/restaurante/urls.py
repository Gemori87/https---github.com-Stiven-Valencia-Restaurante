from django.urls import path
from . import views
from .views import listar_pedidos, crear_pedido  # Importar las vistas de pedidos
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import recuperar_contrasena, logout_view
from django.contrib.auth import views as auth_views
from .views import login_view  

from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', login_view, name='login'),  
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path("recuperar-contrasena/", recuperar_contrasena, name="recuperar_contrasena"),
    path('perfil/', views.perfil, name='perfil'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('logout/', logout_view, name='logout'),

    
    path('platillos/', views.listar_platillos, name='platillos'),
    path('platillos/agregar/', views.agregar_platillo, name='agregar_platillo'),  
    path('platillos/editar/<int:id>/', views.editar_platillo, name='editar_platillo'),  
    path('platillos/eliminar/<int:id>/', views.eliminar_platillo, name='eliminar_platillo'),
    path('platillos/ocultar/<int:id>/', views.ocultar_platillo, name='ocultar_platillo'),
    path('platillos/mostrar/<int:id>/', views.mostrar_platillo, name='mostrar_platillo'),  
    path('crear-pedido/', views.crear_pedido, name='crear_pedido'),
    
    path('pedidos/', listar_pedidos, name='listar_pedidos'),  # Ruta para listar pedidos
    path('pedidos/crear/', crear_pedido, name='crear_pedido'),  # Ruta para crear un nuevo pedido
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
