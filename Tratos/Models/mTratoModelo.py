from django.db import models
from django.contrib.auth.models import User
from .mTrato import Trato
from .mUnidadModelo import UnidadModelo


class TratoModelo(models.Model):
    trato = models.ForeignKey(Trato, on_delete=models.PROTECT)
    modelo = models.ForeignKey(UnidadModelo, on_delete=models.PROTECT)
    cantidad = models.BigIntegerField(default=0)
    rendimiento = models.DecimalField(max_digits=8, decimal_places=2)
    valorTratoModelo = models.BigIntegerField(default=0)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)
    estado = models.BooleanField()
    
    
    def valorTratoModelo_sep(self):
        if self.valorTratoModelo != "" and self.valorTratoModelo != "null":
            res = '{:,}'.format(self.valorTratoModelo)
        else:
            res = '0'
        return res
    
    def __str__(self):
        return self.trato.cod+" "+self.modelo.descripcion