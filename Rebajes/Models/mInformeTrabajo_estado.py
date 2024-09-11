from django.db import models
from django.contrib.auth.models import User


class InformeTrabajo_estado(models.Model):
    cod = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=20)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) 

        

    
    