from django.db import models
from django.contrib.auth.models import User
from .mObra import Obra


class ObraUsuario(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT, related_name='obra')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='usuario')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField(default=1) #1 activo / 0 inactivo  

    def __str__(self):
        return self.usuario.username+" "+self.obra.descripcion
