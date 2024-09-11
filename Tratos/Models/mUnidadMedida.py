from django.db import models
from django.contrib.auth.models import User

class UnidadMedida(models.Model):
    cod = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)    
        
    def natural_key(self):
        return (self.cod, self.descripcion)
    
    def __str__(self):
        return self.descripcion    

    class Meta:
        unique_together = (('cod', 'descripcion'),)
        

    
    