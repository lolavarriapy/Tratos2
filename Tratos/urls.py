
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('', views.signin, name='signin'),
    path('signin/', views.signin, name='signin'),
    path('check-session/', views.check_session, name='check_session'),
    path('obras/', views.obras, name='obras'),
    #path('obras/crear/', views.obras, name='obras_crear'),
    path('obras/categorias/obtener', views.obras_categorias_obtener, name='obras_categorias_obtener'),
    path('obras/categorias/actualizar', views.obras_categorias_actualizar, name='obras_categorias_actualizar'),
    path('obras/<uuid:id>/', views.obras_configuracion, name='obras_configuracion'),
    path('unidadObra/crear/', views.unidadObra_crear, name='unidadObra_crear'),
    path('unidadObra/actualizar/', views.unidadObra_actualizar, name='unidadObra_actualizar'),
    path('unidadObra/obtener/', views.unidadObra_obtener, name='unidadObra_obtener'),
    path('unidadObra/eliminar/', views.unidadObra_eliminar, name='unidadObra_eliminar'),
    path('tiposUnidad/', views.tiposUnidad, name='tiposUnidad'),
    path('ModelosUnidad/', views.modelosUnidad, name='modelosUnidad'),
    path('ModelosUnidad/eliminar/', views.modelosUnidad, name='modelosUnidad_eliminar'),    
    path('tratos/crear/', views.tratos_crear, name='tratos_crear'),
    path('tratos/actualizar/', views.tratos_actualizar, name='tratos_actualizar'),
    path('tratos/estado/actualizar/', views.trato_estado_actualizar, name='trato_estado_actualizar'),
    path('tratos/buscar/', views.tratos_buscar, name='tratos_buscar'),
    path('tratos/modelos/obtener', views.trato_modelos_obtener, name='trato_modelos_obtener'),
    path('tratos/cuadrilla/actualizar', views.tratos_cuadrilla_actualizar, name='tratos_cuadrilla_actualizar'),
    path('tratos/modelos/actualizar', views.tratos_modelos_actualizar, name='tratos_modelos_actualizar'),
    path('tratos/partida/obtener', views.trato_partida_obtener, name='trato_partida_obtener'),
    path('tratos/unidad/bloquear', views.unidadTrato_bloqueo, name='unidadTrato_bloqueo'),
    path('tratos/item/crear', views.item_crear, name='item_crear'),
]


