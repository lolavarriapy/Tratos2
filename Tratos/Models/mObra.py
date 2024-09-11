from django.db import models
from django.contrib.auth.models import User
import uuid

class Obra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cod = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    direccionCalle = models.CharField(max_length=100)
    direccionNumero = models.IntegerField(default=0)
    tipoObra = models.CharField(max_length=2) #1 CA / 2 ED
    #paramgMaps = models.TextField()
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT)
    
    
    def __str__(self):
        return self.descripcion
    