from django.db import models
from django.contrib.auth.models import User
from .mInformeTrabajo import InformeTrabajo
from Tratos.Models import Trato
from Tratos.Models import UnidadObra
from decimal import Decimal

class InformeTrabajo_detalle(models.Model):
    itrabajo = models.ForeignKey(InformeTrabajo, on_delete=models.PROTECT)
    trato = models.ForeignKey(Trato, on_delete=models.PROTECT)
    unidad = models.ForeignKey(UnidadObra, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=0)
    avance = models.DecimalField(max_digits=8, decimal_places=2)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)    
    

    
    def calculaTotal(self):
        resultado = (Decimal(self.trato.valorTrato) /100) * self.avance
        resultado = int(resultado)
        res = '{:,}'.format(resultado)
        return res
    
    def valor_sep(self):
        res = '{:,}'.format(self.total)
        return res