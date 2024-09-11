from django.db import models
from django.contrib.auth.models import User
from .mObra import Obra

class TipoUnidad(models.Model):
    cod = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)
    medicion = models.CharField(max_length=3)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)    
    estado = models.IntegerField(default=1) #1 disponible / 0 no disponible (eliminada) 

    def natural_key(self):
        return (self.cod, self.descripcion)

    #def tiene_unidades_activas(self):
    #    return self.unidades.filter(estado=1).exists()
    
    def __str__(self):
        return self.descripcion        
    
    #class Meta:
        #unique_together = (('cod', 'descripcion'),)
        

    
    