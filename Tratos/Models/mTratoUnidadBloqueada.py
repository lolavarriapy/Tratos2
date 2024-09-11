from django.db import models
from django.contrib.auth.models import User
from .mTrato import Trato
from .mUnidadObra import UnidadObra

class TratoUnidadBloqueada(models.Model):
    trato = models.ForeignKey(Trato, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)
    unidad = models.ForeignKey(UnidadObra, on_delete=models.PROTECT)
    motivo = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.IntegerField(default=1) #1 activo / 0 inactivo  
    
    def __str__(self):
        return self.trato.cod+" "+self.unidad.descripcion        