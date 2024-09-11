from django.db import models
from django.contrib.auth.models import User
from .mObra import Obra
from .mUnidadTipo import TipoUnidad

class UnidadModelo(models.Model):
    cod = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idObra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)    
    tipo = models.ForeignKey(TipoUnidad, on_delete=models.PROTECT,default=1) #(User, on_delete=models.CASCADE)
    estado = models.IntegerField(default=1) #1 disponible / 0 no disponible (eliminada) 
          
            
    def natural_key(self):
        return (self.cod, self.descripcion)

    def __str__(self):
        return self.descripcion    
    
    #class Meta:
        #unique_together = (('cod', 'descripcion'),)
        

    
    