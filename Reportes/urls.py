
from django.urls import path
from . import views

urlpatterns = [
    path('capataz/', views.reporteCapataz, name='reporteCapataz'),
    path('capataz/imprimir', views.capatazImprimir, name='capatazImprimir'),
    path('capataz/obra/list', views.capatazObra, name='capatazObra'),
    path('rebajes/', views.reporteRebajes, name='reporteRebajes'),
]


