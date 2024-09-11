from django.db import models
from django.contrib.auth.models import User
from .mObra import Obra
from .mTratoCategoria import TratoCategoria


class ObraCategoria(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT, related_name='obrac')
    categoria = models.ForeignKey(TratoCategoria, on_delete=models.PROTECT, related_name='categoria')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField(default=1) #1 activo / 0 inactivo  

    def __str__(self):
        return self.obra.descripcion+" "+self.categoria.descripcion    