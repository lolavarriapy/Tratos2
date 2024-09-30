
from django.urls import path
from . import views

urlpatterns = [
    path('informeTrabajo/finalizar/', views.informeTrabajo_finalizar, name='informeTrabajo_finalizar'),
    path('informeTrabajo/cabecera/guardar', views.informeTrabajo_cabecera_guardar, name='informeTrabajo_cabecera_guardar'),
    path('informeTrabajo/detalle/guardar', views.informeTrabajo_detalle_guardar, name='informeTrabajo_detalle_guardar'),
    path('informeTrabajo/detalle/eliminar', views.informeTrabajo_detalle_eliminar, name='informeTrabajo_detalle_eliminar'),
    path('informeTrabajo/cuadrilla/guardar', views.informeTrabajo_cuadrilla_guardar, name='informeTrabajo_cuadrilla_guardar'),
    path('informeTrabajo/cuadrilla/eliminar', views.informeTrabajo_cuadrilla_eliminar, name='informeTrabajo_cuadrilla_eliminar'),
    path('informeTrabajo/crear', views.informeTrabajo_crear, name='informeTrabajo_crear'),
    path('informeTrabajo/buscar', views.informeTrabajo_buscar, name='informeTrabajo_buscar'),
    path('informeTrabajo/ver/<uuid:vid>/', views.informeTrabajo_ver, name='informeTrabajo_ver'),
    path('tratos/', views.tratos, name='tratos'),
    path('unidadTrato/obtener', views.unidadTrato_obtener, name='unidadTrato_obtener'),
]


