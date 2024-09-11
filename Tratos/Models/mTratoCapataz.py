from django.db import models
from django.contrib.auth.models import User
from .mObra import Obra

class TratoCapataz(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)    
    idObra = models.ForeignKey(Obra, on_delete=models.PROTECT)

    def natural_key(self):
        return (self.id, self.nombre)

    def __str__(self):
        return self.nombre+ " "+self.apellido  # O usa self.descripcion si prefieres

    class Meta:
        unique_together = (('id', 'nombre'),)
        

    
    