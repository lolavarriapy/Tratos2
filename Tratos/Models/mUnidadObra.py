from django.db import models
from django.contrib.auth.models import User
from .mObra import Obra
from .mUnidadTipo import TipoUnidad
from .mUnidadModelo import UnidadModelo

class UnidadObra(models.Model):
    cod = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)
    #idTipo = models.ForeignKey(TipoUnidad, on_delete=models.PROTECT, related_name='unidades')
    idModelo = models.ForeignKey(UnidadModelo, on_delete=models.PROTECT, related_name='modelos')
    idObra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)
    estado = models.IntegerField(default=1) #1 disponible / 2 bloqueada / 0 eliminada || bloqueo rebaje de unidades 

    def __str__(self):
        return self.descripcion        