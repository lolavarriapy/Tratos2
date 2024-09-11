from django.db import models
from django.contrib.auth.models import User
from .mInformeTrabajo import InformeTrabajo


class InformeTrabajo_cuadrilla(models.Model):
    itrabajo = models.ForeignKey(InformeTrabajo, on_delete=models.PROTECT)
    codTalana = models.IntegerField(default=0)
    nomTrab = models.TextField()
    lunTrab = models.BooleanField(default=0)
    marTrab = models.BooleanField(default=0)
    mieTrab = models.BooleanField(default=0)
    jueTrab = models.BooleanField(default=0)
    vieTrab = models.BooleanField(default=0)
    totalDias = models.IntegerField(default=0)
    valorDia = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)    


    def __str__(self):
        return self.itrabajo.folio+" "+self.codTalana+" "+self.nomTrab  
    