from django.db import models
from django.contrib.auth.models import User
from .mObra import Obra
from .mUnidadModelo import UnidadModelo
from .mTratoCategoria import TratoCategoria
from .mTratoEspecialidad import TratoEspecialidad
from .mTratoCapataz import TratoCapataz
from .mUnidadMedida import UnidadMedida
import uuid
from django.db.models import Max

# Create your models here.
class Trato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cod = models.CharField(max_length=10)
    codFamilia = models.CharField(max_length=15)
    categoria = models.ForeignKey(TratoCategoria, on_delete=models.PROTECT)
    especialidad = models.ForeignKey(TratoEspecialidad, on_delete=models.PROTECT)
    capataz = models.ForeignKey(TratoCapataz, on_delete=models.PROTECT)
    partida = models.TextField(blank=True)
    Modelos = models.ManyToManyField(UnidadModelo, through='TratoModelo', related_name='modelosTrato')
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    nroMaestros = models.IntegerField(default=0)
    nroAyudantes = models.IntegerField(default=0)
    nroJornales = models.IntegerField(default=0)
    sueldoMaestro = models.IntegerField(default=0)
    sueldoAyudante = models.IntegerField(default=0)
    sueldoJornal = models.IntegerField(default=0)
    valorCuadrilla = models.IntegerField(default=0)
    valorTrato = models.BigIntegerField(default=0)
    cantidad = models.BigIntegerField(default=0)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    idUsuario = models.ForeignKey(User, on_delete=models.PROTECT) #(User, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT)
    orden = models.IntegerField(unique=True, blank=True, null=True)
    estado = models.IntegerField(default=1) #1 activo / 0 inactivo  
    
    def valorTrato_sep(self):
        if self.valorTrato != "" and self.valorTrato != "null":
            res = '{:,}'.format(self.valorTrato)
        else:
            res = '0'
        return res

    def sueldoMaestro_sep(self):
        if self.sueldoMaestro != "" and self.sueldoMaestro != "null":
            res = '{:,}'.format(self.sueldoMaestro)
        else:
            res = '0'
        return res
    
    def sueldoAyudante_sep(self):
        if self.sueldoAyudante != "" and self.sueldoAyudante != "null":
            res = '{:,}'.format(self.sueldoAyudante)
        else:
            res = '0'
        return res

    def sueldoJornal_sep(self):
        if self.sueldoJornal != "" and self.sueldoJornal != "null":
            res = '{:,}'.format(self.sueldoJornal)
        else:
            res = '0'
        return res
    
    def valorCuadrilla_sep(self):
        if self.valorCuadrilla != "" and self.valorCuadrilla != "null":
            res = '{:,}'.format(self.valorCuadrilla)
        else:
            res = '0'
        return res
    
    def save(self, *args, **kwargs):
        if self.orden is None:  # Solo establecer el orden si no está definido
            max_order = Trato.objects.aggregate(Max('orden'))['orden__max'] or 0
            self.orden = max_order + 1
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return self.partida