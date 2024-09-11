from django.db import models
from django.contrib.auth.models import User
from Tratos.Models import Obra
from .mInformeTrabajo_estado import InformeTrabajo_estado
import uuid
from django.db.models import Max

class InformeTrabajo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folio = models.CharField(max_length=10)
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaTermino = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    fechaFinalizado = models.DateTimeField(blank=True,null=True)
    idEstado = models.ForeignKey(InformeTrabajo_estado, on_delete=models.PROTECT)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)    
    orden = models.IntegerField(unique=True, blank=True, null=True)

    
    class Meta:
        permissions = [
            ("can_view_informeTrabajo", "ver InformeTrabajo"),
            ("can_edit_informeTrabajo", "editar InformeTrabajo"),
        ]
        
    
    def save(self, *args, **kwargs):
        if self.orden is None:  # Solo establecer el orden si no está definido
            max_order = InformeTrabajo.objects.aggregate(Max('orden'))['orden__max'] or 0
            self.orden = max_order + 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.partida
    
    
    

